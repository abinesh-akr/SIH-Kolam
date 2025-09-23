import streamlit as st
from cards import blog_card, analysis_card, kolam_mastery_card, kolam_creator_card, one_on_one_card, community_card

st.set_page_config(page_title="SymetriX", layout="wide")

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
    
    .kolam-pattern-3 {
        width: 100px;
        height: 100px;
        position: relative;
        margin: 20px auto;
        animation: spin 10s linear infinite;
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
            0 -30px 0 #FF69B4,
            30px -30px 0 #9370DB,
            30px 0 0 #20B2AA,
            30px 30px 0 #FFD700,
            0 30px 0 #FF69B4,
            -30px 30px 0 #32CD32,
            -30px 0 0 #FF6347,
            -30px -30px 0 #4169E1;
    }
    
    @keyframes rotate {
        100% { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes ripple {
        0% { transform: scale(0.8); opacity: 1; }
        100% { transform: scale(2.4); opacity: 0; }
    }
    
    @keyframes spin {
        100% { transform: rotate(360deg); }
    }
    
    /* Hero section */
    .hero-section {
        position: relative;
        padding: 50px;
        text-align: center;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        margin-bottom: 40px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 5rem;
        color: #2C3E50;
        margin-bottom: 10px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-family: 'Dancing Script', cursive;
        font-size: 2.5rem;
        color: #5D6D7E;
        margin-bottom: 20px;
    }
    
    /* Floating decorations */
    .floating-decoration {
        position: absolute;
        z-index: 0;
    }
    
    .dot-1 { top: 10%; left: 10%; animation: floatUpDown 5s ease-in-out infinite; }
    .dot-2 { top: 20%; right: 10%; animation: floatUpDown 6s ease-in-out infinite; }
    .dot-3 { bottom: 10%; left: 15%; animation: floatUpDown 7s ease-in-out infinite; }
    
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

st.markdown("""
<div style='text-align: center;' class="hero-section"> 
    <div class="kolam-pattern-2"></div>  
    <div class="kolam-pattern-3"></div>
    <img src="https://ik.imagekit.io/o0nppkxow/Kolam_design_5_long%20(1).png?updatedAt=1757718152888" alt="SymetriX Banner" width="500" />
    <h1 style='text-align: center;' class="hero-title">SymetriX</h1>
    <h3 style='color: gray;' class="hero-subtitle">Infinite patterns, infinite stories.</h3>
    <br />
    <div style='margin-top: 10px;'>
        <a href='https://github.com/OmmDevgoswami/SymetriX' target='_blank' style='text-decoration: none; margin: 0 10px;'>🔗 SymetriX GitHub</a>
        <p style='color: gray;'>Built using Python - Streamlit, Pollination AI Image Generation and Sutra-multilingual model</p>
    </div>
</div>
""", unsafe_allow_html=True)

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

cols = st.columns(3)
with cols[0].container(height=380):
    blog_card()
with cols[1].container(height=380):
    analysis_card()
with cols[2].container(height=380):
    kolam_creator_card()
with cols[0].container(height=380):
    kolam_mastery_card()
with cols[1].container(height=380):
    one_on_one_card()
with cols[2].container(height=380):    
    community_card()

st.markdown("""<div class="kolam-pattern-3"></div>""", unsafe_allow_html=True)