import streamlit as st
import pickle
from streamlit_option_menu import option_menu

from predict_page import show_predict_page
from explore_page import  show_explore_page
page=option_menu(
    menu_title="Main Menu",
    options=["Home","Predict","Explore"],
    icons=["house-user","rocket","compass"],
  
    
    orientation ="horizontal",
)
styles={
    "container":{"padding":"0!important","background-color":"green"},
    "nav-link":
        {
            "font-size":"25px",
            "text-align":"left",
            "margin":"0 px",
            "hover-color":"blue"
        },
        "nav-link-selected":{"border-bottom":"3px solid white",'color':'red'},
        
}
if page=="Home":
    show_app1()
if page == "Predict":
    show_predict_page()
if page=="Explore":
    show_explore_page()