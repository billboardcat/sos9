import streamlit as st
import os
import pandas as pd
from SessionState import get
from PIL import Image


session_state = get(username='', password='', is_active=False)
default_pwd = "123"


def main():
    st.subheader("Hello, " + session_state.username + "! :smile:")
    st.info("Get started by answering some questions about your course in the sidebar")
    st.sidebar.header("Step 1 - Upload your student data:")
    file = st.sidebar.file_uploader("Upload a CSV file, max 200 MB", type='csv')
    if file is not None:
        my_DF = pd.read_csv(file)
        st.write(my_DF)

    st.sidebar.header("Step 2 - Tell us more about your course's structure:")

    # Yes/No questions, some will prompt for more information
    graded_attendance = st.sidebar.checkbox(label='Graded attendance')
    lecture_online = st.sidebar.checkbox(label='Lecture materials are uploaded')
    supp_readings = st.sidebar.checkbox(label='Supplemental readings available')
    practice_exams = st.sidebar.checkbox(label='Practice exams available')
    course_calendar = st.sidebar.checkbox(label='Course calendar available')

    lecture_quizzes = st.sidebar.checkbox(label='In-class quizzes')
    quiz_count = 0 if not lecture_quizzes else st.sidebar.number_input(label="Quiz count", min_value=1)

    lecture_clickers = st.sidebar.checkbox(label='In-class questions (i.e. clicker questions)')
    clicker_freq = None if not lecture_clickers else st.sidebar.selectbox(label='Clicker frequency', options=('Rarely', 'Sometimes', 'Often'))

    homeworks_given = st.sidebar.checkbox(label='Homework given')
    homework_count = 0 if not homeworks_given else st.sidebar.number_input(label='Homework count', min_value=1)
    homework_length = 0 if not homeworks_given else st.sidebar.number_input(label='Avg homework length (hours)', min_value=0.0, value=0.0, step=0.5)

    projects_given = st.sidebar.checkbox(label='Projects given')
    project_count = 0 if not projects_given else st.sidebar.number_input(label='Project count', min_value=1)

    office_hours_offered = st.sidebar.checkbox(label='Office hours offered')
    avg_office_hrs_student_count = 0 if not office_hours_offered else st.sidebar.number_input(label='Avg # of students attending office hours, per week')

    tas_available = st.sidebar.checkbox(label='TAs available')
    ta_count = 0 if not tas_available else st.sidebar.number_input(label='Number of TAs available', min_value=1)

    avg_lecture_student_count = st.sidebar.number_input(label='Avg # of students attending lectures, per lecture')

    lecture_duration = st.sidebar.number_input(label="Lecture duration (in hours)", min_value=1.0, step=0.5)
    course_duration = st.sidebar.number_input(label="Course duration (in weeks)", min_value=1)
    term_duration = st.sidebar.number_input(label="School term duration (in weeks)", min_value=1)
    if term_duration < course_duration:
        st.error("Error: School term duration cannot be smaller than course duration")

    st.sidebar.header("Questions?")
    st.sidebar.subheader("Contact Department Chair:")
    st.sidebar.markdown("professor@university.edu")
    st.sidebar.markdown("(800) 888-1234")
    st.sidebar.subheader("Contact IT Assistance:")
    st.sidebar.markdown("IT@university.edu")
    st.sidebar.markdown("(800) 888-5678")



if session_state.password != default_pwd:
    # This is a cleaner implementation of a theoretical user authentication & session model than what was previously
    # implemented. This also prevents StreamLit from rerunning the entire script when interacting with the web app.
    # Credit:
    # Code below modified from nth-attempt's post https://discuss.streamlit.io/t/user-authentication/612/16
    # 'SessionState.py' taken from https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92

    image2 = Image.open('techpoint.jpeg')
    st.image(image2, use_column_width=True)
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
