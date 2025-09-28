import streamlit as st
import base64
from io import BytesIO
from utils import get_neighbors, is_solved, shuffle_board
from a_star import solve_with_astar

def pil_to_base64(img):
    """Convert PIL image to base64 string for HTML embedding."""
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def manual_play(grid_size=3):
    """Render the puzzle sections: Shuffle, A*, and Manual controls."""

    backend_matrix = st.session_state.backend_matrix
    tiles = st.session_state.tiles

    # 1. SHUFFLE SECTION
    st.subheader("🔀 SHUFFLE")
    
    # Display puzzle
    grid_html = f'''
    <div style="
        display: flex; 
        justify-content: center; 
        align-items: center; 
        width: 100%; 
        margin: 20px 0;
    ">
        <div style="
            display: grid; 
            grid-template-columns: repeat({grid_size}, 100px); 
            grid-gap: 2px;
        ">
    '''
    for r in range(grid_size):
        for c in range(grid_size):
            val = backend_matrix[r][c]
            if val is None:
                grid_html += '<div style="width:100px; height:100px; background:#fff; border:1px solid #ccc;"></div>'
            else:
                img_b64 = pil_to_base64(tiles[val - 1])
                grid_html += f'<div style="width:100px; height:100px;"><img src="data:image/png;base64,{img_b64}" style="width:100%; height:100%; object-fit:cover;"></div>'
    grid_html += '</div></div>'
    st.markdown(grid_html, unsafe_allow_html=True)
    
    # Shuffle controls
    shuffle_count = st.slider("Number of shuffles", 1, 20, 10) 
    if st.button("🔀 Shuffle Now"):
        st.session_state.backend_matrix = shuffle_board(backend_matrix, shuffle_count, grid_size)
        st.rerun()

    # 2. A* SECTION
    st.write("--------------")
    st.subheader("A* Algorithm Solver")
    
    # Display puzzle again
    st.markdown(grid_html, unsafe_allow_html=True)
    
    if st.button("Solve Current Puzzle with A*"):
        solve_with_astar()

    # 3. MANUAL CONTROLS SECTION
    st.write("--------------")
    st.subheader("PLAY MANUALLY")
    
    # Find blank position
    blank_pos = None
    for r in range(grid_size):
        for c in range(grid_size):
            if backend_matrix[r][c] is None:
                blank_pos = (r, c)
                break
        if blank_pos: break

    if blank_pos:
        br, bc = blank_pos
        neighbors = get_neighbors(blank_pos, grid_size)
        
        # Control buttons in horizontal order
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if (br-1, bc) in neighbors and st.button("⬆️ Up"):
                r, c = br-1, bc
                backend_matrix[br][bc], backend_matrix[r][c] = backend_matrix[r][c], backend_matrix[br][bc]
                st.session_state.backend_matrix = backend_matrix
                st.rerun()
        
        with col2:
            if (br, bc-1) in neighbors and st.button("⬅️ Left"):
                r, c = br, bc-1
                backend_matrix[br][bc], backend_matrix[r][c] = backend_matrix[r][c], backend_matrix[br][bc]
                st.session_state.backend_matrix = backend_matrix
                st.rerun()
        
        with col3:
            if (br, bc+1) in neighbors and st.button("➡️ Right"):
                r, c = br, bc+1
                backend_matrix[br][bc], backend_matrix[r][c] = backend_matrix[r][c], backend_matrix[br][bc]
                st.session_state.backend_matrix = backend_matrix
                st.rerun()
        
        with col4:
            if (br+1, bc) in neighbors and st.button("⬇️ Down"):
                r, c = br+1, bc
                backend_matrix[br][bc], backend_matrix[r][c] = backend_matrix[r][c], backend_matrix[br][bc]
                st.session_state.backend_matrix = backend_matrix
                st.rerun()