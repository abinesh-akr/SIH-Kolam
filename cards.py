import streamlit as st
from PIL import Image

def blog_card():
    st.page_link(page="Blog.py", label="Kolam: Heritage & Culture", icon=":material/auto_stories:")
    st.markdown('<h2 class="section-header">📜 Kolam: Heritage & Culture</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="interactive-card" style='
        background: linear-gradient(135deg, #FFE4E1, #E6E6FA);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease-in-out;
        cursor: pointer;
    '>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Explore the rich history, cultural significance, and mathematical beauty of Kolam art. Learn about regional variations and their stories.
        </p>
    </div>
    """, unsafe_allow_html=True)

def analysis_card():
    st.page_link(page="Kolam_Insights.py", label="Kolam Insights", icon=":material/analytics:")
    st.markdown('<h2 class="section-header">🔍 Kolam Insights</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="interactive-card" style='
        background: linear-gradient(135deg, #E8F5E8, #FFEAA7);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease-in-out;
        cursor: pointer;
    '>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Uncover the design principles of Kolams with AI-driven analysis and classification. Identify symmetry, grid patterns, and regional styles.
        </p>
    </div>
    """, unsafe_allow_html=True)

def kolam_mastery_card():
    st.page_link(page="Kolam_Mastery.py", label="Kolam Mastery", icon=":material/edit:")
    st.markdown('<h2 class="section-header">🖌️ Kolam Mastery</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="interactive-card" style='
        background: linear-gradient(135deg, #E6F3FF, #FFE4E1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease-in-out;
        cursor: pointer;
    '>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Learn to recreate Kolams with guided drawing tools. Practice rangoli-style tracing or master single-stroke techniques.
        </p>
    </div>
    """, unsafe_allow_html=True)

def kolam_creator_card():
    st.page_link(page="Kolam_Creator.py", label="Kolam Creator", icon=":material/draw_collage:")
    st.markdown('<h2 class="section-header">🎨 Kolam Creator</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="interactive-card" style='
        background: linear-gradient(135deg, #FFEAA7, #E6E6FA);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease-in-out;
        cursor: pointer;
    '>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Design your own Kolams with AI-generated patterns or a digital canvas. Explore symmetry and cultural motifs.
        </p>
    </div>
    """, unsafe_allow_html=True)

def one_on_one_card():
    st.page_link(page="Special_One_on_One.py", label="Special One-on-One", icon=":material/person_raised_hand:")
    st.markdown('<h2 class="section-header">👩‍🏫 Special One-on-One</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="interactive-card" style='
        background: linear-gradient(135deg, #E8F5E8, #FFE4E1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease-in-out;
        cursor: pointer;
    '>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Connect with expert Kolam mentors for personalized lessons to master traditional designs and techniques.
        </p>
    </div>
    """, unsafe_allow_html=True)

def community_card():
    st.page_link(page="Community.py", label="Kolam Community", icon=":material/diversity_3:")
    st.markdown('<h2 class="section-header">🌐 Kolam Community</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="interactive-card" style='
        background: linear-gradient(135deg, #E6E6FA, #E8F5E8);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease-in-out;
        cursor: pointer;
    '>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Join a vibrant community to share Kolam designs, participate in events, and celebrate cultural heritage.
        </p>
    </div>
    """, unsafe_allow_html=True)