import streamlit as st
import cv2
import numpy as np
import time
from kolam_processing import extract_kolam_paths, save_paths_to_csv_bytes

st.set_page_config(page_title="Kolam Drawing Teacher", layout="wide")

st.title("✍️ Kolam Drawing Teacher")
st.write("Upload an image of a Kolam, and watch the app trace and redraw it for you, stroke by stroke.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a Kolam image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the uploaded file into an OpenCV image
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
                    
                    # Display processing steps
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
    
    # --- CHANGE #1: Define a fixed width for the display canvas ---
    DISPLAY_WIDTH = 800 
    
    # Create a black canvas matching the original image's dimensions for accurate drawing
    h, w, _ = st.session_state.image_shape
    canvas = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Calculate aspect ratio for consistent display resizing
    aspect_ratio = h / w
    display_height = int(DISPLAY_WIDTH * aspect_ratio)

    # Placeholder for the animation
    drawing_placeholder = st.empty()
    
    # Initial empty canvas display
    initial_display_canvas = cv2.resize(canvas, (DISPLAY_WIDTH, display_height))
    drawing_placeholder.image(initial_display_canvas, caption="Drawing will appear here...")

    # Animate the drawing
    for path in st.session_state.paths:
        if len(path) < 2:
            continue
        for i in range(len(path) - 1):
            pt1 = path[i]
            pt2 = path[i+1]
            cv2.line(canvas, pt1, pt2, (255, 255, 255), 1)
            
            # --- CHANGE #2: Slow down and smooth out the animation ---
            # We removed the `if i % 5 == 0` to draw every single segment smoothly.
            # We increased the sleep time to slow down the drawing speed.
            
            # Resize the canvas for display right before showing it
            display_canvas = cv2.resize(canvas, (DISPLAY_WIDTH, display_height))
            drawing_placeholder.image(display_canvas, channels="BGR")
            
            time.sleep(0.02) # Increase this value for slower drawing, decrease for faster
    
    # Display the final complete drawing
    final_display_canvas = cv2.resize(canvas, (DISPLAY_WIDTH, display_height))
    drawing_placeholder.image(final_display_canvas, caption="Final Drawing", channels="BGR")
    
    st.success("Drawing complete!")
    
    # --- Download Buttons ---
    st.subheader("Download Results")
    col1, col2 = st.columns(2)
    
    # Download final image (the full-resolution one, not the resized display)
    _, im_buf_arr = cv2.imencode(".png", canvas)
    byte_im = im_buf_arr.tobytes()
    col1.download_button(
        label="Download Final Drawing (PNG)",
        data=byte_im,
        file_name="kolam_drawing.png",
        mime="image/png",
    )
    
    # Download coordinates CSV
    csv_bytes = save_paths_to_csv_bytes(st.session_state.paths)
    col2.download_button(
        label="Download Coordinates (CSV)",
        data=csv_bytes,
        file_name="kolam_coordinates.csv",
        mime="text/csv",
    )

    # Clean up session state after use
    del st.session_state.paths
    del st.session_state.image_shape