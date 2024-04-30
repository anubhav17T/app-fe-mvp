import uuid
import streamlit as st
import requests
from src.helper.endpoint import COMPLETED_TRAINING_JOBS

if "inference" not in st.session_state:
    st.session_state["inference"] = {}

if "training_info" not in st.session_state:
    st.session_state["training_info"] = {}


def model():
    # Just for demonstration, replace with your actual model
    # check for training jobs that have been completed + appended with custom inference
    response = requests.get(COMPLETED_TRAINING_JOBS.format(
        st.session_state["login_information"]["response_data"]["data"]["id"]))

    if response.status_code == 422:
        st.error("Internal Server Error")
    elif response.status_code != 200:
        st.error("Internal Server Error")
    x = response.json()
    model_ = ["PreBuilt_v1"]
    if len(x["data"]) == 0:
        return model_
    else:
        for i in x["data"]:
            model_.append(i["?column?"])
            st.session_state["training_info"].update({i["?column?"]: i["id"]})
        return model_


@st.cache_data
def inference_on_trained_model(message, training_id):
    random_uuid = uuid.uuid4()
    uuid_string = str(random_uuid).replace('-', '')
    random_string = uuid_string[:12]
    response = requests.post("https://mlbe.rekogniz.com/v1/concept/",
                             json={"id": str(st.session_state["login_information"]["response_data"]["data"]["id"]),
                                   "training_id": training_id,
                                   "request_id": random_string,
                                   "inference_schema": {"prompt": message,
                                                        "negative_prompt": "",
                                                        "resolution": "1024"
                                                        }
                                   }, verify=False)
    if response.status_code == 422:
        st.error("Internal Server Error")
    elif response.status_code != 200:
        st.error("Internal Server Error")
    x = response.json()
    data = x["data"]["image_path"]
    if data:
        st.session_state["inference"].update({random_string: {"message": message,
                                                              "images": data
                                                              }})
    return data


@st.cache_data
def make_inference(message):
    random_uuid = uuid.uuid4()
    uuid_string = str(random_uuid).replace('-', '')
    random_string = uuid_string[:12]
    response = requests.post("https://mlbe.rekogniz.com/v1/inference/",
                             json={"id": str(st.session_state["login_information"]["response_data"]["data"]["id"]),
                                   "request_id": random_string,
                                   "inference_schema": {"prompt": message,
                                                        "negative_prompt": "",
                                                        "resolution": "1024"
                                                        }
                                   }, verify=False)
    if response.status_code == 422:
        st.error("Internal Server Error")
    elif response.status_code != 200:
        st.error("Internal Server Error")
    x = response.json()
    data = x["data"]["image_path"]
    if data:
        st.session_state["inference"].update({random_string: {"message": message,
                                                              "images": data
                                                              }})
    return data


def inference():
    # Create or get session state
    if "login_information" not in st.session_state.keys():
        st.error("Please login to continue")
        btn = st.button("Login ✅")
        if btn:
            st.switch_page("pages/2_📲_Login.py")
    else:
        select = st.selectbox(label="Select Model", options=model(), help="Model")
        print(select)
        if select:
            with st.expander("Image Generation", expanded=False):
                # Implementation of chat goes here
                message = st.text_input("Type your message here", "")
                if st.button("Send", key="send_button"):
                    # Here you can include the logic for your model to respond to the user's message
                    if len(message) == 0:
                        st.error("Please type some inference")
                        st.stop()
                    with st.spinner("Generating images..."):
                        progress_bar = st.progress(0)
                        if select == "PreBuilt_v1":
                            data = make_inference(message=message)
                            if data:
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.image(data[0], caption='Image 1')
                                with col2:
                                    st.image(data[1], caption='Image 2')
                                with col3:
                                    st.image(data[2], caption='Image 2')
                            progress_bar.progress(100)
                        else:
                            # trainined models
                            inferred_data = inference_on_trained_model(message=message, training_id=st.session_state["training_info"][select])
                            if inferred_data:
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.image(inferred_data[0], caption='Image 1')
                                with col2:
                                    st.image(inferred_data[1], caption='Image 2')
                                with col3:
                                    st.image(inferred_data[2], caption='Image 2')
                            progress_bar.progress(100)
        st.subheader("History:")
        for key, value in st.session_state["inference"].items():
            st.write("<span style='color:#FF69B4'>{}</span>".format(value["message"]), unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            for idx, image_path in enumerate(value["images"]):
                if idx % 3 == 0:
                    with col1:
                        st.image(image_path, caption=f"Image {idx + 1}", width=320)
                elif idx % 3 == 1:
                    with col2:
                        st.image(image_path, caption=f"Image {idx + 1}", width=320)
                else:
                    with col3:
                        st.image(image_path, caption=f"Image {idx + 1}", width=320)


inference()
