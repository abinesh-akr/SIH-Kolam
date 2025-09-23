import streamlit as st
import cv2
import numpy as np
import time
from kolam_processing import extract_kolam_paths, save_paths_to_csv_bytes
from kolam_one_stroke_logic import (
    get_random_image,
    load_one_stroke_path,
    generate_diamond_dots,
    normalize_path
)

st.set_page_config(page_title="Kolam Mastery", layout="wide")

st.title("🖌️ Kolam Mastery")
st.write("Learn to recreate Kolams through guided drawing.")

tab1, tab2 = st.tabs(["Rangoli-Style Drawing Teacher", "One-Stroke Kolam Teacher"])

with tab1:
    # Code from Kolam_Teacher.py
    uploaded_file = st.file_uploader("Choose a Kolam image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        original_image = cv2.imdecode(file_bytes, 1)
        
        st.image(original_image, caption="Uploaded Kolam", channels="BGR", use_column_width=True)

        if st.button("Trace and Draw Kolam", type="primary"):
            with st.spinner("Analyzing and tracing the Kolam..."):
                try:
                    paths, edges, mask, skeleton = extract_kolam_paths(original_image)
                    if not paths:
                        st.error("Could not detect any Kolam paths. Please try a different image with higher contrast.")
                    else:
                        st.session_state.paths = paths
                        st.session_state.image_shape = original_image.shape
                        
                        st.subheader("Image Processing Steps")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.image(edges, caption="1. Canny Edges")
                        with col2:
                            st.image(mask, caption="2. Filled Mask")
                        with col3:
                            st.image(skeleton, caption="3. Final Skeleton")

                except Exception as e:
                    st.error(f"An error occurred during processing: {e}")

    if 'paths' in st.session_state:
        st.subheader("Animated Drawing")
        
        DISPLAY_WIDTH = 800 
        h, w, _ = st.session_state.image_shape
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        
        aspect_ratio = h / w
        display_height = int(DISPLAY_WIDTH * aspect_ratio)

        drawing_placeholder = st.empty()
        
        initial_display_canvas = cv2.resize(canvas, (DISPLAY_WIDTH, display_height))
        drawing_placeholder.image(initial_display_canvas, caption="Drawing will appear here...")

        for path in st.session_state.paths:
            if len(path) < 2:
                continue
            for i in range(len(path) - 1):
                pt1 = path[i]
                pt2 = path[i+1]
                cv2.line(canvas, pt1, pt2, (255, 255, 255), 1)
                
                display_canvas = cv2.resize(canvas, (DISPLAY_WIDTH, display_height))
                drawing_placeholder.image(display_canvas, channels="BGR")
                
                time.sleep(0.02)
        
        final_display_canvas = cv2.resize(canvas, (DISPLAY_WIDTH, display_height))
        drawing_placeholder.image(final_display_canvas, caption="Final Drawing", channels="BGR")
        
        st.success("Drawing complete!")
        
        st.subheader("Download Results")
        col1, col2 = st.columns(2)
        
        _, im_buf_arr = cv2.imencode(".png", canvas)
        byte_im = im_buf_arr.tobytes()
        col1.download_button(
            label="Download Final Drawing (PNG)",
            data=byte_im,
            file_name="kolam_drawing.png",
            mime="image/png",
        )
        
        csv_bytes = save_paths_to_csv_bytes(st.session_state.paths)
        col2.download_button(
            label="Download Coordinates (CSV)",
            data=csv_bytes,
            file_name="kolam_coordinates.csv",
            mime="text/csv",
        )

        del st.session_state.paths
        del st.session_state.image_shape

with tab2:
    # Code from kolam_one_stroke.py
    dot_options = [19, 29, 109]
    selected_dots = st.radio(
        "Select the number of dots for the Kolam grid:",
        dot_options,
        horizontal=True,
        key="dot_selection"
    )

    if 'current_dots' not in st.session_state or st.session_state.current_dots != selected_dots:
        st.session_state.current_dots = selected_dots
        st.session_state.image_path, st.session_state.image_index, error = get_random_image(selected_dots)
        if error:
            st.error(error)

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

    with col2:
        st.subheader("Live Drawing Canvas")
        
        canvas_placeholder = st.empty()
        
        if st.button("✏️ Draw This Kolam", type="primary", disabled=(st.session_state.get('image_path') is None)):
            try:
                with st.spinner("Preparing to draw..."):
                    points = load_one_stroke_path(st.session_state.current_dots, st.session_state.image_index)
                    
                    CANVAS_SIZE = 700
                    canvas = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 3), dtype=np.uint8)
                    
                    spacing = CANVAS_SIZE / (st.session_state.current_dots + 2)
                    dots, bbox = generate_diamond_dots(max_dots=st.session_state.current_dots, spacing=spacing)
                    norm_points = normalize_path(points, bbox)

                def to_canvas_coords(p):
                    return (int(CANVAS_SIZE/2 + p[0]), int(CANVAS_SIZE/2 + p[1]))

                for dot_coord in dots:
                    center = to_canvas_coords(dot_coord)
                    cv2.circle(canvas, center, 4, (128, 128, 128), -1)
                canvas_placeholder.image(canvas, channels="BGR")
                time.sleep(0.5)

                if norm_points:
                    for i in range(len(norm_points) - 1):
                        pt1 = to_canvas_coords(norm_points[i])
                        pt2 = to_canvas_coords(norm_points[i+1])
                        cv2.line(canvas, pt1, pt2, (255, 255, 255), 2)
                        
                        canvas_placeholder.image(canvas, channels="BGR")
                        time.sleep(0.1)
                
                canvas_placeholder.image(canvas, caption="Drawing Complete!", channels="BGR")

            except (FileNotFoundError, ValueError) as e:
                st.error(f"Could not draw the Kolam. {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            canvas_placeholder.image(np.zeros((700, 700, 3), dtype=np.uint8), caption="Click 'Draw This Kolam' to start.")