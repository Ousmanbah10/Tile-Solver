import streamlit as st
from PIL import Image

# Set page title and layout
st.set_page_config(page_title="Tile Solver Game", layout="centered")

# Title
st.title("🧩 Tile Solver Game")

# Welcome message
st.write("Welcome to our Tile Solver game! 🎉")
st.write("Here you’ll be able to split images into tiles, play the puzzle, and even solve it automatically using A*.")

uploaded_file = st.file_uploader("Upload an image",type=["jpg","jpeg","png"])

def split_image(image, grid_size=3):
    width,height =image.size 
    tile_width=width //grid_size
    tile_height= height //grid_size

    tiles=[]
    for row in range(grid_size):
        for col in range(grid_size):
            left =col*tile_width
            upper=row*tile_height
            right= (col+1)* tile_width
            lower=(row+1)* tile_height
            tile=image.crop((left,upper,right,lower))
            tiles.append(tile)
    return tiles

if uploaded_file is not None:
    image= Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_container_width=True)

    tiles=split_image(image,grid_size=3)

    st.write("Here is your puzzle")
    for i in range(0,9,3):
        cols=st.columns(3)
        for j in range(3):
            cols[j].image(tiles[i+j],use_container_width=True)
