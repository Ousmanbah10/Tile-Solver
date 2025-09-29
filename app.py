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

     # Initialize session state
    if "backend_matrix" not in st.session_state:
        tiles, labels = split_image(image, grid_size)
        labels[-1] = None  # blank tile
        tiles[-1] = None
        backend_matrix = [labels[i:i+grid_size] for i in range(0, len(labels), grid_size)]
        
        # Save both tile objects and base64-encoded versions
        st.session_state.tiles = tiles
        st.session_state.tile_b64 = [pil_to_base64(t) if t else None for t in tiles]
        st.session_state.backend_matrix = backend_matrix
  
 
    manual_play(grid_size)
    
    