# from processors import *
import streamlit as st
import pandas as pd
import selector

st.title("Augmentify - Data Augmentation App")


uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt", "jpg", "png"])

# Input field for specifying the quantity of data to generate
# num_data_to_generate = st.number_input(
#     "Number of Data Points/Images to Generate", min_value=1, value=5
# )

"""
Processing an uploaded file follows these three steps:

- checking what file type was uploaded:
    - excel / csv
    - image
    - text

- selecting an augment processor based on file type og uploaded image

- providing a download link to download augmented data

"""

if uploaded_file:
    # select  processor
    processor = selector.get_processor(uploaded_file)
    print(processor.processes.generators)
    # run processor
    result = processor.run_augmentation()
    # csv and text data should be displayed on web app
    # using streamlite write function
    # images cannot be writeable
    if result.is_writeable:
        st.write(result.content)


    # provide download link
    st.markdown(" ### ***Download Augmented Data*** ")
    download_link = result.get_download_link()
    if download_link is None:
        st.markdown("No augmented data to download")
