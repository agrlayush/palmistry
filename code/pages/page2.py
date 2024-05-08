import streamlit as st
from read_palm import main

import cv2
import numpy as np
file_location = "input/"


# st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center'>Capture a Photo", unsafe_allow_html=True)
st.header('', divider='rainbow')
picture = st.camera_input("Take a picture of you palm:")
filename = "hand.jpg"
if picture:
    with open (file_location + filename,'wb') as file:
          file.write(picture.getbuffer())

    length = main(filename, "streamlit")

    if length == None:
        st.write("Palm lines not properly detected! Please use another palm image.")
    else:
        # st.write(length)
        if st.button("Send to AI Astrologer", type="primary"):
            st.switch_page("pages/page3.py")
        # st.page_link("pages/page3.py", label="Send to AI Astrologer", use_container_width=True)
        # st.link_button("Send to AI Astrologer", "pages/page3.py")
        # st.page_link("pages/page3.py", "Send to AI Astrologer")
        # print(length)
        prompt = "afjoafewfafaefaef"

        # //call bedrock
        # get predictions
        # generate audio
        # generate Video
        # redirect to next page
        # st.page_link("pages/page2.py", See Pre)



# if st.button('Open Camera'):
#     picture = st.camera_input("Take a picture of you palm")
	
# picture = st.camera_input("Take a picture of you palm")

#st. set_page_config(layout="wide") // in case you need wide screen layout

# For Camera Feed
# picture = st.camera_input("Take a picture of you palm")

#For Upload Files
# img_file_buffer = st.file_uploader("Upload an image of you palm", type=["png", "jpg", "jpeg"])



