import streamlit as st
import time
import requests
from src.helper.endpoint import INPROGRESS_TRAINING_ENDPOINT, IMAGE_UPLOAD_ENDPOINT, CHECK_TRAINING_ENDPOINT, \
    START_TRAINING, FETCH_TRAINING


def check_inprogress_training(user_id):
    response = requests.get(INPROGRESS_TRAINING_ENDPOINT.format(user_id))
    x = response.json()
    if response.status_code == 422:
        st.error("Please provide details correctly")
    elif response.status_code != 200:
        st.error(x["error"]["message"])
    else:
        if x["data"] is None:
            return True


def image_upload(files):
    headers = {'accept': 'application/json',
               "Authorization": "Bearer {}".format(
                   st.session_state["login_information"]["response_data"]["access_token"])
               }
    response = requests.post(IMAGE_UPLOAD_ENDPOINT,
                             headers=headers,
                             files=files)
    x = response.json()
    if response.status_code == 422:
        return {"success": False, "data": {}}
    elif response.status_code != 200:
        return {"success": False, "data": {}}
    else:
        st.session_state.update({"upload": {"s3_url": x["s3_uri"],
                                            "bucket": x["bucket"]
                                            }
                                 })
        return {"success": True}


def check_training(user_id, job_name):
    response = requests.get(CHECK_TRAINING_ENDPOINT.format(user_id, job_name))
    x = response.json()
    if response.status_code == 422:
        st.error("Please provide details correctly")
    elif response.status_code != 200:
        st.error(x["error"]["message"])
    else:
        if x["data"] is None:
            return True


def start_training(metadata):
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json',
               "Authorization": "Bearer {}".format(
                   st.session_state["login_information"]["response_data"]["access_token"])
               }
    response = requests.post(START_TRAINING,
                             headers=headers,
                             json={"training_params": {"name": metadata["name"],
                                                       "resolution": str(metadata["resolution"])
                                                       },
                                   "training_prompt_params": {"instance_prompt": metadata["instance_prompt"],
                                                              "class_prompt": metadata["class_prompt"]
                                                              },
                                   "bucket": {"bucket_name": st.session_state["upload"]["bucket"],
                                              "key_name": "a",
                                              "path": st.session_state["upload"]["s3_url"],
                                              "object_key": "a"
                                              }
                                   }
                             )
    x = response.json()
    if response.status_code == 422:
        return {"success": False, "data": {}}
    elif response.status_code != 200:
        return {"success": False, "data": {}}
    else:
        return x


def cooling_highlight(val):
    color = '#ACE5EE' if val else 'white'
    return f'background-color: {color}'


def fetch_trained_model_list():
    import pandas as pd
    response = requests.get(FETCH_TRAINING.format(
        st.session_state["login_information"]["response_data"]["data"]["id"]))

    if response.status_code == 422:
        st.error("Internal Server Error")
    elif response.status_code != 200:
        st.error("Internal Server Error")
    x = response.json()
    df = pd.DataFrame(x["data"]
                      )
    st.dataframe(df.style.applymap(cooling_highlight, subset=['Status', 'Failure']),
                 #  ,(heating_highlight, subset=['Heating inputs', 'Heating outputs'])
                 hide_index=True,
                 width=1100
                 )


def past_training_page():
    fetch_trained_model_list()


def training_page():
    # Create two columns to arrange widgets horizontally
    check_wait_time = requests.get("https://mlbe.rekogniz.com/v1/wait-time",verify=False)
    check_wait_time = check_wait_time.json()

    if 10 <= check_wait_time["data"] <= 20:
        st.info("Current training wait time is {} minutes 😤".format(check_wait_time["data"]))

    elif 0 <= check_wait_time["data"] <= 9:
        st.success("No waiting time for training job 😄")
    else:
        st.warning("Current training wait time is greater than 25 minutes 🤷")

    select = st.selectbox(label="Proceed with training", options=["Training"], index=None)
    if select == "Training":
        with st.form("Training Form"):
            col1, col2 = st.columns(2)

            # Text input for training job name
            with col1:
                training_job_name = st.text_input("Training job name", placeholder="my-taining-job",
                                                  help="Unique name of training")
                object_type = st.text_input("Object Type", placeholder="headphone", help="Type of the object")
                images = st.file_uploader("Upload Images", accept_multiple_files=True,
                                          type=['png', 'jpg', 'jpeg'], help="Please provide 4-8 images")
            with col2:
                resolution_ = st.selectbox("Resolution", options=[512, 1024], help="Image resolution")
                modifier_token = st.text_input("Unique identifier", placeholder="Short word identifier ex-pro#1",
                                               help="Unique and short")
                purpose_training = st.multiselect("Model will be used for",
                                                  options=["Professional", "Random", "Rendering"])
            submit_ = st.form_submit_button("Start Training")
            if submit_:
                if len(training_job_name) == 0 or len(object_type) == 0 or len(modifier_token) == 0:
                    st.error("Please define parameters properly")
                    st.stop()
                elif len(images) <= 3:
                    st.error("Please provide 4/5 images")
                    st.stop()
                elif training_job_name:
                    success = check_training(
                        user_id=st.session_state["login_information"]["response_data"]["data"]["id"],
                        job_name=training_job_name)
                    if not success:
                        st.error("OOPS!! Training Job With Similar Name Exist,Please change name.")
                        st.stop()
                files_dict = {}
                for file in images:
                    files_dict[f"files"] = (file.name, file.getvalue(), file.type)
                success_file_upload = image_upload(files=files_dict)
                if not success_file_upload["success"]:
                    st.error("OOPS! Something went wrong,Please try again later")
                    st.stop()
                with st.status("Starting Training Job") as status:
                    try:
                        st.info("Looking For Machine...")
                        time.sleep(1)
                        st.info("Requesting Machine...")
                        st.info("Checking Training Configurations")
                        st.info("Checking...")
                        check = check_inprogress_training(
                            user_id=st.session_state["login_information"]["response_data"]["data"]["id"])
                        if not check:
                            st.error("One or more training already in progress")
                            status.update(label="Training Failed", state="error", expanded=True)
                            st.stop()
                        start_training_job = start_training(metadata={"name": training_job_name,
                                                                      "resolution": resolution_,
                                                                      "instance_prompt": modifier_token,
                                                                      "class_prompt": object_type
                                                                      })
                        if not start_training_job["success"]:
                            st.error("Can't find Machine to launch training")
                            status.update(label="Training Failed", state="error", expanded=True)
                        # training estimated time, training start time, training complete time in st.success
                    except Exception as E:
                        st.error(f"Error occurred: {str(E)}")  # Display error message
                    st.success("Training Started Successfully,to be completed at {}".format(
                        start_training_job["data"]["end_time"]))


def container():
    x = st.radio(label="Please Select Option", options=["Trained Models", "Create Training"], horizontal=True,
                 key="radio1")
    if x == "Create Training":
        if "login_information" not in st.session_state.keys():
            st.error("Please Log in first")
        else:
            training_page()
    else:
        if "login_information" not in st.session_state.keys():
            st.error("Please Log in first")
        else:
            past_training_page()


container()
