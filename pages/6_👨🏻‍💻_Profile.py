import streamlit as st
import requests
from src.helper.user_helper import check_password_strength


def profile():
    # Sample user data (replace with actual user data)
    if "login_information" not in st.session_state.keys():
        st.error("Please Login First")
        login = st.button("Login ✅", help="Login first")
        if login:
            st.switch_page("pages/2_📲_Login.py")
    else:
        user_data = {
            "first_name": st.session_state["login_information"]["response_data"]["data"]["first_name"],
            "last_name": st.session_state["login_information"]["response_data"]["data"]["last_name"],
            "email": st.session_state["login_information"]["response_data"]["data"]["email"]
        }

        with st.form("Profile"):
            # Display profile picture in the middle
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                display_profile_pic(user_data['first_name'].upper(), user_data['last_name'].upper())

            # Display title for user information
            st.subheader("User Information")
            # Display user information in columns
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name", value=user_data['first_name'], key='first_name')
                last_name = st.text_input("Last Name", value=user_data['last_name'], key='last_name')
            with col2:
                email = st.text_input("Email", value=user_data['email'], key='email', disabled=True)
                verified = st.text_input("Verified", value="Verified✅", disabled=True)
            submit = st.form_submit_button("Update Profile")
            if submit:
                headers = {'accept': 'application/json',
                           'Content-Type': 'application/json',
                           "Authorization": "Bearer {}".format(
                               st.session_state["login_information"]["response_data"]["access_token"])
                           }
                response = requests.patch("http://localhost:8000/api/v1/user/profile",
                                          json={"first_name": first_name,
                                                "last_name": last_name
                                                }, headers=headers
                                          )
                x = response.json()
                if response.status_code == 422:
                    st.error("Please provide details correctly")
                elif response.status_code != 200:
                    st.error(x["error"]["message"])
                else:
                    st.session_state["login_information"]["response_data"]["data"]["first_name"] = first_name
                    st.session_state["login_information"]["response_data"]["data"]["last_name"] = last_name
                    st.success("Profile Updated Successfully")
                    st.balloons()


def display_profile_pic(first_name, last_name):
    # Get initials for profile picture
    initials = (first_name[0] if first_name else '') + (last_name[0] if last_name else '')

    # Set profile picture size and background color
    profile_pic_size = 100
    profile_pic_bg_color = "#FF69B4"  # You can change the background color as needed

    # Display profile picture
    st.markdown(
        f'<div style="width: {profile_pic_size}px; height: {profile_pic_size}px; margin: auto; border-radius: 50%; background-color: {profile_pic_bg_color}; display: flex; justify-content: center; align-items: center; color: #000000; font-size: 48px; font-weight: bold;">{initials}</div>',
        unsafe_allow_html=True
    )


profile()


def change_password():
    if "login_information" in st.session_state.keys():
        with st.form("ChangePassword"):
            st.subheader("Change Password")
            # Display user information in columns
            col1, col2 = st.columns(2, gap="large")
            with col1:
                current_password = st.text_input("Current Password", type="password",placeholder="your-current-password")
                new_password = st.text_input("New Password", key='b', type="password", max_chars=30,placeholder="ThatOneShouldNeverGuess")
                confirm_password = st.text_input("Confirm Password", type="password", max_chars=30,placeholder="ThatOneShouldNeverGuess")
            submit = st.form_submit_button("Update Password")
            if submit:
                if len(confirm_password) == 0 or len(new_password) == 0:
                    st.error("Please enter the password")
                elif confirm_password != new_password:
                    st.error("Passwords are not same")
                elif current_password == new_password:
                    st.error("New password and current password cannot be same")
                else:
                    check = check_password_strength(password=confirm_password)
                    if not check:
                        st.error("Please use a strong password,with characters and numbers")
                        st.stop()
                    # make api call
                    headers = {'accept': 'application/json',
                               'Content-Type': 'application/json',
                               "Authorization": "Bearer {}".format(
                                   st.session_state["login_information"]["response_data"]["access_token"])
                               }
                    response = requests.post("http://localhost:8000/api/v1/user/change-password",
                                              json={"current_password": current_password,
                                                    "new_password": new_password,
                                                    "confirm_password": confirm_password
                                                    }, headers=headers
                                              )
                    x = response.json()
                    if response.status_code == 422:
                        st.error("Please provide details correctly")
                    elif response.status_code != 200:
                        st.error(x["error"]["message"])
                    else:
                        st.success("Password Updated Successfully")
                        st.balloons()


change_password()
