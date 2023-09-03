from processors import TableProcessor, textprocessor, ImageProcessor

def get_processor(uploaded_file):
    if uploaded_file.type == "application/vnd.ms-excel":
        return TableProcessor(uploaded_file)

    elif uploaded_file.type == "text/plain":
        textprocessor.add_file(uploaded_file)
        return textprocessor

    elif uploaded_file.type.startswith("image"):
        return ImageProcessor(uploaded_file)

    else:
        print(uploaded_file.type)
        textprocessor.add_file(uploaded_file)
        return textprocessor