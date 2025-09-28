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
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av

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
        
        grid_dimension = st.slider("Grid Dimension (e.g., 9 for 9x9 grid)", min_value=5, max_value=20, value=9, key="grid_dim")
       
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
        
        # Custom Video Processor for WebRTC
        class KolamVideoProcessor(VideoTransformerBase):
            def __init__(self, dot_size, line_thickness):
                self.current_dots = []
                self.drawn_segments = []
                self.img_h, self.img_w = st.session_state.tab3_image_shape[:2]
                self.dot_size = dot_size  # Use passed parameter
                self.line_thickness = line_thickness  # Use passed parameter
                self.dot_color = (0, 0, 255)  # Red dots
                self.animation_step = 0
                self.grid_dots = st.session_state.tab3_grid_dots
                self.line_paths = st.session_state.tab3_line_paths
                self.total_dots = len(self.grid_dots)
                self.total_segments = sum(len(path) - 1 for path in self.line_paths if len(path) > 1)

            def get_contrast_color(self, frame):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                avg_brightness = np.mean(gray)
                if avg_brightness > 170:
                    return (0, 0, 0)  # Black for bright backgrounds
                elif avg_brightness < 85:
                    return (255, 255, 255)  # White for dark backgrounds
                else:
                    return (0, 255, 255)  # Yellow for medium

            def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
                img = frame.to_ndarray(format="bgr24")
                
                # Resize input frame to match image shape
                img_resized = cv2.resize(img, (self.img_w, self.img_h))
                
                line_color = self.get_contrast_color(img_resized)
                
                # Step 1: Animate placing dots
                if self.animation_step < self.total_dots * 5:
                    dot_index = self.animation_step // 5
                    if dot_index < len(self.grid_dots):
                        self.current_dots.append(self.grid_dots[dot_index])
                    self.animation_step += 1
                
                # Step 2: Animate lines
                elif self.animation_step < self.total_dots * 5 + self.total_segments * 5:
                    seg_step = (self.animation_step - self.total_dots * 5) // 5
                    if seg_step < self.total_segments:
                        all_segments = [(tuple(path[i][0]), tuple(path[i+1][0])) 
                                        for path in self.line_paths if len(path) > 1 
                                        for i in range(len(path) - 1)]
                        if seg_step < len(all_segments):
                            self.drawn_segments.append(all_segments[seg_step])
                    self.animation_step += 1
                else:
                    self.animation_step = 0
                    self.current_dots = []
                    self.drawn_segments = []
                
                # Draw current state
                for dot in self.current_dots:
                    cv2.circle(img_resized, dot, self.dot_size, self.dot_color, -1)
                for pt1, pt2 in self.drawn_segments:
                    cv2.line(img_resized, pt1, pt2, line_color, self.line_thickness)
                
                return av.VideoFrame.from_ndarray(img_resized, format="bgr24")

        if enable_webcam:
            st.info("Grant camera permission when prompted. Animation will overlay on live feed.")
            webrtc_ctx = webrtc_streamer(
                key="kolam-webcam",
                video_processor_factory=lambda: KolamVideoProcessor(dot_size, line_thickness),  # Pass parameters
                rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            )
            
            if webrtc_ctx.state.playing:
                st.success("Webcam stream active! Watch the animation overlay.")
            else:
                st.warning("Start the stream by clicking the play button above.")
        else:
            st.info("Webcam disabled. Animation will use black background.")
            canvas_placeholder = st.empty()
            img_h, img_w = st.session_state.tab3_image_shape[:2]
            canvas = np.zeros((img_h, img_w, 3), dtype=np.uint8)
            current_dots = []
            drawn_segments = []
            
            st.info("Step 1: Placing the foundational grid dots...")
            for i, dot in enumerate(st.session_state.tab3_grid_dots):
                current_dots.append(dot)
                for d in current_dots:
                    cv2.circle(canvas, d, dot_size, (0, 0, 255), -1)
                canvas_placeholder.image(cv2.resize(canvas, (500, int(500 * img_h / img_w))), channels="BGR")
                if i % max(1, len(st.session_state.tab3_grid_dots) // 20) == 0:
                    time.sleep(0.01)
            
            st.info("Step 2: Drawing the connecting lines...")
            for contour in st.session_state.tab3_line_paths:
                if len(contour) < 2:
                    continue
                for i in range(len(contour) - 1):
                    pt1 = tuple(contour[i][0])
                    pt2 = tuple(contour[i+1][0])
                    drawn_segments.append((pt1, pt2))
                    line_color = (255, 255, 255)  # Default white for black bg
                    for d in current_dots:
                        cv2.circle(canvas, d, dot_size, (0, 0, 255), -1)
                    for p1, p2 in drawn_segments:
                        cv2.line(canvas, p1, p2, line_color, line_thickness)
                    canvas_placeholder.image(cv2.resize(canvas, (500, int(500 * img_h / img_w))), channels="BGR")
                    time.sleep(0.01)
            
            st.success("Grid animation complete!")
            
            # Download for non-webcam
            _, im_buf_arr = cv2.imencode(".png", canvas)
            byte_im = im_buf_arr.tobytes()
            st.download_button(
                label="Download Grid Drawing (PNG)",
                data=byte_im,
                file_name="grid_kolam_drawing.png",
                mime="image/png",
            )
        
        # Download (for both webcam and non-webcam cases, static version)
        final_canvas = np.zeros((st.session_state.tab3_image_shape[0], st.session_state.tab3_image_shape[1], 3), dtype=np.uint8)
        for dot in st.session_state.tab3_grid_dots:
            cv2.circle(final_canvas, dot, dot_size, (0, 0, 255), -1)
        for contour in st.session_state.tab3_line_paths:
            if len(contour) > 1:
                for i in range(len(contour) - 1):
                    pt1 = tuple(contour[i][0])
                    pt2 = tuple(contour[i+1][0])
                    cv2.line(final_canvas, pt1, pt2, (255, 255, 255), line_thickness)
        
        _, im_buf_arr = cv2.imencode(".png", final_canvas)
        byte_im = im_buf_arr.tobytes()
        st.download_button(
            label="Download Grid Drawing (PNG)",
            data=byte_im,
            file_name="grid_kolam_drawing.png",
            mime="image/png",
        )
        
        if 'webrtc_ctx' in locals():
            del locals()['webrtc_ctx']
        
        # Clean up session state
        del st.session_state.tab3_line_paths
        del st.session_state.tab3_grid_dots
        del st.session_state.tab3_image_shape
    else:
        st.warning("Upload an image and click 'Analyze and Animate Grid Drawing' to start.")
