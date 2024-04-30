import streamlit as st

#title
st.title("Main Application")

st.header("This is Header")

st.subheader("This is subheader")

#Markdown
st.markdown("This is markdown **text**")

st.markdown("# Header1")
st.markdown("## Header 2")

st.latex("y=mx+c2")
st.caption("caption")

st.code("""import pandas as pd""")

#preformated text
st.text("Text above divide")
st.divider()
st.text("Text below divider")


st.write("")







#Buttons

primary_btn = st.button(label="Primary",type="primary")
secondary_btn = st.button(label="second",type="secondary")

if primary_btn:
    st.write("Hello primary")
if secondary_btn:
    st.write("Hello from secondary")


#checkbox
st.divider()

checkbox = st.checkbox("Remember me")
if checkbox:
    st.write("will remember you")

st.divider()

#radio button
radio = st.radio("Choose somethins",options=["1","2","3"],horizontal=True)
if radio=="1":
    st.write("radio button 1")

st.divider()

select = st.selectbox("How would you like to be contacted",options=["Email","Phone","Personal"])

st.divider()


#multiselect

multiselect = st.multiselect("Choose as many columns",options=["email","phone","personal"],default=["email"],max_selections=2)
st.write(multiselect)

st.divider()

slider = st.slider("Pick number",min_value=0,max_value=10,step=1)
st.write("You have selected currently",slider)

start_color, end_color = st.select_slider(
    'Select a range of color wavelength',
    options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'],
    value=('red', 'blue'))
st.write('You selected wavelengths between', start_color, 'and', end_color)

st.divider()

#text_input


input_ = st.text_input("What is your name",placeholder="John Doe")
st.write("Your name is {}".format(input_))

st.divider()

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable text input widget", key="disabled")
    st.radio(
        "Set text input label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )
    st.text_input(
        "Placeholder for the other text input widget",
        "This is a placeholder",
        key="placeholder",
    )

with col2:
    text_input = st.text_input(
        "Enter some text 👇",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder,
    )

    if text_input:
        st.write("You entered: ", text_input)


st.divider()

tell_me = st.text_area("Your feedbacks",height=200,placeholder="Type your feedback here")

st.divider()


with st.form("form_key"):
    st.write("What would like to order")
    appetizer = st.selectbox("Appetizers", options=["choice1", "choice2", "choice3"])
    main = st.selectbox("Main course", options=["choice1", "choice2", "choice3"])
    dessert = st.selectbox("Dessert", options=["choice1", "choice2", "choice3"])

    wine = st.checkbox("Are you bringing wine?")

    visit_date = st.date_input("When are you coming?")

    visit_time = st.time_input("At what time are you coming?")

    allergies = st.text_area("Any allergies?", placeholder="Leave us a note for allergies")

    submit_btn = st.form_submit_button("Submit")

st.write(f"""Your order summary:

Appetizer: {appetizer}

Main course: {main}

Dessert: {dessert}

Are you bringing your own wine: {"yes" if wine else "no"}

Date of visit: {visit_date}

Time of visit: {visit_time}

Allergies: {allergies}
""")


st.divider()

with st.sidebar:
    r1 = st.radio("Choose",options=["n","a","b"],horizontal=False)


st.divider()



c1,c2,c3 = st.columns(3)
c1.write("this is columns 1")
slider = c2.slider(label="chose number",min_value=0,max_value=10)
c3.write(slider)


st.divider()

tab1,tab2 = st.tabs(["Line Plot","Bar Plot"])

with tab1:
    st.write("Tab1")
with tab2:
    st.write("Tab2")


st.divider()

#container
#adjust and hold multiple elements together in same format
import numpy as np

with st.container():
   st.write("This is inside the container")

   # You can call any Streamlit command, including custom components:
   st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container")
