import streamlit as st
import pandas as pd


def gen_sidebar():
    # Generate sidebar widgets
    st.sidebar.header("Step 1 - Upload your student data:")
    file = st.sidebar.file_uploader("Upload a CSV file, max 200 MB", type='csv')
    my_DF = None
    if file is not None:
        my_DF = pd.read_csv(file)
        # st.write(my_DF)

    st.sidebar.header("Step 2 - Tell us more about your course's structure:")

    course_desc = dict()

    # Yes/no questions, some will prompt for more information
    course_desc['graded_attendance'] = st.sidebar.checkbox(label='Graded attendance')
    course_desc['lect_online'] = st.sidebar.checkbox(label='Lecture materials are uploaded')
    course_desc['supp_readings'] = st.sidebar.checkbox(label='Supplemental readings available')
    course_desc['prac_exams'] = st.sidebar.checkbox(label='Practice exams available')
    course_desc['course_cal'] = st.sidebar.checkbox(label='Course calendar available')

    # Yes/no questions with follow-up
    course_desc['lect_quizzes'] = st.sidebar.checkbox(label='In-class quizzes')
    course_desc['quiz_count'] = 0 if not course_desc['lect_quizzes'] \
        else st.sidebar.number_input(label="Quiz count", min_value=1)

    course_desc['lect_clickers'] = st.sidebar.checkbox(label='In-class questions (i.e. clicker questions)')
    course_desc['clicker_freq'] = 0 if not course_desc['lect_clickers'] \
        else st.sidebar.selectbox(label='Clicker frequency', options=('Rarely', 'Sometimes', 'Often'))

    course_desc['hw_given'] = st.sidebar.checkbox(label='Homework given')
    course_desc['hw_count'] = 0 if not course_desc['hw_given'] \
        else st.sidebar.number_input(label='Homework count', min_value=1)
    course_desc['hw_length'] = 0 if not course_desc['hw_given'] \
        else st.sidebar.number_input(label='Avg homework length (hours)', min_value=0.0, value=0.0, step=0.5)

    course_desc['proj_given'] = st.sidebar.checkbox(label='Projects given')
    course_desc['proj_count'] = 0 if not course_desc['proj_given'] \
        else st.sidebar.number_input(label='Project count', min_value=1)

    course_desc['office_hrs'] = st.sidebar.checkbox(label='Office hours offered')
    course_desc['office_hrs_avg_attendance'] = 0 if not course_desc['office_hrs'] \
        else st.sidebar.number_input(label='Avg # of students attending office hours, per week')

    course_desc['ta_avail'] = st.sidebar.checkbox(label='TAs available')
    course_desc['ta_count'] = 0 if not course_desc['ta_avail'] \
        else st.sidebar.number_input(label='Number of TAs available', min_value=1)

    course_desc['visual_aids'] = st.sidebar.checkbox(label='Visual aids used')
    course_desc['visual_aid_usage'] = 0 if not course_desc['visual_aids'] \
        else st.sidebar.slider(label='Visual aid usage, 10 is \"Very Often\"',
                               value=5, min_value=1, max_value=10, step=1)

    course_desc['in_class_interaction'] = st.sidebar.checkbox(label='In-class interaction (student)')
    course_desc['in_class_int'] = 0 if not course_desc['in_class_interaction'] \
        else st.sidebar.slider(label='Interaction frequency, 10 is \"Very Often\"',
                               value=5, min_value=1, max_value=10, step=1)

    # Pure-numerical input
    course_desc['avg_lect_student_count'] = st.sidebar.number_input(label='Avg # of students attending lectures, per lecture')
    course_desc['lecture_duration'] = st.sidebar.number_input(label="Lecture duration (in hours)", min_value=1.0, step=0.5)
    course_desc['course_duration'] = st.sidebar.number_input(label="Course duration (in weeks)", min_value=1)
    course_desc['term_duration'] = st.sidebar.number_input(label="School term duration (in weeks)", min_value=1)

    if course_desc['term_duration'] < course_desc['course_duration']:  # Check to make sure a valid course duration was chosen
        st.error("Error: School term duration cannot be smaller than course duration")

    # Choice
    course_desc['course_structure'] = st.sidebar.selectbox(label='Course organization', options=(
    'Traditional lecture', 'Team-based lecture', 'Reverse classroom', 'Other'))

    return course_desc, my_DF