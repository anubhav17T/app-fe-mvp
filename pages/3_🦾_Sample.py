import uuid
import streamlit as st
from streamlit_card import card
import requests
import os
import base64
import runpod
current_directory = os.getcwd()
runpod.api_key = "6MRIL8BDMAUTBIMX6JGVOGJCMGR32PYXI7MHR229"


def pod_address():
    pods = runpod.get_pods()
    """This function fetch runpod ip address """
    add = {}
    for pod in pods:
        if 'runtime' in pod and pod['runtime']:
            for port in pod['runtime']['ports']:
                if port['privatePort'] == 8002:
                    add.update({"training": f"{port['ip']}:{port['publicPort']}"})
                elif port['privatePort'] == 8003:
                    add.update({"demo": f"{port['ip']}:{port['publicPort']}"})
    if not add:
        return {"service": "down"}
    return add


@st.cache_data
def make_inference(message, api_type):
    random_uuid = uuid.uuid4()
    uuid_string = str(random_uuid).replace('-', '')
    random_string = uuid_string[:12]
    address = pod_address()
    if "demo" not in address.keys():
        st.error("Service is not available,please try again later")
        st.stop()
    else:
        machine_learning_pod_address = address["demo"]
        response = requests.post(f"http://{machine_learning_pod_address}/v1/demo/{api_type}",
                                 headers={
                                     "verification-key": "cmVrb0duaXpUZWNobm9sb2dpZXNQcmlWYVRlTGlNZXRlZCMjIzEyMzQwOTY4OTY="},
                                 json={"id": str(st.session_state["login_information"]["response_data"]["data"]["id"]),
                                       "request_id": random_string,
                                       "inference_schema": {"prompt": message,
                                                            "negative_prompt": "",
                                                            "resolution": "512"
                                                            }
                                       }, verify=False)
        st.info(response.status_code)
        if response.status_code == 422:
            st.error("Something went wrong at our end, please try again later")
            return False
        elif response.status_code != 200:
            st.error("Something went wrong at our end, please try again later")
            return False
        x = response.json()
        data = x["data"]["image_path"]
        if data:
            st.session_state["inference"].update({random_string: {"message": message,
                                                                  "images": data
                                                                  }})
        return data


def sample():
    if "login_information" not in st.session_state.keys():
        st.error("Please Login First")
        login = st.button("Login ✅", help="Login first")
        if login:
            st.switch_page("pages/2_📲_Login.py")
    else:
        # Sample data for cards with local image paths
        card_data = [current_directory + "/pages/output-lens.jpeg",
                     current_directory + "/pages/headphone3.png",
                     current_directory + "/pages/sample_1.png",
                     current_directory + "/pages/watches2.png",
                     ]

        st.subheader("Pre-Trained Examples")
        with open(card_data[0], "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data)
        with open(card_data[1], "rb") as f:
            data = f.read()
            encoded_headphone = base64.b64encode(data)
        with open(card_data[2], "rb") as f:
            data = f.read()
            encoded_shoes = base64.b64encode(data)
        with open(card_data[3], "rb") as f:
            data = f.read()
            encoded_watch = base64.b64encode(data)
        lens_data = "data:image/png;base64," + encoded.decode("utf-8")
        headphone_data = "data:image/png;base64," + encoded_headphone.decode("utf-8")
        shoes_data = "data:image/png;base64," + encoded_shoes.decode("utf-8")
        watches_data = "data:image/png;base64," + encoded_watch.decode("utf-8")

        col1,col2 = st.columns(2)
        with col1:
            lensCard = card(
                title="",
                text="Eyeglasses",
                image=lens_data)
            if lensCard:
                lens = st.text_input("Type your prompt here", "", key="lens")
                if st.button("Send", key="send_button0"):
                    if len(lens) == 0:
                        st.error("Please type some inference")
                        st.stop()
                    with st.spinner("Generating images..."):
                        progress_bar = st.progress(0)
                        data = make_inference(message=lens, api_type="glasses")
                        if data:
                            st.image(data[0], caption='Image 1')
                            st.image(data[1], caption='Image 2')
                            st.image(data[2], caption='Image 2')
                        progress_bar.progress(100)

            shoeCard = card(
                title="",
                text="Shoes",
                image=shoes_data)
            if shoeCard:
                shoe = st.text_input("Type your prompt here", "", key="shoe")
                if st.button("Send", key="send_button2"):
                    if len(shoe) == 0:
                        st.error("Please type some inference")
                        st.stop()
                    with st.spinner("Generating images..."):
                        progress_bar = st.progress(0)
                        data = make_inference(message=shoe, api_type="shoes")
                        if data:
                            st.image(data[0], caption='Image 1')
                            st.image(data[1], caption='Image 2')
                            st.image(data[2], caption='Image 2')
                        progress_bar.progress(100)

        with col2:
            headphoneCard = card(
                title="",
                text="Headphone",
                image=headphone_data)
            if headphoneCard:
                headphone = st.text_input("Type your prompt here", "", key="headphone")
                if st.button("Send", key="send_button1"):
                    if len(headphone) == 0:
                        st.error("Please type some inference")
                        st.stop()
                    with st.spinner("Generating images..."):
                        progress_bar = st.progress(0)
                        data = make_inference(message=headphone, api_type="headphone")
                        if data:
                            st.image(data[0], caption='Image 1')
                            st.image(data[1], caption='Image 2')
                            st.image(data[2], caption='Image 2')
                        progress_bar.progress(100)

            watchesCard = card(
                        title="",
                        text="Watch",
                        image=watches_data)
            if watchesCard:
                watch = st.text_input("Type your prompt here", "", key="watch")
                if st.button("Send", key="send_button3"):
                    if len(watch) == 0:
                        st.error("Please type some inference")
                        st.stop()
                    with st.spinner("Generating images..."):
                        progress_bar = st.progress(0)
                        data = make_inference(message=watch, api_type="watch")
                        if data:
                            st.image(data[0], caption='Image 1')
                            st.image(data[1], caption='Image 2')
                            st.image(data[2], caption='Image 2')
                        progress_bar.progress(100)

sample()
