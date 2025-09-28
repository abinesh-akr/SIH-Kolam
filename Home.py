import streamlit as st
from cards import blog_card, analysis_card, kolam_mastery_card, kolam_creator_card, one_on_one_card, community_card

# Set page configuration
st.set_page_config(page_title="SymmetriX", layout="wide")

# Custom CSS for blue-themed layout and new animations
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

/* Main container styling */
.main > div {
    padding-top: 1rem;
}

/* Hero section */
.hero-section {
    position: relative;
    padding: 3rem;
    text-align: center;
    background: linear-gradient(135deg, #DBEAFE, #EFF6FF);
    border-radius: 15px;
    margin: 5rem 2rem 2rem 2rem;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    overflow: hidden;
}

/* Hero title and subtitle */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 4.5rem;
    color: #1E3A8A;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); }
    to { text-shadow: 0 2px 8px rgba(59, 130, 246, 0.5); }
}

.hero-subtitle {
    font-family: 'Lato', sans-serif;
    font-size: 2rem;
    color: #3B82F6;
    margin-bottom: 1rem;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* Floating Kolam dots */
.floating-decoration {
    position: absolute;
    width: 12px;
    height: 12px;
    background: radial-gradient(circle, #3B82F6, transparent);
    border-radius: 50%;
    animation: floatPulse 5s ease-in-out infinite;
}

.dot-1 { top: 10%; left: 5%; animation-delay: 0s; }
.dot-2 { top: 15%; right: 5%; animation-delay: 1.5s; }
.dot-3 { bottom: 10%; left: 10%; animation-delay: 3s; }

@keyframes floatPulse {
    0%, 100% { transform: translateY(0) scale(1); opacity: 0.7; }
    50% { transform: translateY(-15px) scale(1.2); opacity: 1; }
}

/* Card container */
.card-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 6.5rem;
    padding: 6rem;
    background: #F8FAFC;
}

/* Card styling */
.card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    background: linear-gradient(135deg, #F8FAFC, #DBEAFE);
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(147, 197, 253, 0.3), transparent);
    transition: 0.5s;
}

.card:hover::before {
    left: 100%;
}

/* Responsive design */
@media (max-width: 768px) {
    .hero-title { font-size: 3rem; }
    .hero-subtitle { font-size: 1.5rem; }
    .hero-section { padding: 2rem; margin: 4rem 1rem 1rem 1rem; }
    .card-container { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero-section">
    <div class="floating-decoration dot-1"></div>
    <div class="floating-decoration dot-2"></div>
    <div class="floating-decoration dot-3"></div>
    <img src="banner.png" alt="SymmetriX Banner" width="400" />
    <h1 class="hero-title">SymmetriX</h1>
    <h3 class="hero-subtitle">Infinite patterns, infinite stories.</h3>
    <p style='color: #1E3A8A; font-family: Lato, sans-serif;'>Built using Python - Streamlit, Pollination AI Image Generation, and Sutra-multilingual model</p>
    <a href='https://github.com/OmmDevgoswami/SymetriX' target='_blank' style='color: #3B82F6; text-decoration: none; font-family: Lato, sans-serif; font-weight: 500;'>🔗 SymetriX GitHub</a>
</div>
""", unsafe_allow_html=True)

# Card container
st.markdown('<div class="card-container">', unsafe_allow_html=True)

# Display all cards
blog_card()
analysis_card()
kolam_creator_card()
kolam_mastery_card()
one_on_one_card()
community_card()

st.markdown('</div>', unsafe_allow_html=True)
