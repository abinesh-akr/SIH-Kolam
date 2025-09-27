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

tab1, tab2, tab3 = st.tabs(["Rangoli-Style Drawing Teacher", "One-Stroke Kolam Teacher", "Grid Kolam Animator"])

with tab1:
    uploaded_file = st.file_uploader("Choose a Kolam image...", type=["jpg", "jpeg", "png"], key="tab1_upload")

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        original_image = cv2.imdecode(file_bytes, 1)
        
        st.image(original_image, caption="Uploaded Kolam", channels="BGR")

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
        
        DISPLAY_WIDTH = 500  # Reduced from 800
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
            st.image(st.session_state.image_path)
        else:
            st.warning("Could not load an image. Please check your folder structure.")

    with col2:
        st.subheader("Live Drawing Canvas")
        
        canvas_placeholder = st.empty()
        
        if st.button("✏️ Draw This Kolam", type="primary", disabled=(st.session_state.get('image_path') is None)):
            try:
                with st.spinner("Preparing to draw..."):
                    points = load_one_stroke_path(st.session_state.current_dots, st.session_state.image_index)
                    
                    CANVAS_SIZE = 400  # Reduced from 700
                    canvas = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 3), dtype=np.uint8)
                    
                    spacing = CANVAS_SIZE / (st.session_state.current_dots + 2)
                    dots, bbox = generate_diamond_dots(max_dots=st.session_state.current_dots, spacing=spacing)
                    norm_points = normalize_path(points, bbox)

                def to_canvas_coords(p):
                    return (int(CANVAS_SIZE/2 + p[0]), int(CANVAS_SIZE/2 + p[1]))

                for dot_coord in dots:
                    center = to_canvas_coords(dot_coord)
                    cv2.circle(canvas, center, 3, (128, 128, 128), -1)  # Adjusted dot size for smaller canvas
                canvas_placeholder.image(canvas, channels="BGR")
                time.sleep(0.5)

                if norm_points:
                    for i in range(len(norm_points) - 1):
                        pt1 = to_canvas_coords(norm_points[i])
                        pt2 = to_canvas_coords(norm_points[i+1])
                        cv2.line(canvas, pt1, pt2, (255, 255, 255), 1)  # Adjusted line thickness
                        
                        canvas_placeholder.image(canvas, channels="BGR")
                        time.sleep(0.1)
                
                canvas_placeholder.image(canvas, caption="Drawing Complete!", channels="BGR")

            except (FileNotFoundError, ValueError) as e:
                st.error(f"Could not draw the Kolam. {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            canvas_placeholder.image(np.zeros((400, 400, 3), dtype=np.uint8), caption="Click 'Draw This Kolam' to start.")

with tab3:
    st.subheader("Grid-Based Kolam Animator")
    st.write("Upload a Kolam image to analyze, extract grid dots, and animate the drawing process using a simulated grid overlay.")
    
    uploaded_file = st.file_uploader("Choose a Kolam image for grid analysis...", type=["jpg", "jpeg", "png"], key="tab3_upload")
    
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        original_image = cv2.imdecode(file_bytes, 1)
        
        st.image(original_image, caption="Uploaded Kolam for Grid Analysis", channels="BGR")
        
        grid_dimension = st.slider("Grid Dimension (e.g., 9 for 9x9 grid)", min_value=5, max_value=15, value=9, key="grid_dim")
        
        if st.button("Analyze and Animate Grid Drawing", type="primary"):
            with st.spinner("Analyzing image and preparing animation..."):
                try:
                    # Preprocess the image
                    scale = 600 / max(original_image.shape)
                    h, w = int(original_image.shape[0] * scale), int(original_image.shape[1] * scale)
                    resized_image = cv2.resize(original_image, (w, h), interpolation=cv2.INTER_AREA)
                    
                    # Extract contours (simulating line_paths)
                    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
                    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                    line_contours = [c for c in contours if cv2.contourArea(c) > 50]
                    
                    if not line_contours:
                        st.error("Could not find significant line patterns. Try a higher contrast image.")
                    else:
                        st.session_state.tab3_line_paths = line_contours
                        st.session_state.tab3_image_shape = resized_image.shape
                        
                        # Sample grid dots
                        all_points = np.vstack(line_contours).squeeze()
                        min_x, min_y = np.min(all_points, axis=0)
                        max_x, max_y = np.max(all_points, axis=0)
                        
                        step_x = (max_x - min_x) / (grid_dimension - 1)
                        step_y = (max_y - min_y) / (grid_dimension - 1)
                        
                        grid_dots = []
                        tolerance = 15
                        for r in range(grid_dimension):
                            for c in range(grid_dimension):
                                x = min_x + c * step_x
                                y = min_y + r * step_y
                                
                                inside = False
                                for contour in line_contours:
                                    dist = cv2.pointPolygonTest(contour, (x, y), True)
                                    if abs(dist) <= tolerance:
                                        inside = True
                                        break
                                if inside:
                                    grid_dots.append((int(x), int(y)))
                        
                        st.session_state.tab3_grid_dots = grid_dots
                        
                        st.success(f"Extracted {len(grid_dots)} grid dots within the Kolam region.")
                        
                        # Display grid overlay
                        overlay = resized_image.copy()
                        for dot in grid_dots:
                            cv2.circle(overlay, dot, 3, (0, 0, 255), -1)  # Red dots
                        
                        st.image(overlay, caption="Kolam with Extracted Grid Dots Overlay", channels="BGR")

                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")

    if 'tab3_grid_dots' in st.session_state and 'tab3_line_paths' in st.session_state:
        enable_webcam = st.checkbox("Enable Webcam Background", key="tab3_webcam_enable")
        
        dot_size = st.slider("Dot Size", min_value=1, max_value=10, value=3, key="dot_size")
        line_thickness = st.slider("Line Thickness", min_value=1, max_value=5, value=2, key="line_thickness")
        
        st.subheader("Animated Grid Drawing")
        
        canvas_placeholder = st.empty()
        
        img_h, img_w, _ = st.session_state.tab3_image_shape
        
        DISPLAY_WIDTH = 500
        aspect_ratio = img_h / img_w
        display_height = int(DISPLAY_WIDTH * aspect_ratio)
        
        cap = None
        dot_color = (0, 0, 255)  # Always red for dots
        
        if enable_webcam:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Cannot open webcam. Falling back to black background.")
                enable_webcam = False
        
        # Prepare drawing state
        current_dots = []
        drawn_segments = []
        
        def get_contrast_color(frame):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray)
            if avg_brightness > 170:
                return (0, 0, 0)  # Black for bright backgrounds
            elif avg_brightness < 85:
                return (255, 255, 255)  # White for dark backgrounds
            else:
                return (255, 255, 0)  # Yellow for medium contrast
            
        def display_current_state():
            if enable_webcam:
                ret, frame = cap.read()
                if ret:
                    bg = cv2.resize(frame, (img_w, img_h))
                    line_color = get_contrast_color(bg)
                else:
                    bg = np.zeros((img_h, img_w, 3), dtype=np.uint8)
                    line_color = (255, 255, 255)
            else:
                bg = np.zeros((img_h, img_w, 3), dtype=np.uint8)
                line_color = (255, 255, 255)
            
            # Redraw all elements with current line color
            for dot in current_dots:
                cv2.circle(bg, dot, dot_size, dot_color, -1)
            for pt1, pt2 in drawn_segments:
                cv2.line(bg, pt1, pt2, line_color, line_thickness)
            
            canvas_placeholder.image(cv2.resize(bg, (DISPLAY_WIDTH, display_height)), channels="BGR")
            return line_color
        
        # Step 1: Place the grid dots
        st.info("Step 1: Placing the foundational grid dots...")
        for i, dot in enumerate(st.session_state.tab3_grid_dots):
            current_dots.append(dot)
            display_current_state()
            if i % max(1, len(st.session_state.tab3_grid_dots) // 20) == 0:
                time.sleep(0.01)
        
        time.sleep(1)
        
        # Step 2: Draw the lines
        st.info("Step 2: Drawing the connecting lines...")
        for contour in st.session_state.tab3_line_paths:
            if len(contour) < 2:
                continue
            for i in range(len(contour) - 1):
                pt1 = tuple(contour[i][0])
                pt2 = tuple(contour[i+1][0])
                drawn_segments.append((pt1, pt2))
                line_color = display_current_state()
                time.sleep(0.01)
        
        # Final display
        final_line_color = display_current_state()
        st.success("Grid animation complete!")
        
        # For download, use a black background since live webcam can't be saved
        final_canvas = np.zeros((img_h, img_w, 3), dtype=np.uint8)
        for dot in current_dots:
            cv2.circle(final_canvas, dot, dot_size, dot_color, -1)
        for pt1, pt2 in drawn_segments:
            cv2.line(final_canvas, pt1, pt2, final_line_color, line_thickness)
        
        _, im_buf_arr = cv2.imencode(".png", final_canvas)
        byte_im = im_buf_arr.tobytes()
        st.download_button(
            label="Download Grid Drawing (PNG)",
            data=byte_im,
            file_name="grid_kolam_drawing.png",
            mime="image/png",
        )
        
        if cap:
            cap.release()
        
        del st.session_state.tab3_line_paths
        del st.session_state.tab3_grid_dots
        del st.session_state.tab3_image_shape
    else:
        st.warning("Upload an image and click 'Analyze and Animate Grid Drawing' to start.")
