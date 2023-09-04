# # from processors import *
# import streamlit as st
# import pandas as pd
# import selector

# st.title("Augmentify - Data Augmentation App")


# uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt", "jpg", "png"])

# # Input field for specifying the quantity of data to generate
# # num_data_to_generate = st.number_input(
# #     "Number of Data Points/Images to Generate", min_value=1, value=5
# # )

# """
# Processing an uploaded file follows these three steps:

# - checking what file type was uploaded:
#     - excel / csv
#     - image
#     - text

# - selecting an augment processor based on file type og uploaded image

# - providing a download link to download augmented data

# """

# if uploaded_file:
#     # select  processor
#     processor = selector.get_processor(uploaded_file)
#     print(processor.processes.generators)
#     # run processor
#     result = processor.run_augmentation()
#     # csv and text data should be displayed on web app
#     # using streamlite write function
#     # images cannot be writeable
#     if result.is_writeable:
#         st.write(result.content)


#     # provide download link
#     st.markdown(" ### ***Download Augmented Data*** ")
#     download_link = result.get_download_link()
#     if download_link is None:
#         st.markdown("No augmented data to download")
#     else:
        
import streamlit as st
import pandas as pd
import random
import nltk
from nltk.corpus import wordnet
import cv2
import numpy as np
import base64
import os
import shutil
import zipfile
import tempfile

st.title("Data Augmentation App")

def augment_text(text, synonym_replacement_prob=0.1):
    words = text.split()
    augmented_words = []

    for word in words:
        if random.random() < synonym_replacement_prob:
            synonyms = wordnet.synsets(word)
            if synonyms:
                synonym = random.choice(synonyms).lemmas()[0].name()
                word = synonym
        augmented_words.append(word)

    augmented_text = ' '.join(augmented_words)
    return augmented_text

def augment_tabular_data(data_frame, noise_std=0.1):
    augmented_data = data_frame.copy()
    numeric_columns = augmented_data.select_dtypes(include=['number']).columns

    for column in numeric_columns:
        augmented_data[column] += np.random.normal(0, noise_std, size=len(augmented_data))

    return augmented_data

def augment_image(image, rotation_angle=30):
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, random.uniform(-rotation_angle, rotation_angle), 1.0)
    augmented_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    
    return augmented_image

uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt", "jpg", "png"])

# Input field for specifying the quantity of data to generate
num_data_to_generate = st.number_input("Number of Data Points/Images to Generate", min_value=1, value=5)

if uploaded_file:
    if uploaded_file.type == "application/vnd.ms-excel":  # CSV
        data_frame = pd.read_csv(uploaded_file)
        augmented_data = augment_tabular_data(data_frame)
        st.write(augmented_data)

        # Provide a download link for augmented data (CSV)
        csv = augmented_data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown('### **Download Augmented Data (CSV)**')
        href = f'<a href="data:file/csv;base64,{b64}" download="augmented_data.csv">Click here to download</a>'
        st.markdown(href, unsafe_allow_html=True)
    elif uploaded_file.type.startswith("text"):  # Text
        text = uploaded_file.read().decode("utf-8")
        augmented_text = augment_text(text)
        st.write(augmented_text)

        # Provide a download link for augmented data (text)
        st.markdown('### **Download Augmented Data (Text)**')
        href = f'<a href="data:text/plain;charset=utf-8,{augmented_text}" download="augmented_text.txt">Click here to download</a>'
        st.markdown(href, unsafe_allow_html=True)
    elif uploaded_file.type.startswith("image"):  # Image
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Create a temporary directory to store augmented images
        with tempfile.TemporaryDirectory() as temp_dir:
            augmented_images = []
            for i in range(num_data_to_generate):
                augmented_image = augment_image(image)
                output_path = os.path.join(temp_dir, f"augmented_image_{i}.jpg")
                cv2.imwrite(output_path, augmented_image)
                augmented_images.append(output_path)

            # Check if there are augmented images to include in the zip file
            if augmented_images:
                # Create a zip file with augmented images
                zip_filename = "augmented_images.zip"
                with zipfile.ZipFile(zip_filename, "w") as zipf:
                    for img_path in augmented_images:
                        zipf.write(img_path, os.path.basename(img_path))

                # Provide a download link for the zip file
                st.markdown(f'### **Download Augmented Images as a Zip Folder**')
                href = f'<a href="{zip_filename}" download="{zip_filename}">Click here to download</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.markdown("No augmented images to download.")
