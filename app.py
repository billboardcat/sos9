import streamlit as st
import os
import pandas as pd
from SessionState import get


session_state = get(username='', password='', is_active=False)
default_pwd = "123"


def main():
    st.subheader("Hello, " + session_state.username + "!")
    st.sidebar.header("Step 1 - Get started by uploading your student data:")
    file = st.sidebar.file_uploader("Upload a CSV file, max 200 MB", type='csv')
    if file is not None:
        my_DF = pd.read_csv(file)
        st.write(my_DF)
    st.sidebar.header("Step 2 - Tell us more about your course's structure:")
    course_duration = st.sidebar.number_input(label="Course duration (in weeks)", min_value=1)
    graded_attendance = st.sidebar.checkbox(label='Graded attendance')
    lecture_online = st.sidebar.checkbox(label='Lecture materials are uploaded')
    supp_readings = st.sidebar.checkbox(label='Supplemental readings available')
    practice_exams = st.sidebar.checkbox(label='Practice exams available')
    lecture_quizzes = st.sidebar.checkbox(label='In-class quizzes')
    lecture_clickers = st.sidebar.checkbox(label='In-class questions (i.e. clicker questions)')
    course_calendar = st.sidebar.checkbox(label='Course calendar available')


if session_state.password != default_pwd:
    # This is a cleaner implementation of a theoretical user authentication & session model than what was previously
    # implemented. This also prevents StreamLit from rerunning the entire script when interacting with the web app.
    # Credit:
    # Code below modified from nth-attempt's post https://discuss.streamlit.io/t/user-authentication/612/16
    # 'SessionState.py' taken from https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92

    st.title("SOS 9!")
    st.header("Schools and Colleges Challenge - Team 9")
    if session_state.is_active:     # User has already logged in and is interacting with webapp, bypass login sequence
        main()
    else:                           # User has not logged in yet, run log in sequence
        usr_placeholder = st.empty()
        pwd_placeholder = st.empty()
        btn_placeholder = st.empty()
        usr = usr_placeholder.text_input("Username:", value="")
        pwd = pwd_placeholder.text_input("Password:", value="", type="password")
        is_pressed = btn_placeholder.button("Login")
        session_state.username = usr
        print(session_state.is_active)
        if len(usr) == 0:   # If the user does not input a username, default to "Guest"
            session_state.username = "Guest"
        if is_pressed:                      # When login button is pressed
            session_state.is_active = True  # Mark the session as active
            usr_placeholder.empty()         # Clear the username field
            pwd_placeholder.empty()         # Clear the password field
            btn_placeholder.empty()         # Clear the login button
            st.balloons()
            main()
        else:
            st.info("Please login before continuing")
else:
    main()
