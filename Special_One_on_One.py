import streamlit as st
import datetime
import time
from datetime import timedelta

# Page configuration
st.set_page_config(
    page_title="Kolam Mentors - Learn & Teach",
    page_icon="🎨",
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
    font-size: 4rem;
    color: #1E3A8A;
    margin-bottom: 1rem;
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

/* Form container */
.form-container {
    background: #F8FAFC;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}

.form-container:hover {
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    background: linear-gradient(135deg, #F8FAFC, #DBEAFE);
}

.form-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(147, 197, 253, 0.3), transparent);
    transition: 0.5s;
}

.form-container:hover::before {
    left: 100%;
}

/* Form title */
.form-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #1E3A8A;
    text-align: center;
    margin-bottom: 1rem;
}

/* Success message */
.success-message {
    background: rgba(59, 130, 246, 0.1);
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #3B82F6;
    margin: 1rem 0;
    color: #2C3E50;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    color: #EFF6FF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #3B82F6, #93C5FD);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
    transform: translateY(-2px);
}

/* Tabs styling */
.stTabs [data-baseweb="tab"] {
    background: darkblue;
    color : white;
    border-radius: 8px;
    margin: 0.5rem;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: #DBEAFE;
    transform: translateY(-2px);
}

.stTabs [data-baseweb="tab-highlight"] {
    background: #3B82F6;
}

/* Responsive design for tablets */
@media (max-width: 768px) {
    .hero-title { font-size: 3rem; }
    .hero-subtitle { font-size: 1.2rem; }
    .form-title { font-size: 2rem; }
    .main-content { padding: 1rem; }
    .form-container { padding: 1.5rem; }
    .stTabs [data-baseweb="tab"] { padding: 0.4rem 0.8rem; font-size: 0.9rem; }
    .success-message { font-size: 0.9rem; padding: 0.8rem; }
}

/* Responsive design for mobile phones */
@media (max-width: 576px) {
    .main-content { padding: 0.8rem; margin-top: 120px; }
    .hero-section { padding: 1.5rem; }
    .hero-title { font-size: 2.2rem; }
    .hero-subtitle { font-size: 1rem; }
    .form-container { padding: 1rem; margin: 0.5rem 0; }
    .form-title { font-size: 1.6rem; }
    .success-message { font-size: 0.85rem; padding: 0.6rem; }
    .stButton > button { padding: 0.4rem 0.8rem; font-size: 0.85rem; }
    .stTabs [data-baseweb="tab"] { padding: 0.3rem 0.6rem; font-size: 0.8rem; margin: 0.3rem; }
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
    <h1 class="hero-title">Kolam Mentors - Learn & Teach</h1>
    <p class="hero-subtitle">Personalized Lessons with Expert Mentors</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'bookings' not in st.session_state:
    st.session_state.bookings = []
if 'mentor_applications' not in st.session_state:
    st.session_state.mentor_applications = []
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Find Mentor"

# Tabs
tab1, tab2 = st.tabs(["Find a Mentor", "Become a Mentor"])

with tab1:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="form-title">Book Your One-on-One Session</h2>', unsafe_allow_html=True)

    student_name = st.text_input("Your Name *")
    student_email = st.text_input("Your Email *")
    student_phone = st.text_input("Your Phone Number *")
    student_level = st.selectbox("Your Kolam Experience Level", ["Beginner", "Intermediate", "Advanced"])
    student_goals = st.text_area("What do you want to learn? *", placeholder="e.g., Basic patterns, Advanced symmetry, Festival designs...")
    mentor = st.selectbox("Select Mentor", ["Priya Ramanathan (Tamil Nadu)", "Lakshmi Nair (Kerala)", "Radha Krishna (Karnataka)", "Sita Devi (Andhra Pradesh)"])
    session_duration = st.selectbox("Session Duration", ["30 minutes (₹500)", "60 minutes (₹900)", "90 minutes (₹1200)"])
    preferred_date = st.date_input("Preferred Date", min_value=datetime.date.today() + timedelta(days=1))
    preferred_time = st.time_input("Preferred Time")

    if st.button("Book Session", type="primary"):
        if (student_name and student_email and student_phone and student_goals and preferred_date and preferred_time):
            price_map = {
                "30 minutes (₹500)": 500,
                "60 minutes (₹900)": 900,
                "90 minutes (₹1200)": 1200
            }
            total_price = price_map.get(session_duration, 0)
            
            booking = {
                'student_name': student_name,
                'student_email': student_email,
                'student_phone': student_phone,
                'student_level': student_level,
                'student_goals': student_goals,
                'mentor_name': mentor,
                'session_duration': session_duration,
                'date': preferred_date.strftime('%Y-%m-%d'),
                'time': preferred_time.strftime('%H:%M'),
                'total_price': total_price,
                'booking_id': f"BK{len(st.session_state.bookings) + 1:04d}",
                'status': 'Confirmed'
            }
            
            st.session_state.bookings.append(booking)
            
            st.markdown(f"""
            <div class="success-message">
                🎉 <strong>Booking Confirmed!</strong><br>
                Booking ID: {booking['booking_id']}<br>
                A confirmation email has been sent to {student_email}.
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("Please fill in all required fields marked with *")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="form-title">Become a Kolam Mentor</h2>', unsafe_allow_html=True)

    full_name = st.text_input("Full Name *")
    email = st.text_input("Email Address *")
    phone = st.text_input("Phone Number *")
    age = st.number_input("Age", min_value=18, max_value=100)
    location = st.text_input("Location (City, State) *")
    years_experience = st.number_input("Years of Kolam Experience *", min_value=1, max_value=50)
    education = st.text_input("Education/Background")
    languages = st.multiselect(
        "Languages Spoken",
        ["English", "Tamil", "Telugu", "Kannada", "Malayalam", "Hindi", "Other"]
    )
    availability = st.multiselect(
        "Available Days",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    specializations = st.multiselect(
        "Specializations",
        [
            "Traditional Kolam",
            "Festival Kolam",
            "Mathematical Kolam",
            "3D Kolam",
            "Contemporary/Modern Kolam",
            "Children's Kolam",
            "Beginner-friendly patterns"
        ]
    )
    
    experience_description = st.text_area(
        "Describe Your Kolam Journey *",
        placeholder="Tell us about how you learned Kolam, your teaching experience, notable achievements, etc.",
        height=100
    )
    
    teaching_modes = st.multiselect(
        "Preferred Teaching Methods",
        ["Video Calls", "In-Person (Local only)", "Phone Calls", "Pre-recorded Courses"]
    )
    
    hourly_rate = st.slider(
        "Expected Hourly Rate (₹)",
        min_value=500,
        max_value=1500,
        value=800,
        step=50
    )
    
    st.markdown("#### 🖼️ Portfolio")
    portfolio_images = st.file_uploader(
        "Upload Your Kolam Photos (Optional)",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg']
    )
    
    portfolio_links = st.text_area(
        "Social Media or Website Links (Optional)",
        placeholder="Instagram, Facebook, YouTube channel, personal website, etc."
    )
    
    additional_info = st.text_area(
        "Additional Information",
        placeholder="Anything else you'd like us to know about your Kolam expertise or teaching style?"
    )
    
    agree_terms = st.checkbox("I agree to the terms and conditions and mentor guidelines *")
    
    if st.button("Submit Application", type="primary"):
        if (full_name and email and phone and location and years_experience and 
            specializations and experience_description and agree_terms):
            
            application = {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'age': age,
                'location': location,
                'years_experience': years_experience,
                'education': education,
                'languages': languages,
                'availability': availability,
                'specializations': specializations,
                'experience_description': experience_description,
                'teaching_modes': teaching_modes,
                'hourly_rate': hourly_rate,
                'portfolio_links': portfolio_links,
                'additional_info': additional_info,
                'application_id': f"MA{len(st.session_state.mentor_applications) + 1:04d}",
                'application_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'Under Review'
            }
            
            st.session_state.mentor_applications.append(application)
            
            st.markdown(f"""
            <div class="success-message">
                🎉 <strong>Application Submitted Successfully!</strong><br>
                Application ID: {application['application_id']}<br>
                We will review your application within 2-3 business days and get back to you via email.
                <br><br>
                <strong>Next Steps:</strong><br>
                1. Application review (2-3 days)<br>
                2. Video interview (if selected)<br>
                3. Sample teaching session<br>
                4. Profile creation and onboarding
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
        else:
            st.error("Please fill in all required fields marked with *")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Admin section (hidden, for demo purposes)
if st.checkbox("🔧 Admin Panel (Demo)", value=False):
    st.markdown("### 📊 Admin Dashboard")
    
    admin_tab1, admin_tab2 = st.tabs(["Bookings", "Mentor Applications"])
    
    with admin_tab1:
        st.markdown("#### Recent Bookings")
        if st.session_state.bookings:
            for booking in st.session_state.bookings:
                st.markdown(f"""
                **Booking ID:** {booking['booking_id']}  
                **Student:** {booking['student_name']}  
                **Mentor:** {booking['mentor_name']}  
                **Date:** {booking['date']} at {booking['time']}  
                **Total:** ₹{booking['total_price']}  
                **Status:** {booking['status']}
                ---
                """)
        else:
            st.info("No bookings yet.")
    
    with admin_tab2:
        st.markdown("#### Mentor Applications")
        if st.session_state.mentor_applications:
            for app in st.session_state.mentor_applications:
                st.markdown(f"""
                **Application ID:** {app['application_id']}  
                **Name:** {app['full_name']}  
                **Experience:** {app['years_experience']} years  
                **Specializations:** {', '.join(app['specializations'])}  
                **Rate:** ₹{app['hourly_rate']}/hour  
                **Status:** {app['status']}
                ---
                """)
        else:
            st.info("No applications yet.")

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
        Connecting Kolam Masters with Eager Learners
    </p>
    <div class="floating-dot dot-2"></div>
    <p style="
        font-style: italic;
    ">
        "Preserving tradition through teaching"
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
