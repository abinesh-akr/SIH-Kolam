import streamlit as st
from PIL import Image
import pandas as pd
import cv2
import numpy as np
import time
import io
from skimage.metrics import structural_similarity as ssim
from skimage import filters
import math
import random
from streamlit_drawable_canvas import st_canvas
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from dotenv import load_dotenv
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import langdetect
from deep_translator import GoogleTranslator
import os
from google import genai  # Assuming this is google-generativeai
import json

# Load environment variables
load_dotenv()

# API Keys (replace with your actual keys if needed)
SUTRA_API_KEY = os.getenv("SUTRA_API_KEY", "sutra_1p8L5c8EmR1gUrtXbmw20kmYzS0GDC2Tq7a86U8pPTNmW6UUz0psboTmC5NK")
GEMINI_API_KEY = "AIzaSyBMThlSDjHMjrCsfxu8bjUZ8VBkDkCYKHg"

# Set up models
sutra_model = OpenAILike(
    id="sutra-v2",
    api_key=SUTRA_API_KEY,
    base_url="https://api.two.ai/v2",
    extra_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
)

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

genai.configure(api_key=GEMINI_API_KEY)  # Assuming google-generativeai setup

# Custom Blue Theme CSS with advanced animations and user-friendly design
blue_theme_css = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lato:wght@300;400;600;700&family=Dancing+Script:wght@400;700&display=swap');
    
    /* Hide Streamlit default elements */
    footer {visibility: hidden;}
    
    /* Main container styling */
    .main > div {
        padding-top: 1rem;
    }
    
    /* Animated blue background */
    body {
        background: linear-gradient(-45deg, #E0F7FA, #BBDEFB, #E3F2FD, #B3E5FC);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated Kolam patterns in blue theme */
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
        background: #3498DB;
        border-radius: 50%;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 
            0 15px 0 #3498DB,
            0 30px 0 #3498DB,
            0 45px 0 #3498DB,
            15px 7.5px 0 #2980B9,
            15px 22.5px 0 #2980B9,
            15px 37.5px 0 #2980B9,
            -15px 7.5px 0 #2980B9,
            -15px 22.5px 0 #2980B9,
            -15px 37.5px 0 #2980B9;
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
        border: 3px solid #2980B9;
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
        border: 2px solid #3498DB;
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
        background: #1ABC9C;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        box-shadow:
            0 -25px 0 #1ABC9C,
            25px -25px 0 #1ABC9C,
            25px 0 0 #1ABC9C,
            25px 25px 0 #1ABC9C,
            0 25px 0 #1ABC9C,
            -25px 25px 0 #1ABC9C,
            -25px 0 0 #1ABC9C,
            -25px -25px 0 #1ABC9C;
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
        text-align: center;
        padding: 50px 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(52,152,219,0.2);
        animation: fadeIn 1.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        color: #1A237E;
        margin: 20px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .hero-subtitle {
        font-family: 'Dancing Script', cursive;
        font-size: 2rem;
        color: #34495E;
        margin-bottom: 30px;
    }
    
    @keyframes glow {
        0% { 
            text-shadow: 0 0 10px rgba(52,152,219,0.5);
        }
        50% { 
            text-shadow: 0 0 20px rgba(52,152,219,0.8);
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
        border-color: #3498DB;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(52,152,219,0.3);
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
    
    /* Button styling */
    button {
        background-color: #3498DB !important;
        color: white !important;
    }
    
    button:hover {
        background-color: #2980B9 !important;
    }
</style>
"""

# Inject CSS
st.markdown(blue_theme_css, unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="AnantaKolam", layout="wide", page_icon="🌸")

# Tabs for new single-page structure
tab_names = ["Home", "Heritage & Culture", "Decoder", "Drawing Teacher", "Classifier", "Generator", "Canva & Brush", "One-on-One", "Community"]
tabs = st.tabs(tab_names)

# Define card functions (from cards.py, adapted for blue theme)
def analysis_card():
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Analysis Results</h3>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Drag and drop your kolam image here, or click to browse",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        help="Upload a high-quality image of what you think might be a kolam art pattern"
    )
    analyze_button = st.button("🔍 Analyze Kolam Pattern", type="primary", use_container_width=True)
    if analyze_button and uploaded_file:
        with st.spinner("🧠 Analyzing patterns and cultural significance..."):
            # Placeholder for analysis (adapt from original)
            st.success("Analysis complete!")  # Replace with actual logic
    st.markdown('</div>', unsafe_allow_html=True)

def blog_card():
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    st.markdown('<h3>🪔 What is Kolam?</h3>', unsafe_allow_html=True)
    st.write("Kolam is a traditional floor art practiced in Tamil Nadu...")
    st.markdown('</div>', unsafe_allow_html=True)

def kolam_generator_card():
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    st.markdown("<h3>🖌️ Kolam Kraziness</h3>", unsafe_allow_html=True)
    st.markdown("<p>Click generate and watch your Kolam dots dance! 🌸✨</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def kolam_canva_card():
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    st.markdown("<h3>Canvas & Brush Settings</h3>", unsafe_allow_html=True)
    # Add canva controls
    st.markdown('</div>', unsafe_allow_html=True)

def kolam_teacher_card():
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    st.markdown("<h3>✍️ Kolam Drawing Teacher</h3>", unsafe_allow_html=True)
    st.info("Watch the magic of technology meet tradition!")
    st.markdown('</div>', unsafe_allow_html=True)

def kolam_classifier_card():
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    st.markdown("<h3>🔎 Kolam Classifier</h3>", unsafe_allow_html=True)
    st.info("Discover the type of Kolam with our AI-powered classifier!")
    st.markdown('</div>', unsafe_allow_html=True)

def one_on_one_card():
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    st.markdown("<h3>Kolam Masters</h3>", unsafe_allow_html=True)
    choice = st.selectbox("Design that Speaks your Mind:", ("Traditional Pulli Kolam", "Sikku Kolam", "Kavi Kolam"))
    st.markdown('</div>', unsafe_allow_html=True)

def community_card():
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    st.markdown("<h3>🌐 Join Our Kolam Community!</h3>", unsafe_allow_html=True)
    st.button("Join Now", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Home Tab (from Home.py)
with tabs[0]:
    st.markdown("""
    <div style='text-align: center;' class="hero-section"> 
        <div class="kolam-pattern-2"></div>  
        <div class="kolam-pattern-3"></div>
        <img src="https://ik.imagekit.io/o0nppkxow/Kolam_design_5_long%20(1).png?updatedAt=1757718152888" alt="AnantaKolam Banner" width = "500" />
        <h1 class="hero-title"> AnantaKolam </h1>
        <h3 class="hero-subtitle"> Infinite patterns, infinite stories. </h3>
        <br />
        <div style='margin-top: 10px;'>
            <a href='https://github.com/OmmDevgoswami/AnantaKolam' target='_blank' style='text-decoration: none; margin: 0 10px;'>🔗 AnantaKolam GitHub</a>
            <p style='color: gray;' > Built using Python - Streamlit, Pollination AI Image Generation and Sutra-multilingual model </p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    with cols[0]:
        blog_card()
    with cols[1]:
        analysis_card()
    with cols[2]:
        kolam_generator_card()
    with cols[0]:
        kolam_canva_card()
    with cols[1]:
        one_on_one_card()
    with cols[2]:
        community_card()

# Heritage & Culture Tab (from Blog.py)
with tabs[1]:
    # Add code from Blog.py here (not provided in full, placeholder)
    st.title("Kolam: Heritage & Culture")
    st.write("Content about Kolam heritage...")

# Decoder Tab (from Analysis.py)
with tabs[2]:
    st.title("Kolam Decoder")
    # Copy code from Analysis.py
    KOLAM_PROMPT = """..."""  # Paste the full prompt
    uploaded_file = st.file_uploader("Upload Kolam Image", type=["jpg", "png"])
    # Rest of the code...

# Drawing Teacher Tab (from Kolam_Teacher.py)
with tabs[3]:
    st.title("Kolam Drawing Teacher")
    # Copy code from Kolam_Teacher.py
    uploaded_file = st.file_uploader("Choose a Kolam image...", type=["jpg", "jpeg", "png"])
    # Rest of the code... (assume kolam_processing is handled externally)

# Classifier Tab (from Kolam_Classifier.py)
with tabs[4]:
    st.title("Kolam Classifier")
    # Copy code from Kolam_Classifier.py
    from kolam_classifier_logic import load_model, predict  # Assume external
    from kolam_descriptions import get_description  # Assume external
    uploaded_file = st.file_uploader("Choose a Kolam image...", type=["jpg", "jpeg", "png"])
    # Rest of the code...

# Generator Tab (from Kolam_Generator.py)
with tabs[5]:
    st.title("Kolam Generator")
    # Copy code from Kolam_Generator.py
    def catmull_rom_spline(P0, P1, P2, P3, nPoints=20):
        # Full function...
    # Rest of the code...
    # Canva & Brush Tab (from kolam_Canva.py)
with tabs[6]:
    st.title("Kolam: Canva and Brush")
    # Copy code from kolam_Canva.py
    canvas_result = st_canvas()
    # Rest of the code...

# One-on-One Tab (from Special_One_on_One.py, assuming from cards)
with tabs[7]:
    st.title("Special One-on-One")
    one_on_one_card()

# Community Tab (from Community.py, assuming from cards)
with tabs[8]:
    st.title("Kolam Community")
    community_card()

# Footer
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #3498DB; color: white;">
    Built with passion by Team Ellipsis 🐦‍🔥🌠
</div>
""", unsafe_allow_html=True)