import streamlit as st
import requests

from src.helper.endpoint import LOGIN_ENDPOINT, REGISTER_ENDPOINT
from src.helper.user_helper import check

headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}


def login():
    if "login_information" in st.session_state.keys():
        st.info("Logged In ✅")
        logout = st.button("Logout ❌")
        if logout:
            st.info("Logout successful!")
            st.session_state.clear()
            st.switch_page("pages/2_📲_Login.py")
    else:
        st.info("Please provide Email & Password")
        with st.form("Login Form"):
            email = st.text_input(
                "Enter your email 👇"
            )
            password = st.text_input("Enter your password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                success = check(email=email, password=password)
                if not success:
                    st.error("Please provide Email or Password")
                else:
                    response = requests.post("http://af18c1ae21c8a449d973b300b323f120-1681068879.ap-south-1.elb.amazonaws.com/api/v1/user/login",
                                             data={"username": email.lower(), "password": password}, headers=headers)
                    x = response.json()
                    if response.status_code != 200:
                        st.error(x["error"]["message"])
                    else:
                        st.session_state["login_information"] = {"type_of": "login",
                                                                 "response_data": {"access_token": x["access_token"],
                                                                                   "data": x["data"]}}
                        st.success("Login successful!")
                        st.switch_page("pages/3_🤖_Training.py")


if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False


def callback():
    st.session_state.button_clicked = True


def user_sign_up():
    if "login_information" not in st.session_state:
        if st.button("Don't have an account?", help="Register yourself",
                     on_click=callback) or st.session_state.button_clicked:
            with st.form("Form"):
                user_first_name = st.text_input("Enter your first name", placeholder="John")
                user_last_name = st.text_input("Enter your last name", placeholder="Doe")
                user_email = st.text_input(
                    "Enter your email 👇", placeholder="test@gmail.com"
                )
                user_password = st.text_input("Enter your password", type="password",
                                              placeholder="ThatOneShouldNeverGuess")
                submit = st.form_submit_button("Signup")
                if submit:
                    if len(user_first_name) == 0 or len(user_password) == 0 or len(user_last_name) == 0:
                        st.error("Please Check your data")
                    else:
                        response = requests.post(REGISTER_ENDPOINT,
                                                 json={"first_name": user_first_name,
                                                       "last_name": user_last_name,
                                                       "email": user_email,
                                                       "password": user_password
                                                       })
                        x = response.json()
                        if response.status_code == 422:
                            st.error("Please provide details correctly")
                        elif response.status_code != 200:
                            st.error(x["error"]["message"])
                        else:
                            st.success("Account Created Successfully,Please login to continue")
                            st.balloons()


login()
st.divider()
user_sign_up()
