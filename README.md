# Augmentify

# data_frame = pd.read_csv(uploaded_file)
	        # augmented_data = augment_tabular_data(data_frame)
	        # st.write(augmented_data)

	        # # Provide a download link for augmented data (CSV)
	        # csv = augmented_data.to_csv(index=False)
	        # b64 = base64.b64encode(csv.encode()).decode()
	        # st.markdown('### **Download Augmented Data (CSV)**')
	        # href = f'<a href="data:file/csv;base64,{b64}" download="augmented_data.csv">Click here to download</a>'
	        # st.markdown(href, unsafe_allow_html=True) 
	        # text = uploaded_file.read().decode("utf-8")
	        # augmented_text = augment_text(text)
	        # st.write(augmented_text)

	        # # Provide a download link for augmented data (text)
	        # st.markdown('### **Download Augmented Data (Text)**')
	        # href = f'<a href="data:text/plain;charset=utf-8,{augmented_text}" download="augmented_text.txt">Click here to download</a>'
	        # st.markdown(href, unsafe_allow_html=True)
	        # image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

	        # # Create a temporary directory to store augmented images
	        # with tempfile.TemporaryDirectory() as temp_dir:
	        #     augmented_images = []
	        #     for i in range(num_data_to_generate):
	        #         augmented_image = augment_image(image)
	        #         output_path = os.path.join(temp_dir, f"augmented_image_{i}.jpg")
	        #         cv2.imwrite(output_path, augmented_image)
	        #         augmented_images.append(output_path)

	        #     # Check if there are augmented images to include in the zip file
	        #     if augmented_images:
	        #         # Create a zip file with augmented images
	        #         zip_filename = "augmented_images.zip"
	        #         with zipfile.ZipFile(zip_filename, "w") as zipf:
	        #             for img_path in augmented_images:
	        #                 zipf.write(img_path, os.path.basename(img_path))

	        #         # Provide a download link for the zip file
	        #         st.markdown(f'### **Download Augmented Images as a Zip Folder**')
	        #         href = f'<a href="{zip_filename}" download="{zip_filename}">Click here to download</a>'
	        #         st.markdown(href, unsafe_allow_html=True)
	        #     else:
	        #         st.markdown("No augmented images to download.")
