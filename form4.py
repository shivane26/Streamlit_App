import streamlit as st
import os
import json
import csv

# Paths for storing user data
USER_DATA_DIR = 'users_data'
USER_DATA_FILE = 'user_data.json'

# Create directory for storing user information if not exists
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

# Load or create user data file
if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'r') as file:
        user_data = json.load(file)
else:
    user_data = {}

# Sidebar for navigation
page = st.sidebar.radio("Navigate", ["Sign Up", "Login", "Submit Marks", "View Report"])

# Session state to keep track of logged-in user
if 'email' not in st.session_state:
    st.session_state.email = None

# Sign Up Page
if page == "Sign Up":
    st.title("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if email not in user_data:
            user_data[email] = {'name': name, 'password': password}
            with open(USER_DATA_FILE, 'w') as file:
                json.dump(user_data, file)
            os.makedirs(os.path.join(USER_DATA_DIR, email))  # Create folder for user
            st.success("Signed up successfully!")
        else:
            st.error("Email already registered!")

# Login Page
if page == "Login":
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email in user_data and user_data[email]['password'] == password:
            st.session_state.email = email
            st.success(f"Welcome, {user_data[email]['name']}!")
        else:
            st.error("Invalid email or password.")

# Marks Submission Page (only visible after login)
if page == "Submit Marks" and st.session_state.email:
    st.title(f"Welcome {user_data[st.session_state.email]['name']}")

    # Submit Marks Section
    st.subheader("Submit Your Marks")
    subjects = ["Maths", "Science", "English", "History", "Geography", "Art", "PE"]
    marks = {}

    for subject in subjects:
        marks[subject] = st.slider(f"Marks for {subject}", 0, 100)

    if st.button("Submit Marks"):
        user_folder = os.path.join(USER_DATA_DIR, st.session_state.email)
        with open(os.path.join(user_folder, 'marks.csv'), 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=marks.keys())
            writer.writeheader()
            writer.writerow(marks)
        st.success("Marks submitted successfully!")

# View Report Page (only visible after login)
if page == "View Report" and st.session_state.email:
    st.title(f"Welcome {user_data[st.session_state.email]['name']}")

    # View Report Section
    st.subheader("Your Report")
    user_folder = os.path.join(USER_DATA_DIR, st.session_state.email)
    marks_file = os.path.join(user_folder, 'marks.csv')

    if os.path.exists(marks_file):
        with open(marks_file, 'r') as file:
            reader = csv.DictReader(file)
            marks = next(reader)
            subjects = list(marks.keys())
            values = list(map(int, marks.values()))

            st.subheader("Marks per Subject")
            for subject, value in zip(subjects, values):
                st.text(f"{subject}: {value}")

            # Calculate and show average marks
            avg_marks = sum(values) / len(values)
            st.text(f"Average Marks: {avg_marks}")
    else:
        st.error("No marks found!")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.email = None
    st.success("Logged out successfully!")

# If user is not logged in, restrict access to Submit Marks and View Report pages
if page in ["Submit Marks", "View Report"] and not st.session_state.email:
    st.warning("Please login first to submit marks or view your report.")
