import streamlit as st
from streamlit import cache_data

st.title("Caching data")


@st.cache_data
def cache_this_function():
    import time
    time.sleep(5)
    return "OUT"


button = st.button("Test Cache")
if button:
    out = cache_this_function()
    st.write(out)
