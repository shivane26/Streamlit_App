import streamlit as st
import os
import csv

# File path for storing user data
file_path = os.path.join(os.getcwd(), "user_data.csv")

# Function to load user data from the CSV file
def load_user_data():
    if os.path.isfile(file_path):
        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            return list(reader)[1:]  # Skip the header row
    return []

# Function to check if the username exists
def username_exists(username):
    user_data = load_user_data()
    for user in user_data:
        if user[0] == username:  # Assuming username is the first column
            return True
    return False

# Function to verify login credentials
def verify_login(username, password):
    user_data = load_user_data()
    for user in user_data:
        if user[0] == username and user[1] == password:
            return True
    return False

# Initialize session state
if 'login_status' not in st.session_state:
    st.session_state.login_status = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Sidebar with dynamic navigation options based on login status
st.sidebar.title("Navigation")
if st.session_state.login_status:
    choice = st.sidebar.radio("Go to", ["Home"])
else:
    choice = st.sidebar.radio("Go to", ["Sign Up", "Login"])

# Sign-Up Page
if choice == "Sign Up":
    st.title('Sign Up to Your Journey')
    
    st.header("Create Your Account")

    # Input fields for user data (centered)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    phone_number = st.text_input("Phone Number")
    city = st.text_input("City")

    # Submit button (centered)
    if st.button("Submit"):
        if username and password and phone_number and city:
            if username_exists(username):
                st.error("Username already exists. Please choose a different username.")
            else:
                # Check if the file exists, if not create it and add headers
                file_exists = os.path.isfile(file_path)

                # Append user data to the CSV file
                with open(file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    
                    # Write headers if file doesn't exist
                    if not file_exists:
                        writer.writerow(["Username", "Password", "Phone Number", "City"])
                    
                    # Write user data
                    writer.writerow([username, password, phone_number, city])

                st.success("Sign-up successful! Your data has been saved.")
        else:
            st.error("Please fill in all the fields.")

# Login Page
elif choice == "Login":
    st.title('Login to Your Account')

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_login(username, password):
            st.session_state.login_status = True
            st.session_state.username = username
            # Redirect to the "Home" page
            st.experimental_set_query_params(page="home")
        else:
            st.error("Invalid username or password.")

# Home Page (after successful login)
elif choice == "Home":
    if st.session_state.login_status:
        st.title(f"Welcome to the Homepage, {st.session_state.username}!")
    else:
        st.warning("Please log in to access the homepage.")