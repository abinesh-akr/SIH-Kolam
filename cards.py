import streamlit as st
from PIL import Image

def blog_card():
    st.markdown("""
    <div class="card">
        <h2 style='color: #1E3A8A; font-family: Lato, sans-serif;'>📜 Kolam: Heritage & Culture</h2>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Explore the rich history, cultural significance, and mathematical beauty of Kolam art. Learn about regional variations and their stories.
        </p>
        <a href="?page=Blog" style='color: #3B82F6; text-decoration: none; font-weight: 500; font-family: Lato, sans-serif;'>Discover Now :material/auto_stories:</a>
    </div>
    """, unsafe_allow_html=True)

def analysis_card():
    st.markdown("""
    <div class="card">
        <h2 style='color: #1E3A8A; font-family: Lato, sans-serif;'>🔍 Kolam Insights</h2>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Uncover the design principles of Kolams with AI-driven analysis and classification. Identify symmetry, grid patterns, and regional styles.
        </p>
        <a href="?page=Kolam_Insights" style='color: #3B82F6; text-decoration: none; font-weight: 500; font-family: Lato, sans-serif;'>Explore Insights :material/analytics:</a>
    </div>
    """, unsafe_allow_html=True)

def kolam_mastery_card():
    st.markdown("""
    <div class="card">
        <h2 style='color: #1E3A8A; font-family: Lato, sans-serif;'>🖌️ Kolam Mastery</h2>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Learn to recreate Kolams with guided drawing tools. Practice rangoli-style tracing or master single-stroke techniques.
        </p>
        <a href="?page=Kolam_Mastery" style='color: #3B82F6; text-decoration: none; font-weight: 500; font-family: Lato, sans-serif;'>Start Learning :material/edit:</a>
    </div>
    """, unsafe_allow_html=True)

def kolam_creator_card():
    st.markdown("""
    <div class="card">
        <h2 style='color: #1E3A8A; font-family: Lato, sans-serif;'>🎨 Kolam Creator</h2>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Design your own Kolams with AI-generated patterns or a digital canvas. Explore symmetry and cultural motifs.
        </p>
        <a href="?page=Kolam_Creator" style='color: #3B82F6; text-decoration: none; font-weight: 500; font-family: Lato, sans-serif;'>Create Now :material/draw_collage:</a>
    </div>
    """, unsafe_allow_html=True)

def one_on_one_card():
    st.markdown("""
    <div class="card">
        <h2 style='color: #1E3A8A; font-family: Lato, sans-serif;'>👩‍🏫 Special One-on-One</h2>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Connect with expert Kolam mentors for personalized lessons to master traditional designs and techniques.
        </p>
        <a href="?page=Special_One_on_One" style='color: #3B82F6; text-decoration: none; font-weight: 500; font-family: Lato, sans-serif;'>Book a Session :material/person_raised_hand:</a>
    </div>
    """, unsafe_allow_html=True)

def community_card():
    st.markdown("""
    <div class="card">
        <h2 style='color: #1E3A8A; font-family: Lato, sans-serif;'>🌐 Kolam Community</h2>
        <p style='font-family: Lato, sans-serif; color: #2C3E50;'>
            Join a vibrant community to share Kolam designs, participate in events, and celebrate cultural heritage.
        </p>
        <a href="?page=Community" style='color: #3B82F6; text-decoration: none; font-weight: 500; font-family: Lato, sans-serif;'>Join Now :material/diversity_3:</a>
    </div>
    """, unsafe_allow_html=True)
