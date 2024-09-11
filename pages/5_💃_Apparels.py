import uuid
import streamlit as st
import requests

from src.helper.endpoint import IMAGE_UPLOAD_ENDPOINT


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
        return {"success": True, "data": x}


def fashion_model_try():
    if "login_information" not in st.session_state.keys():
        st.error("Please login to continue")
        btn = st.button("Login ✅")
        if btn:
            st.switch_page("pages/2_📲_Login.py")
    else:
        select = st.selectbox(label="Select Generation Type",
                              options=["Simple Clothes", "Background Replacement", "Printed Clothes"],
                              help="Model")
        if select == "Simple Clothes":
            with st.form("Apparel Try On"):
                col1, col2 = st.columns(2)
                # Text input for training job name
                with col1:
                    outfit_type = st.selectbox(label="Select Outfit Type", options=["Tshirt", "Skirt"],
                                               help="type of outfit")
                    ethnicity = st.selectbox(label="Select Model Ethnicity", options=["African", "American", "Asian"])
                with col2:
                    garment_type = st.text_input("Garment Type",
                                                 placeholder="a background with pebblles and mountain",
                                                 help="What you want to generate in background")
                    images = st.file_uploader("Upload Images", accept_multiple_files=True,
                                              type=['png', 'jpg', 'jpeg'],
                                              help="Please provide 1 images of your outfit")

                sub = st.form_submit_button("Apparel Try On")
                if sub:
                    if outfit_type is None or ethnicity is None or garment_type is None:
                        st.error("Please provide data")
                        st.stop()
                    else:
                        file_names = {}
                        for file in images:
                            file_names[f"files"] = (file.name, file.getvalue(), file.type)
                        upload = image_upload(file_names)
                        if not upload["success"]:
                            st.error("Something went wrong please try again later")
                            st.stop()
                        print(upload["data"]["s3_uri"])
                        response = requests.post("http://194.68.245.64:22095/v1/upper-body/simple/cloth",
                                                 headers={
                                                     "verification-key": "cmVrb0duaXpUZWNobm9sb2dpZXNQcmlWYVRlTGlNZXRlZCMjIzEyMzQwOTY4OTY="},
                                                 json={"id": str(
                                                     st.session_state["login_information"]["response_data"]["data"][
                                                         "id"]),
                                                     "s3_path": upload["data"]["s3_uri"],
                                                     "prompt": garment_type,
                                                     "model_path": "s3://rekogniz-training-data/fashion_models/western/male",
                                                 }, verify=False)
                        if response.status_code == 422:
                            st.error("Something went wrong at our end, please try again later")
                            return False
                        elif response.status_code != 200:
                            st.error("Something went wrong at our end, please try again later")
                            return False
                        x = response.json()
                        data = x["data"]["image_path"]
                        col1, col2 = st.columns(2)
                        print(x)
                        with col1:
                            st.image(images)
                        with col2:
                            st.image(data)

        elif select == "Printed Clothes":
            with st.form("Printed clothes Try On"):
                col1, col2 = st.columns(2)
                with col1:
                    ethnicity = st.selectbox(label="Select Model Ethnicity", options=["American", "Asian"])
                    prompt = "a photography of a model"
                with col2:
                    images = st.file_uploader("Upload Images", accept_multiple_files=True,
                                              type=['png', 'jpg', 'jpeg'],
                                              help="Please provide 1 images of your outfit")

                sub = st.form_submit_button("Printed clothes Try On")
                if sub:
                    if ethnicity is None:
                        st.error("Please provide data")
                        st.stop()
                    else:
                        file_names = {}
                        for file in images:
                            file_names[f"files"] = (file.name, file.getvalue(), file.type)
                        upload = image_upload(file_names)
                        if not upload["success"]:
                            st.error("Something went wrong please try again later")
                            st.stop()
                        print(st.session_state["login_information"]["response_data"]["data"]["id"])
                        response = requests.post("http://194.68.245.64:22095/v1/upper-body/designer/cloth",
                                                 headers={
                                                     "verification-key": "cmVrb0duaXpUZWNobm9sb2dpZXNQcmlWYVRlTGlNZXRlZCMjIzEyMzQwOTY4OTY="},
                                                 json={"id": str(
                                                     st.session_state["login_information"]["response_data"]["data"][
                                                         "id"]),
                                                     "s3_path": upload["data"]["s3_uri"],
                                                     "prompt": prompt,
                                                 }, verify=False)
                        if response.status_code == 422:
                            st.error("Something went wrong at our end, please try again later")
                            return False
                        elif response.status_code != 200:
                            st.error("Something went wrong at our end, please try again later")
                            return False
                        x = response.json()
                        print(x)
                        data = x["data"]["image_path"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.image(images)
                        with col2:
                            st.image(data)

        elif select == "Background Replacement":
            with st.form("Start Background Replacement"):
                col1, col2 = st.columns(2)
                # Text input for training job name
                with col1:
                    object_type = st.text_input("Object Type", placeholder="headphone", help="Type of the object")
                    object_text = st.selectbox("Text in object", options=[False, True],
                                               help="Does your product consist of text?")
                with col2:
                    background_prompt = st.text_input("Background Prompt",
                                                      placeholder="a background with pebblles and mountain",
                                                      help="What you want to generate in background")
                    images = st.file_uploader("Upload Images", accept_multiple_files=True,
                                              type=['png', 'jpg', 'jpeg'], help="Please provide 1 images")

                submit_ = st.form_submit_button("Start Background Replacement")
                if submit_:
                    if object_type is None:
                        st.error("Please provide object type")
                        st.stop()
                    elif background_prompt is None:
                        st.error("Please provide object type")
                        st.stop()
                    file_names = {}
                    for file in images:
                        file_names[f"files"] = (file.name, file.getvalue(), file.type)
                    upload = image_upload(file_names)
                    if not upload["success"]:
                        st.error("Something went wrong please try again later")
                        st.stop()
                    response = requests.post("http://216.48.187.54:8002/v1/custom_background",
                                             headers={
                                                 "verification-key": "cmVrb0duaXpUZWNobm9sb2dpZXNQcmlWYVRlTGlNZXRlZCMjIzEyMzQwOTY4OTY="},
                                             json={"id": str(
                                                 st.session_state["login_information"]["response_data"]["data"]["id"]),
                                                 "s3_path": upload["data"]["s3_uri"],
                                                 "prompt": object_type,
                                                 "bg_prompt": background_prompt,
                                                 "superimpose": object_text
                                             }, verify=False)
                    if response.status_code == 422:
                        st.error("Something went wrong at our end, please try again later")
                        return False
                    elif response.status_code != 200:
                        st.error("Something went wrong at our end, please try again later")
                        return False
                    x = response.json()
                    data = x["data"]["image_path"]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(images, caption=background_prompt)
                    with col2:
                        st.image(data[0], caption=background_prompt)


fashion_model_try()
