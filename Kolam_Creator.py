import streamlit as st
from google import genai
from PIL import Image, ImageDraw
from io import BytesIO
import json
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = "sfw"

import numpy as np
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Kolam Creator", layout="wide")

# Custom CSS for blue theme and new animations
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lato:wght@300;400;600;700&display=swap');

/* Reset default styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Hide Streamlit default footer */
footer {visibility: hidden;}

/* Main container */
.main-content {
    background: linear-gradient(135deg, #DBEAFE, #EFF6FF);
    padding: 2rem;
    min-height: 100vh;
    margin-top: 80px;
    position: relative;
    overflow: hidden;
}

/* Floating dots animation */
.floating-dot {
    position: absolute;
    width: 12px;
    height: 12px;
    background: radial-gradient(circle, #3B82F6, transparent);
    border-radius: 50%;
    animation: floatPulse 5s ease-in-out infinite;
}

.dot-1 { top: 5%; left: 5%; animation-delay: 0s; }
.dot-2 { top: 15%; right: 5%; animation-delay: 1.5s; }
.dot-3 { bottom: 10%; left: 10%; animation-delay: 3s; }

@keyframes floatPulse {
    0%, 100% { transform: translateY(0) scale(1); opacity: 0.7; }
    50% { transform: translateY(-20px) scale(1.2); opacity: 1; }
}

/* Hero section */
.hero-section {
    background: linear-gradient(135deg, #DBEAFE, #EFF6FF);
    padding: 3rem;
    text-align: center;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    color: #1E3A8A;
    margin-bottom: 0.5rem;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); }
    to { text-shadow: 0 2px 8px rgba(59, 130, 246, 0.5); }
}

.hero-subtitle {
    font-family: 'Lato', sans-serif;
    font-size: 1.6rem;
    color: #3B82F6;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* Container styling */
 .settings-container, .tips-container {
    background: #F8FAFC;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}

.drawing-container:hover, .settings-container:hover, .tips-container:hover {
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    background: linear-gradient(135deg, #F8FAFC, #DBEAFE);
}

.drawing-container::before, .settings-container::before, .tips-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(147, 197, 253, 0.3), transparent);
    transition: 0.5s;
}

.drawing-container:hover::before, .settings-container:hover::before, .tips-container:hover::before {
    left: 100%;
}
            /* Container styling */
    .drawing-container {
        background: rgba(255,255,255,0.95);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 20px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }

/* Section title */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #1E3A8A;
    margin-bottom: 1rem;
    text-align: center;
    position: relative;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 50px;
    height: 3px;
    background: linear-gradient(90deg, #1E3A8A, #3B82F6);
    border-radius: 2px;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    color: #EFF6FF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #3B82F6, #93C5FD);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
    transform: translateY(-2px);
}

/* Color grid */
.color-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}

/* Tabs styling */
.stTabs [data-baseweb="tab"] {
    background: blue;
    border-radius: 8px;
    margin: 0.5rem;
    color : white;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: #DBEAFE;
    transform: translateY(-2px);
}

.stTabs [data-baseweb="tab-highlight"] {
    background: #3B82F6;
}

/* Responsive design */
@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    .hero-subtitle { font-size: 1.2rem; }
    .section-title { font-size: 1.5rem; }
    .main-content { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)


st.title("🎨 Kolam Creator")
st.write("Recreate Kolams through generation or drawing.")

tab1, tab2 = st.tabs(["AI Prompt Generation", "Canvas & Brush"])

with tab1:
    # Code from Kolam.py (assuming it's the prompt-based)
    client = genai.Client(api_key=GEMINI_API_KEY)

    def create_advanced_kolam_prompt(kolam_type, state, complexity, grid_size, color_scheme, occasion, custom_elements):
        prompt = """
        Generate a high-quality, artistic Kolam (Rangoli) design based on the following details:

        - Type: Symmetric Kolam design with dots (pulli) as a base grid.
        - Grid: Use a 1-3-5-7-9-7-5-3-1 stepped dot grid.
        - Style: Traditional South Indian Kolam, drawn with white rice powder on a dark, wet floor background.
        - Lines: Smooth, curvilinear, continuous loops enclosing all dots.
        - Symmetry: Both reflectional and rotational symmetry must be present.
        - Visual feel: Elegant, culturally authentic, geometric, and mathematically balanced.
        - Avoid text, borders, or watermarks.
        - Make it look hand-drawn but neat, with fine white strokes.
        - Output: A single, clear Kolam pattern with focus on the design — no extra decorations, no people, no objects.
        """
        return prompt

    col1, col2 = st.columns(2)
    with col1:
        kolam_type = st.selectbox("Kolam Style", ["Sikku Kolam", "Pulli Kolam", "Rangoli", "Freehand Kolam",
                                                  "Geometric Kolam", "Floral Kolam", "Festival Special"], index=2)
        state = st.selectbox("Regional Style", ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Kerala", "Telangana"])

    with col2:
        complexity = st.selectbox("Complexity", ["Beginner", "Intermediate", "Advanced", "Master Level"], index=1)
        grid_size = st.slider("Pattern Density", 8, 20, 12)

    color_scheme = st.sidebar.selectbox("Color Theme", ["Vibrant Festival", "Royal Colors", "Pastel Dream",
                                                       "Nature Inspired", "Traditional White", "Monochrome Elegant"])

    occasion = st.sidebar.selectbox("Special Occasion", ["Daily Practice", "Diwali", "Pongal",
                                                        "Wedding", "Navratri", "Housewarming"])

    custom_elements = st.sidebar.text_area("Custom Elements",
                                           placeholder="e.g., peacock motifs, lotus flowers, temple arches...",
                                           height=80)

    if st.sidebar.button("🎨 Create Stunning Kolam", type="primary", use_container_width=True):
        with st.spinner("🎭 AI is creating your masterpiece..."):
            try:
                advanced_prompt = create_advanced_kolam_prompt(
                    kolam_type, state, complexity, grid_size, color_scheme, occasion, custom_elements
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash-image-preview",
                    contents=advanced_prompt
                )

                image_parts = [
                    part.inline_data.data
                    for part in response.candidates[0].content.parts
                    if part.inline_data
                ]

                if image_parts:
                    image = Image.open(BytesIO(image_parts[0]))
                    st.image(image, use_container_width=True, caption=f"✨ {kolam_type} Kolam from {state}")

                    img_buffer = BytesIO()
                    image.save(img_buffer, format="PNG")
                    st.download_button(
                        "📥 Download High-Quality Kolam",
                        data=img_buffer.getvalue(),
                        file_name=f"{kolam_type}_{state}_{complexity}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    st.error("⚠️ No image was generated. Try again with a different configuration.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Check your API connection or simplify your prompt.")

with tab2:


    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="kolam-pattern-large"></div>
        <h1 class="hero-title">🎨 Kolam Drawing Canvas</h1>
        <p class="hero-subtitle">Multi-Brush • Symmetry • Sacred Geometry</p>
        <div class="kolam-pattern-small"></div>
    </div>
    """, unsafe_allow_html=True)

    # Instructions / Tips
    st.markdown("""
    <div class="tips-container">
        <div class="tips-title">✨ Tips for Drawing Beautiful Kolam</div>
        <ul style="font-family: 'Lato', sans-serif; color: #2C3E50; line-height: 1.6;">
            <li>🎨 Use light colors for intricate patterns</li>
            <li>🖌️ Try different brush sizes and shapes</li>
            <li>🔄 Enable mirror symmetry for authentic Kolam designs</li>
            <li>💾 Download your final masterpiece when done</li>
            <li>🌟 Start from the center and work outward</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Canvas & Brush Settings
    st.markdown('<div class="settings-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🎨 Canvas & Brush Settings</h2>', unsafe_allow_html=True)

    canvas_size = 900  # Fixed canvas size

    col1, col2, col3 = st.columns(3)

    with col1:
        # Background color
        bg_color = st.color_picker("🎨 Background Color", "#071029")
        
        # Brush width
        stroke_width = st.slider("🖌️ Stroke Width", 1, 20, 3)

    with col2:
        # Brush shape
        drawing_mode = st.selectbox("✏️ Brush Shape", ["freedraw", "line", "circle", "rect"])
        
        # Mirror count
        mirror_count = st.selectbox("🔄 Number of Mirrors", [1, 2, 4, 6, 8], index=0)

    with col3:
        st.markdown('<div class="kolam-pattern-mini"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Color Selection
    st.markdown('<div class="settings-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">🌈 Choose Your Colors</h3>', unsafe_allow_html=True)

    # Define colors with names
    color_options = {
        "Lotus Pink": "#FFD6FF",
        "Sacred Cyan": "#66FFF0", 
        "Temple Orange": "#FF7B2F",
        "Divine Mint": "#2AF598",
        "Sky Blue": "#00C6FF",
        "Golden Sun": "#FFFA66",
        "Royal Magenta": "#FF66A3"
    }

    # Responsive color buttons
    stroke_color = st.session_state.get("selected_color", "#FFD6FF")
    color_cols = st.columns(len(color_options))
    for i, (name, hex_color) in enumerate(color_options.items()):
        with color_cols[i]:
            if st.button(f"🎨 {name}", key=f"color_{name}_{i}", help=f"Click to select {name}"):
                stroke_color = hex_color
                st.session_state["selected_color"] = hex_color
            # Show color preview
            st.markdown(f'<div style="width: 100%; height: 20px; background: {hex_color}; border-radius: 10px; margin: 5px 0; box-shadow: 0 3px 8px rgba(0,0,0,0.2);"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Mirror Symmetry Function
    def apply_mirror(strokes_img: Image.Image, mirrors: int, bg_rgb: tuple) -> Image.Image:
        """Replicates strokes around center with N-way rotational symmetry."""
        if mirrors == 1:
            return strokes_img

        cx, cy = strokes_img.size[0] // 2, strokes_img.size[1] // 2
        base = strokes_img.convert("RGBA")

        # Make strokes transparent except actual drawing
        datas = base.getdata()
        new_data = []
        for item in datas:
            if item[:3] == bg_rgb:  # background pixel
                new_data.append((0, 0, 0, 0))  # transparent
            else:
                new_data.append(item)
        base.putdata(new_data)

        result = Image.new("RGBA", base.size, (0, 0, 0, 0))
        for i in range(mirrors):
            rotated = base.rotate((360.0 / mirrors) * i, center=(cx, cy))
            result = Image.alpha_composite(result, rotated)

        return result

    # Canvas
    st.markdown('<div class="drawing-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🖼️ Your Sacred Canvas</h2>', unsafe_allow_html=True)

    st.markdown('<div class="canvas-wrapper">', unsafe_allow_html=True)
    canvas_result = st_canvas(
        fill_color=None,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_size,
        width=canvas_size,
        drawing_mode=drawing_mode,
        key="kolam_canvas"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Convert background color hex → RGB for transparency check
    bg_rgb = tuple(int(bg_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    # Handle drawing
    if canvas_result.image_data is not None:
        img_current = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")

        # Apply mirror symmetry
        mirrored_strokes = apply_mirror(img_current, mirror_count, bg_rgb)

        # Merge with solid background
        bg_layer = Image.new("RGBA", (canvas_size, canvas_size), bg_rgb + (255,))
        final_img = Image.alpha_composite(bg_layer, mirrored_strokes)

        # Display the drawing
        st.markdown('<div class="drawing-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">✨ Your Kolam Masterpiece</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(final_img, width=canvas_size)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Download drawing
        st.markdown('<div class="download-section">', unsafe_allow_html=True)
        st.markdown('<div class="kolam-pattern-small"></div>', unsafe_allow_html=True)
        
        buf = BytesIO()
        final_img.save(buf, format="PNG")
        st.download_button(
            "💾 Download Your Sacred Art",
            data=buf,
            file_name="kolam_masterpiece.png",
            mime="image/png",
            help="Save your beautiful Kolam creation!"
        )
        
        st.markdown('<div class="kolam-pattern-mini"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 40px; 
        background: linear-gradient(135deg, #E8F5E8, #E6F3FF, #FFE4E1); 
        background-size: 300% 300%;
        animation: gradientShift 10s ease infinite;
        margin-top: 40px; 
        border-radius: 25px;
        position: relative;
    ">
        <div class="kolam-pattern-large"></div>
        <p style="
            font-family: 'Dancing Script', cursive; 
            color: #2C3E50; 
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 15px;
        ">
            Create • Inspire • Preserve Sacred Art
        </p>
        <div class="kolam-pattern-small"></div>
        <p style="
            font-family: 'Lato', sans-serif; 
            color: #5D6D7E; 
            font-style: italic;
        ">
            "Every dot connects to create infinite beauty"
        </p>
    </div>
    """, unsafe_allow_html=True)
