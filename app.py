import streamlit as st
import os
import pandas as pd

# is_authenticated: checks for a valid password
# Args:     password -- string
# Return:   bool
def is_authenticated(password):
    return password == "123"


# generate_login_block: creates the blocks for the login page
def generate_login_block():
    block1 = st.empty()
    block2 = st.empty()

    return block1, block2


# clean_blocks: clears StreamLit blocks in a list; currently used to clear login fields
def clean_blocks(blocks):
    for block in blocks:
        block.empty()


# login: gets the username and password from the client
def login(blocks):
    return blocks[0].text_input('Username'), blocks[1].text_input('Password', type='password')


def main(username):
    st.balloons()
    st.title('SOS 9!')
    st.header('Schools and Colleges Challenge - Team 9')
    st.subheader('Hello, ' + username + '!')
    st.title('This is Erik\'s test ')

    st.sidebar.subheader('Get started by uploading your student data:')
    file = st.sidebar.file_uploader('Upload a CSV file, max 200 MB', type='csv')
    if file is not None:
        my_DF = pd.read_csv(file)
        st.write(my_DF)

# Code to simulate a login page.
# Code and relevant functions implemented from: https://discuss.streamlit.io/t/user-authentication/612/7
login_blocks = generate_login_block()
username, password = login(login_blocks)

if is_authenticated(password):
    clean_blocks(login_blocks)
    main(username)
elif password:
    st.info("Please enter a valid password")
