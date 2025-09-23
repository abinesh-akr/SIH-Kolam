import streamlit as st
import cv2
import numpy as np
import time
from kolam_one_stroke_logic import (
    get_random_image,
    load_one_stroke_path,
    generate_diamond_dots,
    normalize_path
)

st.set_page_config(page_title="Kolam One Stroke", layout="wide")

st.title("🎨 Kolam One Stroke")
st.write("Select a dot grid size, see a sample Kolam, and watch it being drawn in a single continuous stroke.")

# --- 1. User Input and State Management ---
dot_options = [19, 29, 109]
selected_dots = st.radio(
    "Select the number of dots for the Kolam grid:",
    dot_options,
    horizontal=True,
    key="dot_selection"
)

# Initialize or reset state when dot selection changes
if 'current_dots' not in st.session_state or st.session_state.current_dots != selected_dots:
    st.session_state.current_dots = selected_dots
    st.session_state.image_path, st.session_state.image_index, error = get_random_image(selected_dots)
    if error:
        st.error(error)

# --- 2. Image Display and Refresh ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Sample Kolam")
    if st.button("🔄 Refresh Image"):
        st.session_state.image_path, st.session_state.image_index, error = get_random_image(selected_dots)
        if error:
            st.error(error)

    if st.session_state.get('image_path'):
        st.image(st.session_state.image_path, use_column_width=True)
    else:
        st.warning("Could not load an image. Please check your folder structure.")

# --- 3. Drawing Canvas and Logic ---
with col2:
    st.subheader("Live Drawing Canvas")
    
    # Placeholder for the drawing animation
    canvas_placeholder = st.empty()
    
    if st.button("✏️ Draw This Kolam", type="primary", disabled=(st.session_state.get('image_path') is None)):
        try:
            with st.spinner("Preparing to draw..."):
                # Load the specific path data for the current image
                points = load_one_stroke_path(st.session_state.current_dots, st.session_state.image_index)
                
                # --- Animation Setup (replaces turtle) ---
                CANVAS_SIZE = 700
                canvas = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 3), dtype=np.uint8)
                
                # Generate dots and scale the path
                spacing = CANVAS_SIZE / (st.session_state.current_dots + 2)
                dots, bbox = generate_diamond_dots(max_dots=st.session_state.current_dots, spacing=spacing)
                norm_points = normalize_path(points, bbox)

            # --- Animate Drawing ---
            
            # Function to convert normalized coords to canvas coords
            def to_canvas_coords(p):
                return (int(CANVAS_SIZE/2 + p[0]), int(CANVAS_SIZE/2 + p[1]))

            # 1. Draw all dots first
            for dot_coord in dots:
                center = to_canvas_coords(dot_coord)
                cv2.circle(canvas, center, 4, (128, 128, 128), -1) # Grey dots
            canvas_placeholder.image(canvas, channels="BGR")
            time.sleep(0.5)

            # 2. Draw the continuous line
            if norm_points:
                for i in range(len(norm_points) - 1):
                    pt1 = to_canvas_coords(norm_points[i])
                    pt2 = to_canvas_coords(norm_points[i+1])
                    cv2.line(canvas, pt1, pt2, (255, 255, 255), 2) # White line
                    
                    # Update image every few steps for performance
                    #if i % 1 == 0:
                    canvas_placeholder.image(canvas, channels="BGR")
                    time.sleep(0.1) # Controls drawing speed
            
            # Show the final complete drawing
            canvas_placeholder.image(canvas, caption="Drawing Complete!", channels="BGR")

        except (FileNotFoundError, ValueError) as e:
            st.error(f"Could not draw the Kolam. {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        # Display an empty canvas initially
        canvas_placeholder.image(np.zeros((700, 700, 3), dtype=np.uint8), caption="Click 'Draw This Kolam' to start.")