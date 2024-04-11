import streamlit as st
import pandas as pd
import hashlib
import sqlite3
import pickle
import numpy as np
# Import CSS
st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)

# Function to hash passwords
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Function to check hashed passwords
def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# Connect to SQLite database
conn = sqlite3.connect('dat.db')
c = conn.cursor()

# Function to create user table in database if not exists
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT, age INTEGER, location TEXT)')

# Function to add user data to database
def add_userdata(username, password, age, location):
    c.execute('INSERT INTO userstable(username, password, age, location) VALUES (?,?,?,?)', (username, password, age, location))
    conn.commit()

# Function to login user
def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

# Function to view all users
def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

# Function to load the prediction model
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
        return data

# Load model and label encoders
data = load_model()
regressor_loaded = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

# Function to show the Predict page
def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""We need some information to predict the salary""")

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )
    education_levels = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education_levels)
    experience = st.slider("Years of Experience", 0, 50, 3)

    if st.button("Calculate Salary"):
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor_loaded.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

# Function to show the Explore page
def show_explore_page():
    st.write("Explore Page")

# Main function
def main():
    st.title("Simple Login App")
    st.write("This app provides a convenient platform for users to log in, sign up, and explore features related to software development. One of the key features of our app is the Software Price Prediction module.")
    st.header(" Software Price Prediction")
    st.write("Are you curious about how much your software development skills could earn you? Our software price prediction feature utilizes machine learning to estimate the salary of a software developer based on various factors such as country, education level, and years of experience.")

    st.write(" Simply navigate to the Predict section in the sidebar menu after logging in, input your information, and let our model do the rest. Get an instant estimate of your potential salary and plan your career accordingly!")
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu, format_func=lambda x: ' '.join(x.split()), key="sidebar")

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username, check_hashes(password, hashed_pswd))
            
            if result:
                st.success("Logged In as {}".format(username))
                st.balloons()  # Show balloon message upon successful login

                page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))
                
                if page == "Predict":
                    show_predict_page()
                else:
                    show_explore_page()

            #user_result = view_all_users()
            
            #clean_db = pd.DataFrame(user_result, columns=["Username", "Password", "Age", "Location"])
           # st.dataframe(clean_db)
                
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        new_age = st.number_input("Age")
        new_location = st.text_input("Location")

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password), new_age, new_location)
            st.success("You have successfully created a valid Account")
            st.success("🎆 Congratulations! You've successfully signed up!")  # Show firecracker message upon successful sign-up

if __name__ == '__main__':
    main()
