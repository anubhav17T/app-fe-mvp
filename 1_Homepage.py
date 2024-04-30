import streamlit as st


def main():
    st.set_page_config(page_title="Personalisation",
                       page_icon="🧊",
                       initial_sidebar_state="expanded",
                       layout="wide"
                       )

    st.markdown("<h1 style='color: #FF69B4;'>Rekogniz - Text2Image Personalisation</h1>", unsafe_allow_html=True)

    # Greetings
    st.subheader("Greetings!")
    st.info('''Welcome to our company's page. We're glad to have you here!''', icon="🤖")
    st.warning("This product is still under development,Feel free to reach out or raise concerns at "
               "anubhav.tyagi@rekogniz.com")
    st.subheader("About Us")
    st.success(
        "We are group of individuals having combined experience of more than 12+ years across software technology,"
        " Join us in revolutionizing Subject Driven Content Generation")

    # image_urls = [
    #     "https://cdn.britannica.com/05/236505-050-17B6E34A/Elon-Musk-2022.jpg",
    #     "https://cdn.britannica.com/05/236505-050-17B6E34A/Elon-Musk-2022.jpg",
    #     "https://cdn.britannica.com/05/236505-050-17B6E34A/Elon-Musk-2022.jpg"
    # ]
    #
    #
    # # Display images in columns
    # col1, col2 = st.columns(2)
    #
    # with col1:
    #     st.image("https://cdn.britannica.com/05/236505-050-17B6E34A/Elon-Musk-2022.jpg", caption='Image 1',width=400)
    #
    # with col2:
    #     st.image("https://cdn.britannica.com/05/236505-050-17B6E34A/Elon-Musk-2022.jpg", caption='Image 3',width=400)

    # Training Steps
    st.subheader("Training Steps")
    st.write("Here are the steps to get started with our training program:")
    st.markdown("<span style='color: #008000;'>1. Sign up/Log in on the website.</span>",
                unsafe_allow_html=True)
    st.markdown(
        "<span style='color: #FFA500;'>2. Go to training page in sidebar, provide your product images and wait 7-10 minutes.</span>",
        unsafe_allow_html=True)
    st.markdown(
        "<span style='color: #0000FF;'>3. Upon finishing the training you'll receive confirmation email.</span>",
        unsafe_allow_html=True)
    st.markdown(
        "<span style='color: #800080;'>4. Start inferencing,personalisation catered for you on demand.</span>",
        unsafe_allow_html=True)


if __name__ == "__main__":
    main()
