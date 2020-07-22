import streamlit as st
import pandas as pd
from SessionState import get
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

session_state = get(username='', password='', is_active=False, step1_done=False)
default_pwd = "SOSdemopassword123"


def main():
    # Generate welcome message
    st.image(techpoint_logo, use_column_width=True)
    st.subheader("Hello, " + session_state.username + "! :smile:")
    start_placeholder = st.empty()

    if not session_state.step1_done:
        start_placeholder.info("Get started by uploading your course data in the sidebar")

    st.sidebar.header("Upload your course data")
    file = st.sidebar.file_uploader("Upload a CSV file, max 200 MB", type='csv')

    if file is None:
        st.sidebar.markdown("---")
        st.sidebar.markdown("<h2 style='color:maroon;'>Students to pay attention to</h2>", unsafe_allow_html=True)
        st.sidebar.subheader("After you upload your data, we'll identify students that may need attention")

    if file is not None:
        session_state.step1_done = True
        start_placeholder.empty()

        st.markdown("---")
        st.subheader("Here's the raw data. Make sure everything's looking right before continuing!")
        myDF = pd.read_csv(file)
        st.write(myDF.head(5))

        sidebar_analysis_placeholders = [st.sidebar.empty() for i in range(4)]

        # st.sidebar.markdown("---")
        # st.sidebar.header("Questions?")
        # st.sidebar.subheader("Contact Department Chair:")
        # st.sidebar.markdown("professor@university.edu")
        # st.sidebar.markdown("(800) 888-1234")
        # st.sidebar.subheader("Contact IT Assistance:")
        # st.sidebar.markdown("IT@university.edu")
        # st.sidebar.markdown("(800) 888-5678")

        # Q1: methods of communication v. final grades
        st.markdown("---")
        plt.style.use('ggplot')  # Personal style preference
        q1 = myDF.groupby(by='commMethod')['finalGrade'].mean()  # Grouping and averaging grades
        plt.bar(q1.index.values, q1.values, color='blue')  # Bar Plot
        plt.ylabel("Average Grade")
        plt.xlabel("Professor's Communication")
        plt.title("Comparing methods of Professor Communication via final grades", fontsize=12)
        st.pyplot()

        # Q2: graded attendance v. student interaction
        st.markdown("---")
        myDF['gradeAttendance'] = myDF['gradeAttendance'].replace({1: 'Yes', 0: 'No'})
        q2 = myDF.groupby(by='gradeAttendance')['attendanceCount'].mean()
        plt.bar(q2.index.values, q2.values, color='red')  # Bar Plot
        plt.ylabel("Lecture Attendance Count")
        plt.xlabel("Does the Professor Grade Attendance?")
        plt.title("Does Graded Attendance Increase Student Interaction?")
        st.pyplot()

        # Q3:
        st.markdown("---")
        q3DF = myDF[['attendanceCount', 'finalGrade']]
        corr = float(q3DF.corr().iloc[0, 1])

        st.header("Attendance and Assignment Grades")
        st.subheader("Correlation coefficient: {:.4f}".format(corr))
        # if corr > 0.9:
        #     st.subheader('There is likely a very high positive correlation between attendance and assignment grades')
        # if 0.9 > corr >= 0.7:
        #     st.subheader('There is likely a high positive correlation between attendance and assignment grades')
        # if 0.7 > corr >= 0.5:
        #     st.subheader('There is likely moderate positive correlation between attendance and assignment grades')
        # if 0.5 > corr >= 0.3:
        #     st.subheader('There is likely slight positive correlation between attendance and assignment grades')
        # if 0.3 > corr >= 0.0:
        #     st.subheader('There is likely no correlation between attendance and assignment grades')
        # if corr < 0.0:
        #     st.subheader('There is likely a negative correlation between attendance and assignment grades')

        if corr > 0.3:
            st.subheader("It is very likely that improving lecture attendance will result in improved grades. "
                         "Students with poor attendance are shown in the sidebar, "
                         "consider reaching out to them and help remove barriers discouraging them from attending.")

            # Also generate a message in the side bar ID-ing possible students of attention
            top5raw = myDF.sort_values('attendanceCount')[['First Name', 'Last Name']].head(5)
            top5raw['Names'] = top5raw['First Name'] + ' ' + top5raw['Last Name']
            top5names = ', '.join(list(top5raw['Names']))
            # print(top5names)
            sidebar_analysis_placeholders[0].markdown("---")
            sidebar_analysis_placeholders[1].markdown("<h2 style='color:maroon;'>Students to pay attention to</h2>",
                                                      unsafe_allow_html=True)
            sidebar_analysis_placeholders[2].subheader("Students with low attendance:")
            sidebar_analysis_placeholders[3].markdown(top5names)
        elif 0.3 >= corr >= -0.3:
            st.subheader("There is insufficient data to determine if lecture attendance improves student's grades.")
        else:
            st.subheader("It appears students who frequently attend lectures tend to have worse grades "
                         "than those who don't. This is a very complicated issue, "
                         "but start by reviewing your curriculum, as well as the format and length of your lectures.")

        # Q4
        st.markdown("---")
        st.header("Attendance and Lecture Engagement")
        dist = np.random.normal(9, 3, size=len(myDF['finalGrade']))
        dist = [int(i) for i in dist]
        myDF['questions'] = dist

        q4DF = myDF[['questions', 'finalGrade']]
        corr = float(q4DF.corr().iloc[0, 1])
        st.subheader("Correlation Coefficient: {:.4f}".format(corr))

        # if corr > 0.9:
        #     st.subheader('There is likely a very high positive correlation between attendance and lecture engagement')
        # if 0.9 > corr >= 0.7:
        #     st.subheader('There is likely a high positive correlation between attendance and lecture engagement')
        # if 0.7 > corr >= 0.5:
        #     st.subheader('There is likely moderate positive correlation between attendance and lecture engagement')
        # if 0.5 > corr >= 0.3:
        #     st.subheader('There is likely slight positive correlation between attendance and lecture engagement')
        # if 0.3 > corr >= 0.0:
        #     st.subheader('There is likely no correlation between attendance and lecture engagement')
        # if corr < 0.0:
        #     st.subheader('There is likely a negative correlation between attendance and lecture engagement')

        if corr > 0.3:
            st.subheader("It is very likely that improving class participation will result in improved grades. "
                         "Students with poor class participation are shown in the sidebar. "
                         "Consider engaging with these students during lecture "
                         "to ensure they are following with the instruction")
        elif 0.3 >= corr >= -0.3:
            st.subheader("There is insufficient data to determine if lecture engagement improves student's grades")
        else:
            st.subheader("It appears students that engage more in lectures receive lower grades than their peers. "
                         "This is a very complicated issue, but you should review the curriculum "
                         "and format of your lectures, as well as frequency of calling on students.")

        # st.sidebar.markdown("---")
        # st.sidebar.header("Questions?")
        # st.sidebar.subheader("Contact Department Chair:")
        # st.sidebar.markdown("professor@university.edu")
        # st.sidebar.markdown("(800) 888-1234")
        # st.sidebar.subheader("Contact IT Assistance:")
        # st.sidebar.markdown("IT@university.edu")
        # st.sidebar.markdown("(800) 888-5678")
    st.sidebar.markdown("---")
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

    techpoint_logo = Image.open('techpoint.jpg')
    step_logo = Image.open('step_logo.jpg')

    if session_state.is_active:     # User has already logged in and is interacting with webapp, bypass login sequence
        main()
    else:                           # User has not logged in yet, run log in sequence
        # Generate STEP logo and login message
        step_logo_placeholder = st.image(step_logo, use_column_width=True)
        login_msg = st.info("Please login before continuing")
        # st.header("Schools and Colleges Challenge - Team 9")

        # Generate fields for username & password, button for login
        usr_placeholder = st.empty()
        pwd_placeholder = st.empty()
        btn_placeholder = st.empty()
        usr = usr_placeholder.text_input("Username:", value="Jill Purdue")
        pwd = pwd_placeholder.text_input("Password:", value=default_pwd, type="password")
        is_pressed = btn_placeholder.button("Login")
        session_state.username = usr
        # techpoint_logo = st.image(techpoint_logo, use_column_width=True)

        if len(usr) == 0:   # If the user does not input a username, default to "Guest"
            session_state.username = "Guest"
        if is_pressed:                      # When login button is pressed
            session_state.is_active = True  # Mark the session as active
            step_logo_placeholder.empty()
            login_msg.empty()
            usr_placeholder.empty()         # Clear the username field
            pwd_placeholder.empty()         # Clear the password field
            btn_placeholder.empty()         # Clear the login button
            st.balloons()
            main()

else:
    main()
