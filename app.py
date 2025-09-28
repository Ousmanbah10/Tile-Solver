# app.py
import streamlit as st
from PIL import Image
from utils import split_image, pil_to_base64
from manual_play import manual_play


st.set_page_config(page_title="Tile Solver Game", layout="centered")
st.title("🧩 Tile Solver Game")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

st.write("--------------")

st.title("Uploaded Photo")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    display_image = image.resize((300, 300))
    
    # Center the image using columns
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(display_image)
        
    grid_size = 3

    manual_play(grid_size)
    
    