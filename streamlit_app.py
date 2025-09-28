import streamlit as st
from cards import blog_card, analysis_card, kolam_creator_card, kolam_mastery_card, one_on_one_card, community_card

# Set page configuration
st.set_page_config(page_title="SymmetriX", layout="wide")

# Define pages for navigation
pages = [
    st.Page("Home.py", title="Home", icon=":material/home:"),
    st.Page("Blog.py", title="Kolam: Heritage & Culture", icon=":material/auto_stories:"),
    st.Page("Kolam_Insights.py", title="Kolam Insights", icon=":material/analytics:"),
    st.Page("Kolam_Mastery.py", title="Kolam Mastery", icon=":material/edit:"),
    st.Page("Kolam_Creator.py", title="Kolam Creator", icon=":material/draw_collage:"),
    st.Page("Special_One_on_One.py", title="Special One-on-One", icon=":material/person_raised_hand:"),
    st.Page("Community.py", title="Kolam Community", icon=":material/diversity_3:")
]

# Run navigation
page = st.navigation(pages,position="top")
page.run()

# Custom CSS for blue-themed navbar and new animations
st.markdown("""
<style>
/* Reset default styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Hide Streamlit default footer */
footer {visibility: hidden;}

/* Navbar styling */
.navbar {
    background: linear-gradient(90deg, #1E3A8A, #3B82F6);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    position: fixed;
    top: 0;
    width: 1350px;
    z-index: 1000;
            margin-top:50px}
            margin-left:-100px

/* Navbar links */
.nav-links {
    display: flex;
    gap: 1.5rem;
}

.nav-links a {
    color: #EFF6FF;
    text-decoration: none;
    font-family: 'Lato', sans-serif;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    transition: all 0.3s ease;
    position: relative;
}

.nav-links a:hover {
    color: #93C5FD;
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(147, 197, 253, 0.5);
}

/* Floating dot animation for navbar */
.nav-links a::before {
    content: '';
    position: absolute;
    width: 6px;
    height: 6px;
    background: #93C5FD;
    border-radius: 50%;
    top: -8px;
    left: 50%;
    transform: translateX(-50%);
    opacity: 0;
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.nav-links a:hover::before {
    opacity: 1;
    transform: translate(-50%, -10px);
}

/* Logo and title */
.navbar-logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.navbar-logo img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    transition: transform 0.5s ease;
}

.navbar-logo img:hover {
    transform: rotate(360deg) scale(1.1);
}

.navbar-logo h1 {
    color: #EFF6FF;
    font-family: 'Lato', sans-serif;
    font-size: 1.5rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Main content */
.main-content {
    margin-top: 80px;
    padding: 2rem;
    background: linear-gradient(135deg, #DBEAFE, #EFF6FF);
    min-height: 100vh;
    position: relative;
    overflow: hidden;
}

/* Floating Kolam dots animation */
.floating-dot {
    position: absolute;
    width: 10px;
    height: 10px;
    background: radial-gradient(circle, #3B82F6, transparent);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
}

.dot-1 { top: 10%; left: 5%; animation-delay: 0s; }
.dot-2 { top: 20%; right: 10%; animation-delay: 1s; }
.dot-3 { bottom: 15%; left: 15%; animation-delay: 2s; }

@keyframes float {
    0%, 100% { transform: translateY(0); opacity: 0.7; }
    50% { transform: translateY(-20px); opacity: 1; }
}

/* Card container */
.card-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    padding: 1rem;
}

/* Card styling with glow animation */
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

/* Card glow effect */
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

/* Footer */
.footer {
    text-align: center;
    padding: 1rem;
    background: #1E3A8A;
    color: #EFF6FF;
    font-family: 'Lato', sans-serif;
    margin-top: 2rem;
    position: relative;
}

/* Responsive design */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 1rem;
    }
    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
    }
    .navbar-logo h1 {
        font-size: 1.2rem;
    }
}
</style>
""", unsafe_allow_html=True)




# Footer
st.markdown("""
<div class="footer">
    Built with passion by Team SymmetriX :)
</div>
""", unsafe_allow_html=True)
