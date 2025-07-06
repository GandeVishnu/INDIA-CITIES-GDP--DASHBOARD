import streamlit as st
import sqlite3
import os

# --- DATA BASE ---
DB_FILE = "signup.db"

# Initialize the SQLite Database and Table
def initialize_db():
    if not os.path.exists(DB_FILE):
        create_db()

def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Load users from the database
def load_users():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT email, name, password FROM users")
    users = cursor.fetchall()
    conn.close()
    return {user[0]: {"name": user[1], "password": user[2]} for user in users}

# Save a new user to the database
def save_user(email, name, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)", (email, name, password))
    conn.commit()
    conn.close()

# Initialize the database
initialize_db()

# --- CUSTOM CSS ---
def add_responsive_styles():
    st.markdown("""
        <style>
            /* General Page Styling */
            .title-text {
                font-size: 40px;
                font-weight: bold;
                color: DodgerBlue;
                text-align: center;
                text-transform: uppercase;
                letter-spacing: 3px;
                margin-top: 30px;
            }
            .subtitle-text {
                font-size: 18px;
                text-align: center;
                color: Tomato;
                margin-bottom: 20px;
            }
            /* Full-Width Buttons */
            div.stButton > button {
                width: 100%;
                background-color: #0B5ED7;
                color: white;
                padding: 12px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            div.stButton > button:hover {
                background-color: #084298;
                transition: 0.3s ease;
            }
            /* Responsive Adjustments */
            @media (max-width: 768px) {
                .title-text {
                    font-size: 30px;
                }
                .subtitle-text {
                    font-size: 16px;
                }
            }
        </style>
    """, unsafe_allow_html=True)


# Home Page
def home():
    add_responsive_styles()
    st.markdown('<div class="title-text">INDIACITYGDP: A VISUALIZATION OF URBAN ECONOMIC METRICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Explore the economic data of Indian cities through visualizations and interactive dashboards.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state["page"] = "Login"
            st.rerun()
    with col2:
        if st.button("Signup"):
            st.session_state["page"] = "Signup"
            st.rerun()

# Login Page
def login():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")  
    
    users = load_users()

    if st.button("Login"):
        if email in users and users[email]["password"] == password:
            st.success("Login Successful! Redirecting...")
            st.session_state["page"] = "Dashboard"
            st.rerun()
        else:
            st.error("Invalid email or password.")
    
    if st.button("Back to Home"):
        st.session_state["page"] = "Home"
        st.rerun()

# Signup Page
def signup():
    st.subheader("Signup")
    name = st.text_input("Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")  
    confirm_password = st.text_input("Re-enter Password", type="password", key="signup_confirm_password")

    users = load_users()
    
    if st.button("Signup"):
        if not name or not email or not password or not confirm_password:
            st.error("All fields are required.")
        elif email in users:
            st.error("User already exists!")
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            save_user(email, name, password)
            st.success("Signup Successful! Redirecting to Home...")
            st.session_state["page"] = "Home"
            st.rerun()
    
    if st.button("Back to Home"):
        st.session_state["page"] = "Home"
        st.rerun()

# Dashboard Page
def display_dashboard():
    st.title("Power BI Dashboard")
    st.markdown("""
        <div style="max-width: 100%; overflow: hidden;">
            <iframe 
                width="100%" 
                height="500px"
                src="https://app.powerbi.com/view?r=eyJrIjoiZmY4YTE1MjktMDlmMy00ZjU3LWE0NTUtMTY0ZTMxMmMwODA5IiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9" 
                frameborder="30" 
                allow="fullscreen">
            </iframe>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Signout"):
        st.session_state["page"] = "Home"
        st.rerun()

# --- MAIN APP ---
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    if st.session_state["page"] == "Home":
        home()
    elif st.session_state["page"] == "Login":
        login()
    elif st.session_state["page"] == "Signup":
        signup()
    elif st.session_state["page"] == "Dashboard":
        display_dashboard()

if __name__ == "__main__":
    main()
