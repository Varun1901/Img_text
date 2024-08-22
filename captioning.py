import requests
import streamlit as st
import base64

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Background image setup
img = get_img_as_base64("bg.jpg")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
}}
[data-testid="stHeader"] {{
background: rgba(0, 0, 0, 0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}

def query(file_bytes):
    response = requests.post(API_URL, headers=headers, data=file_bytes)
    return response.json()

# File uploader and button
uploaded_file = st.file_uploader("Upload your image", type="jpg")
if st.button("Generate"):
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        result = query(file_bytes)
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.write(result)
    else:
        st.error("Please upload an image file.")
