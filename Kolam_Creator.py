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

# Custom CSS with enhanced Kolam-themed styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lato:wght@300;400;600;700&family=Dancing+Script:wght@400;700&display=swap');
    
    /* Hide Streamlit default elements */
    footer {visibility: hidden;}
    
    /* Main container styling */
    .main > div {
        padding-top: 1rem;
    }
    
    /* Animated background */
    body {
        background: linear-gradient(-45deg, #FFE4E1, #E6E6FA, #E8F5E8, #FFEAA7);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated Kolam patterns */
    .kolam-pattern-large {
        width: 120px;
        height: 120px;
        position: relative;
        margin: 20px auto;
        animation: rotate 12s linear infinite;
    }
    
    .kolam-pattern-large::before {
        content: '';
        position: absolute;
        width: 8px;
        height: 8px;
        background: #FF69B4;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        box-shadow:
            0 -40px 0 #FF69B4,
            40px -40px 0 #9370DB,
            40px 0 0 #20B2AA,
            40px 40px 0 #FFD700,
            0 40px 0 #FF69B4,
            -40px 40px 0 #32CD32,
            -40px 0 0 #FF6347,
            -40px -40px 0 #4169E1,
            0 -20px 0 #FF69B4,
            20px -20px 0 #9370DB,
            20px 0 0 #20B2AA,
            20px 20px 0 #FFD700,
            0 20px 0 #FF69B4,
            -20px 20px 0 #32CD32,
            -20px 0 0 #FF6347,
            -20px -20px 0 #4169E1;
        animation: pulse 3s ease-in-out infinite;
    }
    
    .kolam-pattern-small {
        width: 80px;
        height: 80px;
        position: relative;
        margin: 15px auto;
        animation: float 4s ease-in-out infinite;
    }
    
    .kolam-pattern-small::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border: 4px solid #FF69B4;
        border-radius: 50%;
        animation: ripple 4s ease-out infinite;
    }
    
    .kolam-pattern-small::after {
        content: '';
        position: absolute;
        width: 60%;
        height: 60%;
        top: 20%;
        left: 20%;
        border: 3px solid #9370DB;
        border-radius: 50%;
        animation: ripple 4s ease-out infinite 1.5s;
    }
    
    .kolam-pattern-mini {
        width: 60px;
        height: 60px;
        position: relative;
        margin: 10px auto;
        animation: spin 8s linear infinite reverse;
    }
    
    .kolam-pattern-mini::before {
        content: '';
        position: absolute;
        width: 4px;
        height: 4px;
        background: #FFD700;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        box-shadow:
            0 -20px 0 #FF69B4,
            20px -20px 0 #9370DB,
            20px 0 0 #20B2AA,
            20px 20px 0 #FFD700,
            0 20px 0 #FF69B4,
            -20px 20px 0 #32CD32,
            -20px 0 0 #FF6347,
            -20px -20px 0 #4169E1;
        animation: twinkle 2s ease-in-out infinite alternate;
    }
    
    @keyframes ripple {
        0% { transform: scale(0.6); opacity: 1; }
        100% { transform: scale(1.8); opacity: 0; }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes spin {
        from { transform: rotate(360deg); }
        to { transform: rotate(0deg); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.7; transform: translate(-50%, -50%) scale(1); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.3); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    @keyframes twinkle {
        0% { opacity: 0.5; transform: translate(-50%, -50%) scale(0.8); }
        100% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #FFE4E1 40%, #FEFAA7 60%, #E6E6FA 10%);
        padding: 50px 40px;
        text-align: center;
        border-radius: 30px;
        margin-bottom: 30px;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.6);
        position: relative;
        overflow: hidden;
        background-size: 200% 200%;
        animation: gradientShift 10s ease infinite;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: #5D6D7E;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
        text-shadow: 3px 3px 6px rgba(255,255,255,0.8);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { text-shadow: 3px 3px 6px rgba(255,255,255,0.8); }
        to { text-shadow: 3px 3px 20px rgba(255,182,193,0.6), 0 0 30px rgba(255,182,193,0.4); }
    }
    
    .hero-subtitle {
        font-family: 'Dancing Script', cursive;
        font-size: 1.6rem;
        color: #5D6D7E;
        font-weight: 700;
        position: relative;
        z-index: 2;
        animation: subtitleFloat 4s ease-in-out infinite;
    }
    
    @keyframes subtitleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
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
    
    .settings-container {
        background: rgba(255,255,255,0.9);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        margin: 15px 0;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 20px;
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
        background: linear-gradient(90deg, #FF69B4, #9370DB);
        border-radius: 2px;
    }
    
    /* Color button styling */
    .color-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF69B4, #9370DB);
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(255,105,180,0.4) !important;
        font-family: 'Lato', sans-serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255,105,180,0.6) !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #FF69B4, #9370DB);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.9);
        border-radius: 12px;
        border: 2px solid t...(truncated 1911 characters)...: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-25px) rotate(180deg); }
    }
    
    /* Tips section special styling */
    .tips-container {
        background: linear-gradient(135deg, rgba(232,245,232,0.9), rgba(255,228,225,0.9));
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        border: 2px solid rgba(50,205,50,0.3);
    }
    
    .tips-title {
        font-family: 'Playfair Display', serif;
        color: #2C3E50;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem; }
        .hero-subtitle { font-size: 1.3rem; }
        .drawing-container { padding: 25px; }
        .settings-container { padding: 20px; }
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