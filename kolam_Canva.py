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

# Custom CSS with animated Kolam patterns and enhanced visuals
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
        background: linear-gradient(135deg, #FFE4E1 0%, #FFEAA7 50%, #E6E6FA 100%);
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
        color: #2C3E50;
        margin-bottom: 1rem;
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

# Enhanced Hero Section
st.markdown("""
<div class="hero-section">
    <div class="kolam-pattern-2"></div>
    <div class="emoji-large">🌸</div>
    <h1 class="hero-title">Kolam</h1>
    <p class="hero-subtitle">The Ancient Art Where Dots, Lines, Faith, and Mathematics Meet</p>
    <div class="kolam-pattern-1"></div>
</div>
""", unsafe_allow_html=True)

# Enhanced Introduction Section
st.markdown('<div class="section-container section-pink">', unsafe_allow_html=True)
st.markdown('<div class="kolam-pattern-3"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🌸 A Morning Ritual of Beauty</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.write("""
    Imagine this: it's early morning in a South Indian village. The sun is not yet up, the ground is cool and freshly washed with water, and you see women bending down in front of their homes with a small bowl of white powder in their hands. 
    
    Slowly, dot by dot, line by line, they create stunning patterns on the ground. By the time the street wakes up, the entire road looks decorated with lace-like white drawings.
    """)

with col2:
    st.markdown('<div class="kolam-pattern-2"></div>', unsafe_allow_html=True)

st.markdown('<div class="quote-highlight">This is called a <strong>Kolam</strong>.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Enhanced What is Kolam Section
st.markdown('<div class="section-container section-peach">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🪔 What is Kolam?</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown('<div class="kolam-pattern-1"></div>', unsafe_allow_html=True)
    st.markdown('<div class="kolam-pattern-3"></div>', unsafe_allow_html=True)

with col2:
    st.write("""
    Kolam is a traditional floor art practiced in Tamil Nadu and across South India for thousands of years. It is made using rice flour, chalk powder, or sometimes colored powders.

    The designs are usually based on a grid of dots, which are then connected with curves, loops, and lines to form symmetrical and geometric patterns.
    """)

st.markdown("""
<div class="highlight-box">
<strong>You can think of Kolam as something between art, meditation, and mathematics.</strong>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Parallax Section
st.markdown("""
<div class="parallax-section">
    <div class="kolam-pattern-2"></div>
    <div class="parallax-text">✨ Over 5,000 Years of Continuous Tradition ✨</div>
    <div class="kolam-pattern-1"></div>
</div>
""", unsafe_allow_html=True)

# Enhanced Ancient Origins Section
st.markdown('<div class="section-container section-lavender">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📅 Ancient Origins</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown('<div class="kolam-pattern-3"></div>', unsafe_allow_html=True)
    
with col2:
    st.write("Kolam is incredibly ancient:")
    
    st.markdown("""
    <div class="interactive-card">
    <strong>🏛️ Indus Valley Civilization</strong><br>
    Archaeologists have found designs similar to Kolam from around 2500 BCE—that's more than 4,500 years ago.
    </div>
    
    <div class="interactive-card">
    <strong>📚 Tamil Sangam Literature</strong><br>
    From 500 BCE–300 CE describes women drawing patterns outside their houses.
    </div>
    
    <div class="interactive-card">
    <strong>🏛️ Medieval Temples</strong><br>
    Around the 10th century CE, temple carvings show Kolam-like patterns.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown('<div class="kolam-pattern-2"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="quote-highlight">
Kolam is at least 2,000 years old by literature and possibly 5,000 years old by archaeology. It is one of the oldest continuous art traditions in the world.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Deep Meaning Section
st.markdown('<div class="section-container section-mint">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">❓ The Deep Meaning Behind Kolam</h2>', unsafe_allow_html=True)
st.markdown('<div class="kolam-pattern-1" style="margin-bottom: 30px;"></div>', unsafe_allow_html=True)

st.write("Kolam may look like just decoration, but it has many layers of meaning:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="interactive-card">
    <strong>🙏 Spiritual Meaning</strong><br>
    • Invites Goddess Lakshmi into the house<br>
    • Form of daily prayer and devotion
    </div>
    
    <div class="interactive-card">
    <strong>🛡️ Protective Purpose</strong><br>
    • Symbolic barrier against evil spirits<br>
    • Keeps away negative energies
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="kolam-pattern-2"></div>', unsafe_allow_html=True)
    
with col3:
    st.markdown("""
    <div class="interactive-card">
    <strong>🏠 Hospitality</strong><br>
    • Shows the house is welcoming<br>
    • Invitation for guests
    </div>
    
    <div class="interactive-card">
    <strong>🐜 Ecological Purpose</strong><br>
    • Made with rice flour for insects and birds<br>
    • Sharing food with nature
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="interactive-card" style="margin-top: 20px;">
<strong>🧘 Personal Discipline</strong><br>
• Requires patience and steady hands • Daily practice of mindfulness • Training focus and creativity
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Art of Creation Section
st.markdown('<div class="section-container section-blue">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📝 The Art of Creation</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.write("The process itself is very systematic:")

    st.markdown("""
    <div class="highlight-box">
    <h3>The Four Steps:</h3>
    <div class="interactive-card">
    <strong>1. Cleaning the Ground:</strong> The entrance is swept and washed in the early morning. Sometimes cow dung mixed with water is spread to purify the space.
    </div>

    <div class="interactive-card">
    <strong>2. Dot Grid:</strong> A series of dots are placed in a pattern (rows, triangles, or circles).
    </div>

    <div class="interactive-card">
    <strong>3. Drawing Lines:</strong> The artist connects these dots with continuous loops, curves, and lines.
    </div>

    <div class="interactive-card">
    <strong>4. Adding Details:</strong> Some designs are left plain; some are filled with color during festivals.
    </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="kolam-pattern-3"></div>', unsafe_allow_html=True)
    st.markdown('<div class="kolam-pattern-1"></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="interactive-card">
    <strong>🔸 Pulli Kolam:</strong> Made using dot grids
    </div>
    <div class="interactive-card">
    <strong>🔸 Sikku Kolam:</strong> Knot-like, with lines weaving around dots
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="interactive-card">
    <strong>🔸 Kavi Kolam:</strong> Red background with white powder, used in temples
    </div>
    <div class="interactive-card">
    <strong>🔸 Freehand Kolam:</strong> Floral or symbolic designs drawn without dots
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Sacred Moments Section
st.markdown('<div class="section-container section-coral">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🌸 Sacred Moments</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="kolam-pattern-2"></div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="interactive-card">
    <strong>🌅 Daily Practice</strong><br>
    Women wake up before sunrise to draw Kolam at the doorstep as part of starting the day.
    </div>
    
    <div class="interactive-card">
    <strong>🎉 Festivals</strong><br>
    On Pongal (January harvest festival), large, colorful Kolams cover entire streets.
    </div>
    
    <div class="interactive-card">
    <strong>💒 Weddings</strong><br>
    Special Kolams are drawn with symbols of fertility, prosperity, and good luck.
    </div>
    
    <div class="interactive-card">
    <strong>🏛️ Temples & Ceremonies</strong><br>
    Kolams are drawn on temple floors during rituals and festivals.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown('<div class="kolam-pattern-3"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Mathematics Section
st.markdown('<div class="section-container section-lavender">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🧮 Kolam Meets Modern Science</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="kolam-pattern-1"></div>', unsafe_allow_html=True)

with col2:
    st.write("One of the most fascinating aspects of Kolam is that it is not only artistic but also mathematical:")

    st.markdown("""
    <div class="highlight-box">
    <div class="interactive-card">
    • The designs use <strong>symmetry, geometry, and repetition</strong>
    </div>
    <div class="interactive-card">
    • The dots and lines can be explained with <strong>algorithms</strong>—step-by-step instructions, like computer code
    </div>
    <div class="interactive-card">
    • Scientists today study Kolam using <strong>graph theory and fractals</strong>
    </div>
    <div class="interactive-card">
    • Kolam is now being used in <strong>computer science, AI, and design automation</strong> as a way of understanding patterns
    </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown('<div class="kolam-pattern-2"></div>', unsafe_allow_html=True)

st.markdown('<div class="quote-highlight">So Kolam connects ancient tradition with modern science.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Final Section
st.markdown('<div class="section-container section-pink">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">✅ The Essence of Kolam</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="kolam-pattern-3"></div>', unsafe_allow_html=True)

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
    st.markdown('<div class="kolam-pattern-1"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="quote-highlight">
<strong>👉 In one line: Kolam is the art where dots, lines, faith, and mathematics meet on the doorstep of every home.</strong>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interactive Kolam Gallery Section
st.markdown('<div class="section-container section-peach">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🎨 Interactive Kolam Gallery</h2>', unsafe_allow_html=True)

st.write("Experience the beauty of different Kolam patterns:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="interactive-card" style="text-align: center; padding: 30px;">
        <div class="kolam-pattern-1"></div>
        <strong>Dot Pattern Kolam</strong><br>
        <small>Traditional grid-based design</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="interactive-card" style="text-align: center; padding: 30px;">
        <div class="kolam-pattern-2"></div>
        <strong>Circular Kolam</strong><br>
        <small>Ripple effect design</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="interactive-card" style="text-align: center; padding: 30px;">
        <div class="kolam-pattern-3"></div>
        <strong>Star Kolam</strong><br>
        <small>Twinkling star pattern</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="interactive-card" style="text-align: center; padding: 30px;">
        <div class="kolam-pattern-1" style="animation-direction: reverse;"></div>
        <strong>Festival Kolam</strong><br>
        <small>Special occasion design</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer with more animations
st.markdown("""
<div style="
    text-align: center; 
    padding: 60px 40px; 
    background: linear-gradient(135deg, #E8F5E8, #E6F3FF, #FFE4E1); 
    background-size: 300% 300%;
    animation: gradientShift 10s ease infinite;
    margin-top: 40px; 
    border-radius: 30px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.1);
">
    <div class="kolam-pattern-2"></div>
    <div style="font-size: 4rem; margin-bottom: 30px; animation: bounce 2s infinite; filter: drop-shadow(0 5px 15px rgba(0,0,0,0.2));">🌸✨🪔</div>
    <p style="
        font-family: 'Dancing Script', cursive; 
        color: #2C3E50; 
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 20px;
        animation: subtitleFloat 4s ease-in-out infinite;
    ">
        Thank you for exploring the beautiful world of Kolam
    </p>
    <div class="kolam-pattern-1"></div>
    <p style="
        font-family: 'Lato', sans-serif; 
        color: #5D6D7E; 
        font-size: 1.1rem;
        font-style: italic;
        margin-top: 20px;
    ">
        "Where ancient wisdom meets modern wonder"
    </p>
    <div class="kolam-pattern-3"></div>
</div>
""", unsafe_allow_html=True)

# Add some interactive elements with JavaScript
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
