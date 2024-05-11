import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
# st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center'>Welcome to AI Astrologer</h2>", unsafe_allow_html=True)
st.header('', divider='rainbow')

st.image('palmistry.jpeg', caption='')
st.write("One of the most well-known aspects of palmistry is the interpretation of palm lines. These lines, also known as creases or folds, provide significant information about a person's life, relationships and destiny. The primary lines used in palm reading include the life line, heart line and head line. Let's explore each of these lines with us:")

col1, col2, col3 = st.columns([1, 1, 1])

# col2.button("Open Camera To Start", type="primary")

# col2.page_link("pages/page2.py", label="Open Camera to Start", use_container_width=True)
if col2.button("Open Camera to Start", type="primary"):
    st.switch_page("pages/page2.py")
