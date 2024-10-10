import numpy as np
import streamlit as st
import time
import requests
from src.helper.endpoint import INPROGRESS_TRAINING_ENDPOINT, IMAGE_UPLOAD_ENDPOINT, CHECK_TRAINING_ENDPOINT, \
    START_TRAINING, FETCH_TRAINING, USER_PROFILE
from src.helper.user_helper import generate_random_word
from PIL import Image
from streamlit_drawable_canvas import st_canvas
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
def image_upload(files, is_logo_exist: dict, dataset_name: str):
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
        if is_logo_exist.keys():
            st.session_state.update({"upload": [{"dataset_name": dataset_name,
                                                 "s3_url": x["s3_uri"],
                                                 "bucket": x["bucket"],
                                                 "coordinates": is_logo_exist}]})
        else:
            st.session_state.update({"upload": [{"dataset_name": dataset_name,
                                                 "s3_url": x["s3_uri"],
                                                 "bucket": x["bucket"],
                                                 "coordinates": {}}]})
        return {"success": True, "data": x}
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
    # in this we are only creating one and only one dataset at a time
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json',
               "Authorization": "Bearer {}".format(
                   st.session_state["login_information"]["response_data"]["access_token"])
               }
    response = requests.post(START_TRAINING,
                             headers=headers,
                             json={"training_params": {"name": metadata["name"],
                                                       "resolution": str(metadata["resolution"]),
                                                       "dataset_config": st.session_state["upload"][0]
                                 ,
                                                       },
                                   "training_prompt_params": {"instance_prompt": metadata["instance_prompt"],
                                                              "class_prompt": metadata["class_prompt"]
                                                              },
                                   "bucket": {"bucket_name": st.session_state["upload"][0]["bucket"],
                                              "key_name": "a",
                                              "path": st.session_state["upload"][0]["s3_url"],
                                              "object_key": "a"
                                              }
                                   }
                             )
    print("HERERER")
    x = response.json()
    print(x)
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
def check_user_verification():
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json',
               "Authorization": "Bearer {}".format(
                   st.session_state["login_information"]["response_data"]["access_token"])
               }
    response = requests.get(USER_PROFILE, headers=headers, verify=False)
    if response.status_code == 422:
        return False
    elif response.status_code != 200:
        return False
    else:
        data = response.json()
        if not data["data"]["is_verified"]:
            return False
        else:
            return True
def training_page():
    # Create two columns to arrange widgets horizontally
    # check_wait_time = requests.get("https://mlbe.rekogniz.com/v1/wait-time",
    #                                headers={"verification-key":"cmVrb0duaXpUZWNobm9sb2dpZXNQcmlWYVRlTGlNZXRlZCMjIzEyMzQwOTY4OTY="},
    #                                verify=False)
    # check_wait_time = check_wait_time.json()
    #
    # if 10 <= check_wait_time["data"] <= 20:
    #     st.info("Current training wait time is {} minutes 😤".format(check_wait_time["data"]))
    #
    # elif 0 <= check_wait_time["data"] <= 9:
    #     st.success("No waiting time for training job 😄")
    # else:
    #     st.warning("Current training wait time is greater than 25 minutes 🤷")
    select = st.selectbox(label="Proceed with training", options=["Training", "Background Replacement", "Apparels"],
                          index=None)
    if select == "Training":
        verify = check_user_verification()
        if not verify:
            st.error("Please ask Rekogniz Team for setting up quota to start training")
            st.stop()
        else:
            modifier = "<" + generate_random_word() + ">"
            check = []
            if "upload" in st.session_state.keys():
                for k in st.session_state["upload"]:
                    check.append(k["dataset_name"])
            with st.form("Training Form"):
                col1, col2 = st.columns(2)
                # Text input for training job name
                with col1:
                    training_job_name = st.text_input("Training job name", placeholder="my-taining-job",
                                                      help="Unique name of training")
                    object_type = st.text_input("Object Type", placeholder="headphone", help="Type of the object")
                    dataset_name = st.selectbox("Dataset Name", options=check)
                with col2:
                    resolution_ = st.selectbox("Resolution", options=[512, 1024], help="Image resolution")
                    st.text_input("Unique identifier", placeholder=modifier,
                                  help="Unique and short identifier to describe images", disabled=True)
                    purpose_training = st.multiselect("Model will be used for",
                                                      options=["Professional", "Random", "Rendering"])
                submit_ = st.form_submit_button("Start Training")
                if submit_:
                    if len(training_job_name) == 0 or len(object_type) == 0:
                        st.error("Please define parameters properly")
                        st.stop()
                    elif training_job_name:
                        success = check_training(
                            user_id=st.session_state["login_information"]["response_data"]["data"]["id"],
                            job_name=training_job_name)
                        if not success:
                            st.error("OOPS!! Training Job With Similar Name Exist,Please change name.")
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
                                                                          "instance_prompt": modifier,
                                                                          "class_prompt": object_type
                                                                          }
                                                                )
                            if not start_training_job["success"]:
                                st.error("Can't find Machine to launch training")
                                status.update(label="Training Failed", state="error", expanded=True)
                            # training estimated time, training start time, training complete time in st.success
                        except Exception as E:
                            st.error(f"Error occurred: {str(E)}")  # Display error message
                        else:
                            st.success("Training Started Successfully,to be completed at {}".format(
                                start_training_job["data"]["end_time"]))
def dataset():
    # Only one dataset will exist in the upload at a time
    st.warning("Please tick the box if your products need fine detailing and have logos")
    sel = st.checkbox("Does your product have logo?", help="We need to annotate images for better"
                                                           "training of logo")
    images = st.file_uploader("Upload Images", accept_multiple_files=True,
                              type=['png', 'jpg', 'jpeg'], help="Please provide 4-8 images")
    dataset_name = st.text_input("Please enter the dataset name")
    check = []
    if "upload" in st.session_state.keys():
        for k in st.session_state["upload"]:
            check.append(k["dataset_name"])
    if sel:
        if dataset_name is not None and dataset_name in check:
            st.error("Dataset name already exist")
            st.stop()
        files_dict = {}
        if images is not None:
            if len(images) <= 3:
                st.error("Please provide 4/5 images")
                st.stop()
            for file in images:
                image = Image.open(file)
                image = np.array(image)
                st.subheader(f"Annotate Image: {file.name}")
                canvas_result = st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                    stroke_width=3,
                    stroke_color="#00FF00",
                    background_image=Image.fromarray(image),
                    update_streamlit=True,
                    height=image.shape[0],
                    width=image.shape[1],
                    drawing_mode="rect",
                    key=f"canvas_{file.name}",
                )
                if canvas_result.json_data is not None:
                    objects = canvas_result.json_data["objects"]
                    for obj in objects:
                        if obj["type"] == "rect":
                            st.write(
                                f"Rectangle: {obj['left']}, {obj['top']}, {obj['width']}, {obj['width']}")
                            if file.name in files_dict.keys():
                                files_dict[file.name] = [obj['left'], obj['top'], obj['width'], obj['width']]
                            else:
                                files_dict.update({file.name: [obj['left'], obj['top'], obj['width'], obj['width']]})
        if files_dict.keys():
            file_names = {}
            for file in images:
                file_names[f"files"] = (file.name, file.getvalue(), file.type)
            check = st.button("Upload Files")
            if check:
                success_file_upload = image_upload(files=file_names, is_logo_exist=files_dict,
                                                   dataset_name=dataset_name)
                if not success_file_upload["success"]:
                    st.error("OOPS! Something went wrong,Please try again later")
                    st.stop()
                else:
                    st.write(st.session_state)
    else:
        if images is not None:
            if dataset_name is not None and dataset_name in check:
                st.error("Dataset name already exist")
                st.stop()
            files_dict = {}
            if len(images) <= 3:
                st.error("Please provide 4/5 images")
                st.stop()
            for file in images:
                files_dict[f"files"] = (file.name, file.getvalue(), file.type)
            if files_dict.keys():
                check = st.button("Upload Files")
                if check:
                    success_file_upload = image_upload(files=files_dict, is_logo_exist={}, dataset_name=dataset_name)
                    if not success_file_upload["success"]:
                        st.error("OOPS! Something went wrong,Please try again later")
                        st.stop()
                    else:
                        st.write(st.session_state)
                    # redirect to training page
def container():
    x = st.radio(label="Please Select Option", options=["Trained Models", "Create Experiment", "Make Dataset"],
                 horizontal=True,
                 key="radio1")
    if x == "Create Experiment":
        if "login_information" not in st.session_state.keys():
            st.error("Please Log in first")
        else:
            training_page()
    elif x == "Make Dataset":
        if "login_information" not in st.session_state.keys():
            st.error("Please Log in first")
        else:
            dataset()
    else:
        if "login_information" not in st.session_state.keys():
            st.error("Please Log in first")
        else:
            past_training_page()
container()