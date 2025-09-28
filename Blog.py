import streamlit as st
import time
import math

# Page configuration
st.set_page_config(
    page_title="Kolam - Ancient Art of South India",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with mobile media query
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
    width: 10px;
    height: 10px;
    background: radial-gradient(circle, #3B82F6, transparent);
    border-radius: 50%;
    animation: floatPulse 5s ease-in-out infinite;
}

.dot-1 { top: 10%; left: 5%; animation-delay: 0s; }
.dot-2 { top: 20%; right: 10%; animation-delay: 1.5s; }
.dot-3 { bottom: 15%; left: 15%; animation-delay: 3s; }

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
    font-size: 4.5rem;
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

/* Section container */
.section-container {
    background: #F8FAFC;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}

.section-container:hover {
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    background: linear-gradient(135deg, #F8FAFC, #DBEAFE);
}

.section-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(147, 197, 253, 0.3), transparent);
    transition: 0.5s;
}

.section-container:hover::before {
    left: 100%;
}

/* Section title */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
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
    width: 60px;
    height: 4px;
    background: linear-gradient(90deg, #1E3A8A, #3B82F6);
    border-radius: 2px;
}

/* Quote highlight */
.quote-highlight {
    font-family: 'Lato', sans-serif;
    font-style: italic;
    color: #2C3E50;
    text-align: center;
    margin: 2rem 0;
    padding: 1rem 2rem;
    background: rgba(59, 130, 246, 0.1);
    border-radius: 10px;
    border-left: 5px solid #3B82F6;
    animation: fadeIn 2s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Highlight box */
.highlight-box {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
    margin: 1rem 0;
}

/* Interactive card */
.interactive-card {
    background: #FFFFFF;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.4s ease;
    cursor: pointer;
    font-family: 'Lato', sans-serif;
    color: #2C3E50;
    text-align: center;
    min-width: 150px;
}

.interactive-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    background: linear-gradient(135deg, #F8FAFC, #DBEAFE);
}

/* Responsive design for tablets */
@media (max-width: 768px) {
    .hero-title { font-size: 3rem; }
    .hero-subtitle { font-size: 1.2rem; }
    .section-title { font-size: 2rem; }
    .main-content { padding: 1rem; }
    .section-container { padding: 1.5rem; }
    .interactive-card { min-width: 120px; padding: 0.8rem 1rem; }
    .quote-highlight { padding: 0.8rem 1.2rem; }
}

/* Responsive design for mobile phones */
@media (max-width: 576px) {
    .main-content { padding: 0.8rem; margin-top: 120px; }
    .hero-section { padding: 1.5rem; }
    .hero-title { font-size: 2.2rem; }
    .hero-subtitle { font-size: 1rem; }
    .section-container { padding: 1rem; margin: 0.5rem 0; }
    .section-title { font-size: 1.6rem; }
    .section-title::after { width: 40px; height: 3px; }
    .quote-highlight { font-size: 0.9rem; padding: 0.6rem 1rem; margin: 1rem 0; }
    .highlight-box { gap: 0.5rem; }
    .interactive-card { min-width: 100%; padding: 0.6rem 0.8rem; font-size: 0.85rem; }
    .floating-dot { width: 8px; height: 8px; }
}
</style>
""", unsafe_allow_html=True)





# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="floating-dot dot-1"></div>
    <div class="floating-dot dot-2"></div>
    <div class="floating-dot dot-3"></div>
    <h1 class="hero-title">Kolam - Ancient Art of South India</h1>
    <p class="hero-subtitle">A beautiful tradition of designs, culture, and mathematics</p>
</div>
""", unsafe_allow_html=True)

# Introduction Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🌟 What is Kolam?</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="floating-dot dot-1"></div>', unsafe_allow_html=True)

with col2:
    st.write("""
    Kolam is a traditional art form from South India, drawn by women in front of their homes every morning. Made with rice flour or chalk, it creates beautiful patterns using dots and lines. It is a symbol of welcome and prosperity.
    """)

with col3:
    st.markdown('<div class="floating-dot dot-2"></div>', unsafe_allow_html=True)

st.markdown('<div class="quote-highlight">"Kolam is a daily ritual that connects us to our ancestors and brings positive energy to our homes."</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# History Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📜 The Rich History of Kolam</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="floating-dot dot-3"></div>', unsafe_allow_html=True)

with col2:
    st.write("""
    Kolam dates back to the Indus Valley Civilization (over 4,000 years ago). It is mentioned in ancient Tamil literature like the Sangam poems. In Hindu tradition, it is said to invite Goddess Lakshmi into the home.
    """)

    st.markdown("""
    <div class="highlight-box">
    <p><strong>Key Historical Facts:</strong></p>
    <div class="interactive-card">🏛️ Indus Valley origins</div>
    <div class="interactive-card">📖 Sangam literature mentions</div>
    <div class="interactive-card">🕉️ Linked to Hindu rituals</div>
    <div class="interactive-card">🌍 Regional variations across South India</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown('<div class="floating-dot dot-1"></div>', unsafe_allow_html=True)

st.markdown('<div class="quote-highlight">Kolam has evolved from simple patterns to complex designs over centuries.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Cultural Significance Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🕉️ Cultural and Spiritual Significance</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="floating-dot dot-2"></div>', unsafe_allow_html=True)

with col2:
    st.write("""
    Kolam is more than art—it's a spiritual practice. It represents:
    - **Prosperity**: Inviting wealth and good luck
    - **Protection**: Warding off evil spirits
    - **Harmony**: Connecting with nature and cosmos
    - **Community**: Shared during festivals
    """)

with col3:
    st.markdown('<div class="floating-dot dot-3"></div>', unsafe_allow_html=True)

st.markdown('<div class="quote-highlight">In many homes, drawing Kolam is the first act of the day, setting a positive tone.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mathematical Beauty Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📐 The Mathematical Beauty of Kolam</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="floating-dot dot-1"></div>', unsafe_allow_html=True)

with col2:
    st.write("""
    Kolam designs are based on mathematical principles:
    - **Symmetry**: Rotational and reflection symmetry
    - **Geometry**: Dots connected with curves and lines
    - **Graph Theory**: Some Kolams relate to Eulerian paths
    - **Fractals**: Complex patterns show self-similarity
    """)

with col3:
    st.markdown('<div class="floating-dot dot-2"></div>', unsafe_allow_html=True)

st.markdown('<div class="quote-highlight">Kolam connects ancient tradition with modern science.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Essence Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">✅ The Essence of Kolam</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="floating-dot dot-3"></div>', unsafe_allow_html=True)

with col2:
    st.write("""
    Kolam is a beautiful, ancient, living art form from South India. It is drawn every day with rice flour in front of homes. It is thousands of years old, both a cultural tradition and a spiritual practice.
    """)

    st.markdown("""
    <div class="highlight-box">
    <p><strong>It is not just decoration—it is about:</strong></p>
    <div class="interactive-card">🌟 Inviting good fortune</div>
    <div class="interactive-card">🛡️ Protecting the home</div>
    <div class="interactive-card">🌿 Respecting nature</div>
    <div class="interactive-card">🧘 Practicing discipline</div>
    <div class="interactive-card">🎨 Celebrating art and mathematics together</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown('<div class="floating-dot dot-1"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="quote-highlight">
<strong>👉 In one line: Kolam is the art where dots, lines, faith, and mathematics meet on the doorstep of every home.</strong>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interactive Kolam Gallery Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🎨 Interactive Kolam Gallery</h2>', unsafe_allow_html=True)

st.write("Experience the beauty of different Kolam patterns:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="interactive-card" style="text-align: center; padding: 30px;">
        <div class="floating-dot dot-1"></div>
        <strong>Dot Pattern Kolam</strong><br>
        <small>Traditional grid-based design</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="interactive-card" style="text-align: center; padding: 30px;">
        <div class="floating-dot dot-2"></div>
        <strong>Circular Kolam</strong><br>
        <small>Ripple effect design</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="interactive-card" style="text-align: center; padding: 30px;">
        <div class="floating-dot dot-3"></div>
        <strong>Star Kolam</strong><br>
        <small>Twinkling star pattern</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="interactive-card" style="text-align: center; padding: 30px;">
        <div class="floating-dot dot-1"></div>
        <strong>Festival Kolam</strong><br>
        <small>Special occasion design</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="
    text-align: center; 
    padding: 2rem; 
    background: #1E3A8A; 
    color: #EFF6FF; 
    font-family: 'Lato', sans-serif;
    margin-top: 2rem;
    border-radius: 15px;
    position: relative;
">
    <div class="floating-dot dot-1"></div>
    <p style="
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 1rem;
    ">
        Thank you for exploring the beautiful world of Kolam
    </p>
    <div class="floating-dot dot-2"></div>
    <p style="
        font-style: italic;
    ">
        "Where ancient wisdom meets modern wonder"
    </p>
</div>
""", unsafe_allow_html=True)

# Add interactive elements with JavaScript
st.markdown("""
<script>
// Add some interactive hover effects
document.addEventListener('DOMContentLoaded', function() {
    // Add click effect to interactive cards
    const cards = document.querySelectorAll('.interactive-card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'translateY(-5px)';
            }, 100);
        });
    });
    
    // Add parallax effect to hero section
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            heroSection.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
});
</script>
""", unsafe_allow_html=True)
