import streamlit as st
from cards import blog_card, analysis_card, kolam_creator_card, kolam_mastery_card, one_on_one_card, community_card

st.set_page_config(page_title="AnantaKolam", layout="wide", initial_sidebar_state="expanded")

pages = [
    st.Page("Home.py", title="Home", icon=":material/home:"),
    st.Page("Blog.py", title="Kolam: Heritage & Culture", icon=":material/auto_stories:"),
    st.Page("Kolam_Insights.py", title="Kolam Insights", icon=":material/analytics:"),
    st.Page("Kolam_Mastery.py", title="Kolam Mastery", icon=":material/edit:"),
    st.Page("Kolam_Creator.py", title="Kolam Creator", icon=":material/draw_collage:"),
    st.Page("Special_One_on_One.py", title="Special One-on-One", icon=":material/person_raised_hand:"),
    st.Page("Community.py", title="Kolam Community", icon=":material/diversity_3:")
]

page = st.navigation(pages)
page.run()

with st.sidebar.container(height=380):
    if page.title == "Kolam: Heritage & Culture":
        blog_card()
    elif page.title == "Kolam Insights":
        analysis_card()
    elif page.title == "Kolam Mastery":
        kolam_mastery_card()
    elif page.title == "Kolam Creator":
        kolam_creator_card()
    elif page.title == "Special One-on-One":
        one_on_one_card()
    elif page.title == "Kolam Community":
        community_card()
    else:
        st.page_link("Home.py", label="Home", icon=":material/home:")
        st.write("Welcome to AnantaKolam")
        st.markdown("""
        <div style='text-align: center;'>
            <img src="https://ik.imagekit.io/o0nppkxow/Kolam_design_5_long%20(1).png?updatedAt=1757718152888" alt="AnantaKolam Banner" width="200" />
            <h3 style='color: gray;'>Infinite patterns, infinite stories.</h3>
            <br />
            <p style='color: gray;'>Built using Python - Streamlit, Pollination AI Image Generation, and Sutra-multilingual model</p>
        </div>
        """, unsafe_allow_html=True)

st.caption("Built with passion by Team Symmetrix :)")