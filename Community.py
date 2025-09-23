import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import os
import time

DB_PATH = "anantakolam_community.db"
IMAGE_DIR = "uploads"

# ----------------------
# Helpers: DB and files
# ----------------------

def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            bio TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            state TEXT,
            kolam_type TEXT,
            tags TEXT,
            image_path TEXT,
            created_at REAL,
            likes INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            user_id INTEGER,
            comment TEXT,
            created_at REAL,
            FOREIGN KEY(post_id) REFERENCES posts(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            lat REAL,
            lon REAL,
            date TEXT,
            prize TEXT,
            created_at REAL
        )
    ''')
    conn.commit()
    return conn


def save_image(file, prefix="post"):
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    img = Image.open(file)
    timestamp = int(time.time() * 1000)
    fname = f"{prefix}_{timestamp}.png"
    path = os.path.join(IMAGE_DIR, fname)
    img.save(path)
    return path

# ----------------------
# Data access helpers
# ----------------------

def get_user_by_name(conn, name):
    c = conn.cursor()
    c.execute("SELECT id, name, bio FROM users WHERE name = ?", (name,))
    return c.fetchone()

def create_user(conn, name, bio=""):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, bio) VALUES (?, ?)", (name, bio))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    return get_user_by_name(conn, name)

def create_post(conn, user_id, title, description, state, kolam_type, tags, image_path):
    c = conn.cursor()
    created_at = time.time()
    c.execute(
        "INSERT INTO posts (user_id, title, description, state, kolam_type, tags, image_path, created_at) VALUES (?,?,?,?,?,?,?,?)",
        (user_id, title, description, state, kolam_type, tags, image_path, created_at),
    )
    conn.commit()

def get_posts(conn, order_desc=True):
    c = conn.cursor()
    q = """SELECT p.id, u.name, p.title, p.description, p.state, p.kolam_type,
                  p.tags, p.image_path, p.created_at, p.likes, p.user_id
           FROM posts p JOIN users u ON p.user_id = u.id"""
    if order_desc:
        q += " ORDER BY p.created_at DESC"
    c.execute(q)
    return c.fetchall()

def add_comment(conn, post_id, user_id, comment):
    c = conn.cursor()
    created_at = time.time()
    c.execute(
        "INSERT INTO comments (post_id, user_id, comment, created_at) VALUES (?,?,?,?)",
        (post_id, user_id, comment, created_at),
    )
    conn.commit()

def get_comments_for_post(conn, post_id):
    c = conn.cursor()
    c.execute(
        """SELECT c.comment, u.name, c.created_at 
           FROM comments c 
           JOIN users u ON c.user_id = u.id 
           WHERE c.post_id = ? 
           ORDER BY c.created_at""",
        (post_id,),
    )
    return c.fetchall()

def like_post(conn, post_id):
    c = conn.cursor()
    c.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()

def create_event(conn, title, description, lat, lon, date, prize):
    c = conn.cursor()
    created_at = time.time()
    c.execute(
        "INSERT INTO events (title, description, lat, lon, date, prize, created_at) VALUES (?,?,?,?,?,?,?)",
        (title, description, lat, lon, date, prize, created_at),
    )
    conn.commit()

def get_upcoming_events(conn):
    c = conn.cursor()
    c.execute("SELECT id, title, description, lat, lon, date, prize FROM events ORDER BY date")
    return c.fetchall()

# ----------------------
# Streamlit UI
# ----------------------

st.set_page_config(page_title="AnantaKolam Community", layout="wide")
conn = init_db()

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Centered Login/Profile
if st.session_state.current_user is None:
    st.markdown("<h2 style='text-align:center;'>Welcome to AnantaKolam Community</h2>", unsafe_allow_html=True)
    with st.container():
        cols = st.columns([1,2,1])
        with cols[1]:
            name = st.text_input("Enter your display name")
            bio = st.text_area("Short bio (optional)")
            if st.button("Login / Create"):
                if name.strip():
                    user = create_user(conn, name.strip(), bio.strip())
                    st.session_state.current_user = {'id': user[0], 'name': user[1], 'bio': user[2]}
                    st.success(f"Logged in as {user[1]}")
                    st.rerun()
else:
    u = st.session_state.current_user
    st.markdown(f"<h3 style='text-align:center;'>Hello, {u['name']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>{u.get('bio','')}</p>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.current_user = None
        st.rerun()

if st.session_state.current_user:
    st.header("Community — Share Kolams, find events, win prizes")
    tabs = st.tabs(["Feed","Upload","Events & Map","Artists","Leaderboard"])

    # --- Feed ---
    with tabs[0]:
        posts = get_posts(conn)
        for post in posts:
            post_id, author, title, desc, state, kolam_type, tags, img_path, created_at, likes, user_id = post
            cols = st.columns([1,3])
            with cols[0]:
                if img_path and os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
            with cols[1]:
                st.markdown(f"**{title}** — by **{author}**")
                st.write(desc)
                st.caption(f"State: {state} • Type: {kolam_type} • Tags: {tags}")
                st.write(f"❤️ {likes}")
                if st.button("Like", key=f"like_{post_id}"):
                    like_post(conn, post_id)
                    st.rerun()
                st.write("Comments:")
                comments = get_comments_for_post(conn, post_id)
                for cmt, uname, ctime in comments:
                    st.write(f"**{uname}**: {cmt}")
                comment = st.text_input("Add comment", key=f"comment_{post_id}")
                if st.button("Post", key=f"postc_{post_id}") and comment.strip():
                    add_comment(conn, post_id, st.session_state.current_user['id'], comment.strip())
                    st.rerun()

    # --- Upload ---
    with tabs[1]:
        with st.form("upload_form"):
            title = st.text_input("Title")
            desc = st.text_area("Description")
            state = st.selectbox("State", ['Tamil Nadu','Kerala','Karnataka','Andhra Pradesh','Odisha','Other'])
            kolam_type = st.selectbox("Kolam Type", ['Traditional','Festival','Geometric','Experimental'])
            tags = st.text_input("Tags (comma separated)")
            uploaded_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
            if st.form_submit_button("Upload"):
                if uploaded_file and title.strip():
                    path = save_image(uploaded_file)
                    create_post(conn, st.session_state.current_user['id'], title.strip(), desc.strip(), state, kolam_type, tags.strip(), path)
                    st.success("Uploaded!")
                    st.rerun()

    # --- Events & Map ---
    with tabs[2]:
        st.subheader("Events")
        e_title = st.text_input("Event Title")
        e_desc = st.text_area("Description")
        e_date = st.date_input("Date")
        e_prize = st.text_input("Prize")
        e_lat = st.text_input("Latitude")
        e_lon = st.text_input("Longitude")
        if st.button("Create Event"):
            try:
                create_event(conn, e_title, e_desc, float(e_lat), float(e_lon), e_date.isoformat(), e_prize)
                st.success("Event Created")
                st.rerun()
            except:
                st.error("Invalid lat/lon")

        events = get_upcoming_events(conn)
        if events:
            st.dataframe(pd.DataFrame(events, columns=['ID','Title','Description','Lat','Lon','Date','Prize']))

    # --- Artists ---
    with tabs[3]:
        c = conn.cursor()
        c.execute("SELECT id, name, bio FROM users")
        artists = c.fetchall()
        for aid, aname, abio in artists:
            with st.expander(aname):
                st.write(abio)

    # --- Leaderboard ---
    with tabs[4]:
        c = conn.cursor()
        c.execute("SELECT u.name, p.title, p.likes FROM posts p JOIN users u ON p.user_id=u.id ORDER BY p.likes DESC LIMIT 10")
        top = c.fetchall()
        if top:
            st.table(pd.DataFrame(top, columns=['Artist','Title','Likes']))
        else:
            st.write("No posts yet")

st.caption("AnantaKolam Community demo — add authentication and cloud storage for production")
