import streamlit as st
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from dotenv import load_dotenv
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import langdetect
from PIL import Image
from deep_translator import GoogleTranslator
import os
load_dotenv()

SUTRA_API = os.getenv("SUTRA_API_KEY")

sutra_model = OpenAILike(
    id="sutra-v2",
    api_key=os.getenv("SUTRA_API_KEY", "sutra_1p8L5c8EmR1gUrtXbmw20kmYzS0GDC2Tq7a86U8pPTNmW6UUz0psboTmC5NK"),
    base_url="https://api.two.ai/v2",
    extra_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
)

print(sutra_model)

sutra_agent = Agent(
    name="Kolam Multilingual Analyzer",
    model=sutra_model,
    instructions=[
        "Be culturally sensitive, clear, and detailed.",
        "Explain the Kolam art type, its regional origin, mathematical significance, grid count, history, and importance in a systematic way.",
        "Respond in the user's preferred language. If you cannot connect to Sutra or face any error, return a short friendly error message instead of crashing."
    ],
  
    markdown=True,
)

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
    .kolam-pattern-1 {
        width: 60px;
        height: 60px;
        position: relative;
        margin: 20px auto;
        animation: rotate 8s linear infinite;
    }
    
    .kolam-pattern-1::before {
        content: '';
        position: absolute;
        width: 4px;
        height: 4px;
        background: #FF69B4;
        border-radius: 50%;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 
            0 15px 0 #FF69B4,
            0 30px 0 #FF69B4,
            0 45px 0 #FF69B4,
            15px 7.5px 0 #FF1493,
            15px 22.5px 0 #FF1493,
            15px 37.5px 0 #FF1493,
            -15px 7.5px 0 #FF1493,
            -15px 22.5px 0 #FF1493,
            -15px 37.5px 0 #FF1493;
    }
    
    .kolam-pattern-2 {
        width: 80px;
        height: 80px;
        position: relative;
        margin: 20px auto;
        animation: pulse 3s ease-in-out infinite;
    }
    
    .kolam-pattern-2::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid #9370DB;
        border-radius: 50%;
        animation: ripple 2s ease-out infinite;
    }
    
    .kolam-pattern-2::after {
        content: '';
        position: absolute;
        width: 60%;
        height: 60%;
        top: 20%;
        left: 20%;
        border: 2px solid #DA70D6;
        border-radius: 50%;
        animation: ripple 2s ease-out infinite 0.5s;
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0.8);
            opacity: 1;
        }
        100% {
            transform: scale(1.2);
            opacity: 0;
        }
    }
    
    .kolam-pattern-3 {
        width: 100px;
        height: 100px;
        position: relative;
        margin: 20px auto;
    }
    
    .kolam-pattern-3::before {
        content: '';
        position: absolute;
        width: 6px;
        height: 6px;
        background: #20B2AA;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        box-shadow:
            0 -25px 0 #20B2AA,
            25px -25px 0 #20B2AA,
            25px 0 0 #20B2AA,
            25px 25px 0 #20B2AA,
            0 25px 0 #20B2AA,
            -25px 25px 0 #20B2AA,
            -25px 0 0 #20B2AA,
            -25px -25px 0 #20B2AA;
        animation: twinkle 2s ease-in-out infinite;
    }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Hero section with enhanced animations */
    .hero-section {
        background: linear-gradient(135deg, 'black' 0%, #FFEAA7 50%, #E6E6FA 100%);
        padding: 80px 40px;
        text-align: center;
        border-radius: 30px;
        margin-bottom: 40px;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.6);
        position: relative;
        overflow: hidden;
        background-size: 200% 200%;
        animation: gradientShift 10s ease infinite;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,182,193,0.3) 2px, transparent 2px);
        background-size: 50px 50px;
        animation: backgroundMove 20s linear infinite;
    }
    
    @keyframes backgroundMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 5rem;
        font-weight: 900;
        color: #2C3E60;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { text-shadow: 3px 3px 6px rgba(255,255,255,0.8); }
        to { text-shadow: 3px 3px 20px rgba(255,182,193,0.6), 0 0 30px rgba(255,182,193,0.4); }
    }
    
    .hero-subtitle {
        font-family: 'Dancing Script', cursive;
        font-size: 2rem;
        color: #5D6D7E;
        font-weight: 700;
        position: relative;
        z-index: 2;
        animation: subtitleFloat 4s ease-in-out infinite;
    }
    
    @keyframes subtitleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Enhanced section styling */
    .section-container {
        margin: 40px 0;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .section-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .section-container:hover::before {
        left: 100%;
    }
    
    .section-container:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 10px 25px rgba(0,0,0,0.08);
    }
    
    .section-pink { 
        background: linear-gradient(135deg, #FFE4E1, rgba(255,255,255,0.9));
        border: 1px solid rgba(255,182,193,0.3);
    }
    .section-peach { 
        background: linear-gradient(135deg, #FFEAA7, rgba(255,255,255,0.9));
        border: 1px solid rgba(255,215,0,0.3);
    }
    .section-lavender { 
        background: linear-gradient(135deg, #E6E6FA, rgba(255,255,255,0.9));
        border: 1px solid rgba(147,112,219,0.3);
    }
    .section-mint { 
        background: linear-gradient(135deg, #E8F5E8, rgba(255,255,255,0.9));
        border: 1px solid rgba(144,238,144,0.3);
    }
    .section-blue { 
        background: linear-gradient(135deg, #E6F3FF, rgba(255,255,255,0.9));
        border: 1px solid rgba(173,216,230,0.3);
    }
    .section-coral { 
        background: linear-gradient(135deg, #FFB6C1, rgba(255,255,255,0.9));
        border: 1px solid rgba(255,182,193,0.3);
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #FF69B4, #9370DB);
        border-radius: 2px;
    }
    
    .quote-highlight {
        background: rgba(255,255,255,0.95);
        border-left: 6px solid #FF69B4;
        padding: 25px;
        margin: 25px 0;
        border-radius: 0 20px 20px 0;
        font-style: italic;
        font-size: 1.3rem;
        font-weight: 500;
        color: #2C3E50;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .quote-highlight::before {
        content: '"';
        font-size: 4rem;
        color: #FF69B4;
        opacity: 0.3;
        position: absolute;
        top: -10px;
        left: 10px;
        font-family: 'Playfair Display', serif;
    }
    
    .highlight-box {
        background: rgba(255,255,255,0.8);
        padding: 25px;
        border-radius: 20px;
        margin: 25px 0;
        border: 2px solid rgba(255,182,193,0.4);
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        backdrop-filter: blur(5px);
    }
    
    .parallax-section {
        background: linear-gradient(45deg, #E6E6FA, #E8F5E8, #FFE4E1);
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        padding: 100px 30px;
        text-align: center;
        margin: 60px 0;
        border-radius: 30px;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 0 50px rgba(255,255,255,0.3);
    }
    
    .parallax-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 50%, rgba(255,182,193,0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 50%, rgba(147,112,219,0.3) 0%, transparent 50%),
                    radial-gradient(circle at 40% 80%, rgba(144,238,144,0.3) 0%, transparent 50%);
        animation: backgroundMove 15s ease infinite;
    }
    
    .parallax-text {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        color: #2C3E50;
        font-weight: 700;
        position: relative;
        z-index: 2;
        animation: sparkle 3s ease-in-out infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { 
            transform: scale(1);
            filter: drop-shadow(0 0 10px rgba(255,182,193,0.5));
        }
        50% { 
            transform: scale(1.05);
            filter: drop-shadow(0 0 20px rgba(255,182,193,0.8));
        }
    }
    
    .emoji-large {
        font-size: 4.5rem;
        margin: 25px 0;
        display: inline-block;
        animation: bounce 2s infinite;
        filter: drop-shadow(0 5px 10px rgba(0,0,0,0.2));
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0) rotate(0deg); }
        10% { transform: translateY(-10px) rotate(5deg); }
        30% { transform: translateY(-15px) rotate(-5deg); }
        40% { transform: translateY(-10px) rotate(3deg); }
        60% { transform: translateY(-5px) rotate(-2deg); }
    }
    
    /* Enhanced interactive elements */
    .interactive-card {
        background: rgba(255,255,255,0.9);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .interactive-card:hover {
        border-color: #FF69B4;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(255,105,180,0.3);
        background: rgba(255,255,255,0.95);
    }
    
    .floating-decoration {
        position: fixed;
        pointer-events: none;
        z-index: 1;
        opacity: 0.6;
    }
    
    .floating-decoration.dot-1 {
        top: 10%;
        left: 5%;
        animation: floatUpDown 6s ease-in-out infinite;
    }
    
    .floating-decoration.dot-2 {
        top: 20%;
        right: 10%;
        animation: floatUpDown 4s ease-in-out infinite reverse;
    }
    
    .floating-decoration.dot-3 {
        bottom: 30%;
        left: 8%;
        animation: floatUpDown 5s ease-in-out infinite;
    }
    
    @keyframes floatUpDown {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title { font-size: 4.5rem; }
        .hero-subtitle { font-size: 2rem; }
        .section-title { font-size: 2.2rem; }
        .section-container { padding: 25px; margin: 25px 0; }
        .parallax-text { font-size: 2rem; }
    }
</style>
""", unsafe_allow_html=True)

# Add floating decorations
st.markdown("""
<div class="floating-decoration dot-1">
    <div class="kolam-pattern-1"></div>
</div>
<div class="floating-decoration dot-2">
    <div class="kolam-pattern-2"></div>
</div>
<div class="floating-decoration dot-3">
    <div class="kolam-pattern-3"></div>
</div>
""", unsafe_allow_html=True)

st.set_page_config(page_title="🎨 Kolam Multilingual Analyzer", layout="wide")

st.markdown("""
<div style='text-align: center;' class="hero-section"> 
    <h1 style='text-align: center;' class="hero-title"> 🎨 Kolam Art - Multilingual Analyzer </h1>
    <h3 style='color: gray;' class="hero-subtitle">  </h3>
    <br />
    <div style='margin-top: 10px;'>
        <p style='color: gray;' > Reference : Teaching Mathematics through the ART OF KOLAM  -by SYAMALA CHENULU </p>
        <p style='color: gray;' > Reference : South Indian art (Kambi Kolam)Kambi Kolam a daily mathematical activity  -by A. BRUNDA </p>
</div>
""", unsafe_allow_html=True)
preferred_language = st.selectbox("🌎 Preferred Language:", ["Auto-Detect", "English", "Hindi", "Tamil", "Telugu", "Kannada", "Malayalam"])

uploaded_file = st.file_uploader("📤 Upload Kolam Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Kolam", use_container_width=True)

query = st.text_area("Add any extra context (optional):")

KOLAM_PROMPT = """To create a powerful model that can analyze any Kolam image, we need a robust and well-structured text format that can accurately capture all the intricacies of a Kolam design, including its mathematical underpinnings. Below is an improved prompt structure in a well-formatted text, incorporating mathematical expressions for dot grid calculations and further enhancing the detail in other sections. This structure aims to be comprehensive and adaptable for various Kolam designs.
Kolam Design Analysis Report
This report provides a comprehensive analysis of a Kolam design based on its visual characteristics and underlying mathematical principles.
1. Design Identification
Name: [Name of the kolam design (e.g., '1-3-5-7-9-7-5-3-1 Parallel dots', 'Hearth Kolam')]
Origin:
Region: South India
State: Tamil Nadu
Description: [A brief description of the design, its visual characteristics, and cultural significance. For instance, "This Kolam features a symmetrical arrangement of loops and lines, often drawn during festivals to invite prosperity and positive energy."]
2. Dot Grid Structure (Pulli)
Grid Type: [The arrangement of the dots (pulli) (e.g., 'square', 'stepped', 'free shape', 'hexagonal')]
Dimensions:
For Square Grids (n x n):
n (Number of dots in a row/column): [e.g., 5]
Total Pulli (dots): n^2 = [Calculated value]
For Stepped Grids (e.g., 1-3-5-3-1):
n (Number of dots in the center row): [e.g., 5 or 9]
Total Pulli (dots): 2 * ((n-1)/2)^2 + n = [Calculated value] (This formula assumes a symmetrical stepped pattern where the number of dots increases by 2 in each step up to the center, and then decreases. For instance, for 1-3-5, n=5, total = 2*((5-1)/2)^2 + 5 = 2*(2)^2 + 5 = 8 + 5 = 13. For 1-3-5-7-5-3-1, n=7, total = 2*((7-1)/2)^2 + 7 = 2*(3)^2 + 7 = 18 + 7 = 25.)
For General/Free-Shape Grids:
Total Pulli (dots): [Calculated total number of dots based on image analysis]
3. Line Drawing Characteristics (Kambi)
Path Type: [Classification of the line drawing (e.g., 'single loop', 'multiple loops', 'interconnected patterns')]
Graph Theory Model: [Graph theory concept that applies (e.g., 'Eulerian path', 'Eulerian circuit', 'Hamiltonian Cycle', 'Traveling Salesman Problem', 'Planar Graph')]
Line Properties:
Line Style: [Type of lines used ('linear', 'curvilinear', 'combination')]
Stroke Continuity: [Is the drawing completed with a single, uninterrupted line? (True/False)]
4. Geometric Properties
Symmetry:
Type: [Type of symmetry present ('reflectional', 'rotational', 'both', 'none')]
Lines of Reflection: [Number of lines of reflection symmetry (e.g., 1, 2, 4, 8)]
Angle of Rotational Symmetry: [Smallest angle of rotational symmetry in degrees (e.g., 90, 120, 180, 360)]
Pattern Rules (Observed/Deduced):
Loop drawing-lines, and never trace a line through the same route.
The drawing is completed when all points are enclosed by a drawing-line.
Straight lines are drawn along the dual grid inclined at an angle of 45 degrees (if applicable).
Arcs are drawn surrounding the points (if applicable).
There must be symmetry in the drawings (if applicable).
[Add any other specific rules or patterns observed in the given Kolam.]
5. Graph Theory Analysis Results
Has Euler Path: [Does the design contain an Euler path? (True/False)]
Has Euler Circuit: [Does the design contain an Euler circuit? (True/False)]
Justification:
If the graph has exactly two odd vertices, it contains an Euler path.
If all vertices are even, it contains an Euler path and an Euler circuit.
[Provide a detailed explanation based on the identified number of odd and even vertices in the Kolam's underlying graph representation.]
6. Extensibility
Description: [Description of how the pattern can be extended (e.g., 'by increasing the number of dots in a uniform manner', 'by adding concentric layers', 'by repeating the base module')]
7. Cultural Context
Purpose: Decoration, a daily tribute to harmonious co-existence, a welcoming sign to all beings including the Goddess Lakshmi, an act of meditation and prayer.
Materials: White rice powder, powdered white stone, diluted rice paste, cow dung, synthetic colored powders.
Process: Drawn daily in the morning on a cleaned and dampened surface, typically at the entrance of homes.
Artisans: Traditionally drawn by women, now also practiced by men in various cultural contexts.
To make this model "powerful," the core challenge lies in the image analysis itself. An AI model for Kolam analysis would need to perform the following:
Dot Detection and Grid Inference: Accurately identify the individual dots (pulli) and determine their arrangement (square, stepped, hexagonal, or free-form).
Line Tracing and Graph Construction: Trace the lines (kambi) connecting the dots, representing them as edges in a graph where dots are vertices.
Symmetry Detection: Analyze the arrangement of dots and lines to identify various types of symmetry (reflectional, rotational).
Mathematical Calculation: Apply the appropriate formulas based on the identified grid type to calculate the total number of dots.
Graph Theory Properties: Analyze the constructed graph to determine properties like the number of odd/even vertices to infer the presence of Euler paths/circuits.
Pattern Recognition: Identify recurring motifs, line styles, and overall design principles.
Extensibility Inference: Based on the observed patterns, predict how the design could be extended.
Text Generation: Synthesize all the extracted information into the structured text format provided above.
This detailed JSON structure, combined with advanced image processing and AI pattern recognition, will enable a comprehensive analysis of any Kolam image.
"""

if st.button("🧠 Analyze with Sutra"):
    if not uploaded_file:
        st.warning("Please upload a Kolam image first.")
    else:
        full_prompt = f"{KOLAM_PROMPT}\n\nExtra context: {query}" if query.strip() else KOLAM_PROMPT
        with st.spinner("Analyzing Kolam with Sutra..."):
            try:
                response = sutra_agent.run(full_prompt).content.strip()
            except Exception:
                st.error("⚠️ Could not connect to Sutra API. Please try again later.")
                response = ""

            if response:
                # 🔎 Detect input language (if query provided)
                detected_language = "en"
                try:
                    detected_language = langdetect.detect(query) if query.strip() else "en"
                except:
                    pass

                target_language = preferred_language
                if preferred_language == "Auto-Detect":
                    lang_map = {
                        'en': 'English', 'hi': 'Hindi', 'ta': 'Tamil',
                        'te': 'Telugu', 'kn': 'Kannada', 'ml': 'Malayalam'
                    }
                    target_language = lang_map.get(detected_language, "English")

                # ✅ Show original analysis first
                st.markdown("### ✅ Kolam Analysis:")

                if target_language != "English":
                    try:
                        lang_codes = {
                            "Hindi": "hi", "Tamil": "ta", "Telugu": "te",
                            "Kannada": "kn", "Malayalam": "ml"
                        }
                        lang_code = lang_codes.get(target_language, "en")
                        translated_response = GoogleTranslator(
                            source='auto', target=lang_code
                        ).translate(response)

                        st.markdown(f"### 🌐 Translated Answer ({target_language}):")
                        st.write(translated_response)
                    except Exception as e:
                        st.warning(f"Translation unavailable: {e}")
                        st.write(response)  # fallback to English
                else:
                    # Directly show English without translation
                    st.write(response)