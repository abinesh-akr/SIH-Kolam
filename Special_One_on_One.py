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

# Custom CSS with enhanced styling
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
    .kolam-pattern-mentor {
        width: 80px;
        height: 80px;
        position: relative;
        margin: 20px auto;
        animation: rotate 10s linear infinite;
    }
    
    .kolam-pattern-mentor::before {
        content: '';
        position: absolute;
        width: 6px;
        height: 6px;
        background: #FF69B4;
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
        animation: pulse 2s ease-in-out infinite;
    }
    
    .kolam-pattern-booking {
        width: 60px;
        height: 60px;
        position: relative;
        margin: 15px auto;
        animation: float 4s ease-in-out infinite;
    }
    
    .kolam-pattern-booking::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid #FF69B4;
        border-radius: 50%;
        animation: ripple 3s ease-out infinite;
    }
    
    .kolam-pattern-booking::after {
        content: '';
        position: absolute;
        width: 70%;
        height: 70%;
        top: 15%;
        left: 15%;
        border: 2px solid #9370DB;
        border-radius: 50%;
        animation: ripple 3s ease-out infinite 1s;
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0.8);
            opacity: 1;
        }
        100% {
            transform: scale(1.4);
            opacity: 0;
        }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.7; transform: translate(-50%, -50%) scale(1); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #FFE4E1 0%, #FFEAA7 50%, #E6E6FA 100%);
        padding: 60px 40px;
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
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
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
        font-size: 1.8rem;
        color: #5D6D7E;
        font-weight: 700;
        position: relative;
        z-index: 2;
        animation: subtitleFloat 4s ease-in-out infinite;
    }
    
    @keyframes subtitleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        padding: 10px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 30px;
        background: transparent;
        border-radius: 15px;
        color: #2C3E50;
        font-weight: 600;
        font-size: 1.1rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF69B4, #9370DB);
        color: white;
        box-shadow: 0 5px 15px rgba(255,105,180,0.4);
    }
    
    /* Form styling */
    .form-container {
        background: rgba(255,255,255,0.95);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 20px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .form-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .form-title::after {
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
    
    /* Mentor card styling */
    .mentor-card {
        background: rgba(255,255,255,0.9);
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 2px solid transparent;
        cursor: pointer;
    }
    
    .mentor-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        border-color: #FF69B4;
    }
    
    .mentor-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 10px;
    }
    
    .mentor-rating {
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    
    .mentor-experience {
        color: #5D6D7E;
        font-weight: 500;
        margin-bottom: 15px;
    }
    
    .mentor-price {
        font-size: 1.3rem;
        font-weight: 700;
        color: #FF69B4;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF69B4, #9370DB);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(255,105,180,0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,105,180,0.6);
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(135deg, #E8F5E8, #FFFFFF);
        border: 2px solid #32CD32;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
        color: #2C3E50;
        font-weight: 600;
    }
    
    /* Floating decorations */
    .floating-decoration {
        position: fixed;
        pointer-events: none;
        z-index: 1;
        opacity: 0.6;
    }
    
    .floating-decoration.dot-1 {
        top: 15%;
        left: 5%;
        animation: floatUpDown 6s ease-in-out infinite;
    }
    
    .floating-decoration.dot-2 {
        top: 30%;
        right: 8%;
        animation: floatUpDown 4s ease-in-out infinite reverse;
    }
    
    .floating-decoration.dot-3 {
        bottom: 20%;
        left: 10%;
        animation: floatUpDown 5s ease-in-out infinite;
    }
    
    @keyframes floatUpDown {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem; }
        .hero-subtitle { font-size: 1.4rem; }
        .form-container { padding: 25px; }
        .mentor-card { padding: 20px; }
    }
</style>
""", unsafe_allow_html=True)

# Add floating decorations
st.markdown("""
<div class="floating-decoration dot-1">
    <div class="kolam-pattern-mentor"></div>
</div>
<div class="floating-decoration dot-2">
    <div class="kolam-pattern-booking"></div>
</div>
<div class="floating-decoration dot-3">
    <div class="kolam-pattern-mentor"></div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'mentors' not in st.session_state:
    st.session_state.mentors = [
        {
            'name': 'Priya Krishnamurthy',
            'experience': '15 years teaching traditional Kolam',
            'rating': '⭐⭐⭐⭐⭐ 4.9',
            'speciality': 'Traditional Pulli & Sikku Kolam',
            'price': '₹800/hour',
            'available_times': ['9:00 AM', '11:00 AM', '2:00 PM', '4:00 PM', '6:00 PM'],
            'description': 'Master artist specializing in traditional Tamil Kolam designs with geometric precision.'
        },
        {
            'name': 'Lakshmi Venkatesh',
            'experience': '12 years in contemporary Kolam art',
            'rating': '⭐⭐⭐⭐⭐ 4.8',
            'speciality': 'Modern & Festival Kolam',
            'price': '₹700/hour',
            'available_times': ['10:00 AM', '1:00 PM', '3:00 PM', '5:00 PM', '7:00 PM'],
            'description': 'Expert in colorful festival Kolams and modern artistic interpretations.'
        },
        {
            'name': 'Meera Rajagopalan',
            'experience': '20+ years in Kolam mathematics',
            'rating': '⭐⭐⭐⭐⭐ 5.0',
            'speciality': 'Mathematical Kolam & Fractals',
            'price': '₹1000/hour',
            'available_times': ['8:00 AM', '12:00 PM', '3:00 PM', '6:00 PM'],
            'description': 'Renowned expert connecting ancient Kolam patterns with modern mathematical concepts.'
        }
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

if 'mentor_applications' not in st.session_state:
    st.session_state.mentor_applications = []

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="kolam-pattern-mentor"></div>
    <h1 class="hero-title">🎨 Kolam Mentors</h1>
    <p class="hero-subtitle">Learn from Masters • Teach Others • Preserve Tradition</p>
    <div class="kolam-pattern-booking"></div>
</div>
""", unsafe_allow_html=True)

# Main tabs
tab1, tab2 = st.tabs(["🔍 Find a Mentor", "🎓 Become a Mentor"])

with tab1:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="form-title">Book a Kolam Learning Session</h2>', unsafe_allow_html=True)
    
    # Display available mentors
    st.markdown("### 👩‍🎨 Available Mentors")
    
    for i, mentor in enumerate(st.session_state.mentors):
        with st.expander(f"{mentor['name']} - {mentor['speciality']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="mentor-card">
                    <div class="mentor-name">{mentor['name']}</div>
                    <div class="mentor-rating">{mentor['rating']}</div>
                    <div class="mentor-experience">📚 {mentor['experience']}</div>
                    <div class="mentor-experience">🎯 Speciality: {mentor['speciality']}</div>
                    <div class="mentor-experience">📝 {mentor['description']}</div>
                    <div class="mentor-price">💰 {mentor['price']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="kolam-pattern-booking"></div>', unsafe_allow_html=True)
            
            # Booking form for this mentor
            st.markdown("#### 📅 Book a Session")
            
            booking_col1, booking_col2 = st.columns(2)
            
            with booking_col1:
                selected_date = st.date_input(
                    "Select Date",
                    min_value=datetime.date.today(),
                    max_value=datetime.date.today() + timedelta(days=30),
                    key=f"date_{i}"
                )
                
                session_type = st.selectbox(
                    "Session Type",
                    ["Video Call", "In-Person (Bangalore only)", "Phone Call"],
                    key=f"type_{i}"
                )
            
            with booking_col2:
                selected_time = st.selectbox(
                    "Available Times",
                    mentor['available_times'],
                    key=f"time_{i}"
                )
                
                duration = st.selectbox(
                    "Session Duration",
                    ["1 hour", "1.5 hours", "2 hours"],
                    key=f"duration_{i}"
                )
            
            # Student details
            student_name = st.text_input("Your Name", key=f"student_name_{i}")
            student_email = st.text_input("Email Address", key=f"student_email_{i}")
            student_phone = st.text_input("Phone Number", key=f"student_phone_{i}")
            
            # Experience level
            experience_level = st.selectbox(
                "Your Experience Level",
                ["Complete Beginner", "Some Experience", "Intermediate", "Advanced"],
                key=f"experience_{i}"
            )
            
            # Special requests
            special_requests = st.text_area(
                "Special Requests or Learning Goals",
                placeholder="Any specific Kolam patterns you'd like to learn?",
                key=f"requests_{i}"
            )
            
            if st.button(f"Book Session with {mentor['name']}", key=f"book_{i}"):
                if student_name and student_email and student_phone:
                    # Calculate price based on duration
                    base_price = int(mentor['price'].split('₹')[1].split('/')[0])
                    duration_multiplier = {"1 hour": 1, "1.5 hours": 1.5, "2 hours": 2}
                    total_price = int(base_price * duration_multiplier[duration])
                    
                    booking = {
                        'mentor_name': mentor['name'],
                        'student_name': student_name,
                        'student_email': student_email,
                        'student_phone': student_phone,
                        'date': selected_date.strftime('%Y-%m-%d'),
                        'time': selected_time,
                        'duration': duration,
                        'session_type': session_type,
                        'experience_level': experience_level,
                        'special_requests': special_requests,
                        'total_price': total_price,
                        'booking_id': f"KM{len(st.session_state.bookings) + 1:04d}",
                        'status': 'Pending Confirmation'
                    }
                    
                    st.session_state.bookings.append(booking)
                    
                    st.markdown(f"""
                    <div class="success-message">
                        🎉 <strong>Booking Successful!</strong><br>
                        Booking ID: {booking['booking_id']}<br>
                        Total Cost: ₹{total_price}<br>
                        You will receive a confirmation email shortly with payment details.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                else:
                    st.error("Please fill in all required fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="form-title">Apply to Become a Kolam Mentor</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🌟 Share Your Kolam Expertise with Others!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Why become a Kolam mentor?**
        - 💰 Earn ₹500-₹1200 per hour
        - 🌍 Teach students globally via video calls
        - 🎨 Share your passion for this beautiful art form
        - 📚 Preserve traditional knowledge for future generations
        - ⏰ Flexible schedule - choose your own hours
        """)
    
    with col2:
        st.markdown('<div class="kolam-pattern-mentor"></div>', unsafe_allow_html=True)
    
    # Mentor application form
    st.markdown("#### 📝 Application Form")
    
    mentor_col1, mentor_col2 = st.columns(2)
    
    with mentor_col1:
        full_name = st.text_input("Full Name *")
        email = st.text_input("Email Address *")
        phone = st.text_input("Phone Number *")
        age = st.number_input("Age", min_value=18, max_value=80, value=25)
        location = st.text_input("City/Location *")
    
    with mentor_col2:
        years_experience = st.number_input("Years of Kolam Experience *", min_value=1, max_value=50, value=5)
        education = st.selectbox(
            "Educational Background",
            ["High School", "Bachelor's Degree", "Master's Degree", "PhD", "Art School", "Traditional Learning"]
        )
        languages = st.multiselect(
            "Languages You Can Teach In",
            ["Tamil", "English", "Hindi", "Telugu", "Kannada", "Malayalam", "Sanskrit"]
        )
        
        availability = st.multiselect(
            "Preferred Teaching Hours",
            ["Morning (6 AM - 12 PM)", "Afternoon (12 PM - 6 PM)", "Evening (6 PM - 10 PM)"]
        )
    
    # Specializations
    specializations = st.multiselect(
        "Your Kolam Specializations *",
        [
            "Traditional Pulli Kolam",
            "Sikku Kolam (Knot patterns)",
            "Kavi Kolam (Temple style)",
            "Freehand Kolam",
            "Festival Kolam",
            "Mathematical Kolam",
            "3D Kolam",
            "Contemporary/Modern Kolam",
            "Children's Kolam",
            "Beginner-friendly patterns"
        ]
    )
    
    # Experience details
    experience_description = st.text_area(
        "Describe Your Kolam Journey *",
        placeholder="Tell us about how you learned Kolam, your teaching experience, notable achievements, etc.",
        height=100
    )
    
    # Teaching preference
    teaching_modes = st.multiselect(
        "Preferred Teaching Methods",
        ["Video Calls", "In-Person (Local only)", "Phone Calls", "Pre-recorded Courses"]
    )
    
    # Hourly rate
    hourly_rate = st.slider(
        "Expected Hourly Rate (₹)",
        min_value=500,
        max_value=1500,
        value=800,
        step=50
    )
    
    # Portfolio
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
    
    # Additional information
    additional_info = st.text_area(
        "Additional Information",
        placeholder="Anything else you'd like us to know about your Kolam expertise or teaching style?"
    )
    
    # Terms and conditions
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
    padding: 40px; 
    background: linear-gradient(135deg, #E8F5E8, #E6F3FF, #FFE4E1); 
    background-size: 300% 300%;
    animation: gradientShift 10s ease infinite;
    margin-top: 40px; 
    border-radius: 25px;
    position: relative;
">
    <div class="kolam-pattern-mentor"></div>
    <p style="
        font-family: 'Dancing Script', cursive; 
        color: #2C3E50; 
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
    ">
        Connecting Kolam Masters with Eager Learners
    </p>
    <div class="kolam-pattern-booking"></div>
    <p style="
        font-family: 'Lato', sans-serif; 
        color: #5D6D7E; 
        font-style: italic;
    ">
        "Preserving tradition through teaching"
    </p>
</div>
""", unsafe_allow_html=True)
