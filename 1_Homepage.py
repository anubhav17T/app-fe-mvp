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

    with st.expander("Expand to show some usecases"):
        st.info("The actual generated images are much clear and concise.Images Mentioned here are just for reference!")
        col1, col2 = st.columns(2)
        with col1:
            st.image("img/sample_2 (15).png", caption='Tshirt taken from zara',width=600,clamp=True)
            st.image("img/sample_0 (10).png", caption='Tshirt taken from zara',width=450)
            st.image("img/sample_1 (26).png", caption='Tshirt taken from zara',width=250)
        with col2:
            st.image("img/lens.png", caption='Glasses taken from Lenskart',width=450)
            st.image("img/lens1.png", caption='Glasses taken from Lenskart',width=250)
            st.image("img/lens3.png", caption='Glasses taken from Lenskart',width=250)

    st.subheader("Journey so far ...")

    st.success("Jan - Mar 2024")
    st.write("🧑‍🤝‍🧑 Team Building ✅")
    st.write("🏃 Research and Development on Custom Diffusion models ✅")
    st.write("🧑🏼‍💻 Prototyping and Idea Validation ✅")
    st.write("🤦 Legal and Regulatory Compliance ✅")

    st.success("Apr - May 2024")
    st.write("🤖 MVP Development ⏳")
    st.write("💵 Fundraising ⏳")
    st.divider()
    st.subheader("Contact Details")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Reach us at anubhav.tyagi@rekogniz.com or aishwary@rekogniz.com ")
        st.info("Address - Vinishma Tower, Shahpur Jat, 110049, New Delhi")


if __name__ == "__main__":
    main()
