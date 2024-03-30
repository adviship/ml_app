import streamlit as st
import pickle

from streamlit_option_menu import option_menu
from predict_page import show_predict_page
from explore_page import show_explore_page


st.title("Software Salary Prediction")
st.header("About Software Salary Prediction")
st.write("""
    This web application is designed to predict the salary of software engineers based on various features such as education, experience, location, etc. 
    The prediction model is built using machine learning algorithms and trained on a dataset of software engineer salaries.
    
    **Features:**
    - Education: The highest level of education completed by the software engineer.
    - Experience: The number of years of experience in the software engineering field.
    - Location: The geographical location where the software engineer works.
    - Skills: Relevant technical skills possessed by the software engineer.
    
    **Model:**
    The prediction model is trained using a regression algorithm, which learns the relationship between the features and the salary from the dataset. 
    Once trained, the model can predict the salary of a software engineer given their features.
    
    **Dataset:**
    The dataset used for training the model contains information about software engineer salaries collected from various sources.
    
    **Disclaimer:**
    The predictions provided by this web application are estimates and may not accurately reflect real-world salaries. 
    The actual salary of a software engineer may vary based on individual factors not captured by the model.
    """)

page=option_menu (
    menu_title="Main Menu",
    options=["Home","Predict",],
    icons=['house','gear'],
    orientation ="horizontal",
)

if page == "Predict":
    show_predict_page()

