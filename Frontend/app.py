import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import sqlite3
from datetime import datetime, timedelta
import sys
import os

# Dynamic path resolution to import Backend/survey.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend')))
import survey  # Import our math scoring engine

# Set page configuration with a premium look
st.set_page_config(
    page_title="Sarawak Tech-Trust Barometer (STTB)",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Flag_of_Sarawak.svg/200px-Flag_of_Sarawak.svg.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 1. PREMIUM GLASSMORPHISM THEME & STYLING (DYNAMIC DARK/LIGHT)
# ---------------------------------------------------------
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Dark Mode"

gold_color = "#D4AF37" if st.session_state.get("theme_mode") == "Light Mode" else "#FCD116"

if st.session_state["theme_mode"] == "Dark Mode":
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,600;1,400&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        .stApp {
            background: #1A1D20;
            color: #F4F6F8;
        }
        
        [data-testid="stSidebar"] {
            background: #000000 !important;
            border-right: 1px solid rgba(252, 209, 22, 0.15) !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #F4F6F8 !important;
        }
        
        /* Ensure selectbox text has perfect dark contrast on its white background */
        div[data-baseweb="select"] * {
            color: #1A1D20 !important;
        }
        
        /* Make standard input widget labels fully readable in Dark Mode */
        label p {
            color: #F4F6F8 !important;
            font-weight: 600 !important;
        }
        
        div[data-testid="stSidebarUserContent"] .stRadio label {
            color: #F4F6F8 !important;
        }
        
        .glass-card {
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(252, 209, 22, 0.15);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease-in-out;
            color: #F4F6F8 !important;
        }
        
        .glass-card:hover {
            border: 1px solid rgba(252, 209, 22, 0.35);
            box-shadow: 0 12px 40px 0 rgba(252, 209, 22, 0.08);
            transform: translateY(-2px);
        }
        
        .glass-header {
            background: linear-gradient(90deg, rgba(252, 209, 22, 0.12) 0%, rgba(206, 17, 38, 0.04) 60%, rgba(0, 0, 0, 0) 100%);
            border-left: 5px solid #FCD116;
            border-radius: 4px 16px 16px 4px;
            padding: 20px;
            margin-bottom: 25px;
        }
        
        h1 {
            font-family: 'Outfit', sans-serif;
            font-weight: 800 !important;
            letter-spacing: -1px;
            color: #FCD116 !important;
            text-shadow: 0px 4px 12px rgba(252, 209, 22, 0.25);
        }
        
        h2, h3 {
            font-family: 'Outfit', sans-serif;
            font-weight: 600 !important;
            color: #F4F6F8 !important;
        }
        
        .subtitle {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: 1.2rem;
            color: #bdc3c7;
            margin-top: -15px;
            margin-bottom: 25px;
        }
        
        .metric-value {
            font-size: 2.8rem;
            font-weight: 800;
            margin: 5px 0;
            background: linear-gradient(45deg, #FCD116, #CE1126);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-label {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #a0aec0;
        }
        
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #CE1126 0%, #A50F1E 100%) !important;
            color: #ffffff !important;
            border: 1px solid #FCD116 !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            box-shadow: 0 4px 15px rgba(206, 17, 38, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #FCD116 0%, #D8B213 100%) !important;
            color: #1A1D20 !important;
            border: 1px solid #CE1126 !important;
            box-shadow: 0 4px 15px rgba(252, 209, 22, 0.4) !important;
            transform: translateY(-1px) !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,600;1,400&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f4f5f8 0%, #ffffff 100%);
            color: #1a1a24;
        }
        
        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #1a1a24 !important;
        }
        
        /* Ensure selectbox text has perfect dark contrast */
        div[data-baseweb="select"] * {
            color: #1a1a24 !important;
        }
        
        /* Ensure standard input widget labels are dark in Light Mode */
        label p {
            color: #1a1a24 !important;
            font-weight: 600 !important;
        }
        
        div[data-testid="stSidebarUserContent"] .stRadio label {
            color: #1a1a24 !important;
        }
        
        .glass-card {
            background: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            transition: all 0.3s ease-in-out;
            color: #1a1a24 !important;
        }
        
        .glass-card:hover {
            border: 1px solid rgba(218, 41, 28, 0.3);
            box-shadow: 0 8px 30px rgba(218, 41, 28, 0.06);
            transform: translateY(-2px);
        }
        
        .glass-header {
            background: linear-gradient(90deg, rgba(255, 199, 44, 0.18) 0%, rgba(218, 41, 28, 0.05) 60%, rgba(0, 0, 0, 0) 100%);
            border-left: 5px solid #E0AE1B;
            border-radius: 4px 16px 16px 4px;
            padding: 20px;
            margin-bottom: 25px;
        }
        
        h1 {
            font-family: 'Outfit', sans-serif;
            font-weight: 800 !important;
            letter-spacing: -1px;
            color: #DA291C !important;
            text-shadow: none;
        }
        
        h2, h3 {
            font-family: 'Outfit', sans-serif;
            font-weight: 600 !important;
            color: #1a1a24 !important;
        }
        
        .subtitle {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: 1.2rem;
            color: #4a5568;
            margin-top: -15px;
            margin-bottom: 25px;
        }
        
        .metric-value {
            font-size: 2.8rem;
            font-weight: 800;
            margin: 5px 0;
            background: linear-gradient(45deg, #DA291C, #E0AE1B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-label {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #718096;
        }
        
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #DA291C 0%, #B81D13 100%) !important;
            color: #ffffff !important;
            border: 1px solid #E0AE1B !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            box-shadow: 0 4px 15px rgba(218, 41, 28, 0.15) !important;
            transition: all 0.3s ease !important;
        }
        
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #E0AE1B 0%, #CFA015 100%) !important;
            color: #ffffff !important;
            border: 1px solid #DA291C !important;
            box-shadow: 0 4px 15px rgba(255, 199, 44, 0.2) !important;
            transform: translateY(-1px) !important;
        }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. PDPA-COMPLIANT DATABASE ARCHITECTURE (SQLite)
# ---------------------------------------------------------
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend', 'sttb.db'))

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Respondents Profile Table (Anonymous)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS respondents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age_group TEXT NOT NULL,
        gender TEXT NOT NULL,
        occupation TEXT NOT NULL,
        district TEXT NOT NULL,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 2. Survey Responses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS survey_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        respondent_id INTEGER UNIQUE,
        responses_json TEXT NOT NULL,
        FOREIGN KEY (respondent_id) REFERENCES respondents (id)
    )
    """)
    
    # 3. Computed Index Scores Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS computed_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        respondent_id INTEGER UNIQUE,
        ps1_transparency REAL,
        ps2_ethics REAL,
        ps3_privacy REAL,
        ps4_security REAL,
        ps5_inclusion REAL,
        sttb_index REAL,
        trust_level TEXT,
        FOREIGN KEY (respondent_id) REFERENCES respondents (id)
    )
    """)
    
    # 4. Feedback & Complaints Table (Anonymized Audit Repository)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_role TEXT NOT NULL,
        category TEXT NOT NULL,
        subject TEXT NOT NULL,
        description TEXT NOT NULL,
        satisfaction INTEGER,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 5. Administrative Audit Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL,
        details TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()


def log_admin_action(action_type, details):
    """Inserts a new record into the admin audit logs table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO admin_audit_logs (action_type, details)
            VALUES (?, ?)
        """, (action_type, details))
        conn.commit()
    except Exception as e:
        pass
    finally:
        conn.close()


def seed_database_if_empty():
    """Pre-seeds the database with 50 diverse respondents for realistic visualizations."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if system_config table exists and indicates that seeding was explicitly disabled/purged
    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='system_config'")
    if cursor.fetchone()[0] > 0:
        cursor.execute("SELECT val FROM system_config WHERE key='seeded'")
        row = cursor.fetchone()
        if row and row[0] == 'false':
            conn.close()
            return  # Do not auto-seed, the user wants a clean state!
            
    cursor.execute("SELECT COUNT(*) FROM respondents")
    count = cursor.fetchone()[0]
    
    if count > 0:
        conn.close()
        return  # Database is already populated
        
    st.info("Initializing Sarawak Tech-Trust Barometer database with pilot demographic seed data...")
    
    districts = [
        "Kuching", "Samarahan", "Serian", "Sri Aman", "Betong", 
        "Sarikei", "Sibu", "Kapit", "Mukah", "Bintulu", "Miri", "Limbang"
    ]
    age_groups = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    genders = ["Male", "Female"]
    occupations = ["Student", "Civil Servant", "Private Sector", "Self-Employed", "Retired"]
    
    # Seed 65 random respondents with varying trust profiles per district
    np.random.seed(42)  # For reproducible seeding
    
    start_time = datetime.now() - timedelta(days=90)
    
    for i in range(75):
        dist = np.random.choice(districts)
        age = np.random.choice(age_groups)
        gender = np.random.choice(genders)
        occ = np.random.choice(occupations)
        
        # Determine average answer depending on location/occupation to make graphs look interesting
        # E.g., rural areas Kapit/Betong might have lower DI (Inclusion) but higher Ethics
        # Students might have higher privacy concerns
        avg_score = 3.2 # default neutral
        if dist in ["Kuching", "Miri", "Sibu"]:
            avg_score += 0.4 # Higher infrastructure, higher trust
        if dist in ["Kapit", "Betong"]:
            avg_score -= 0.3 # Rural infrastructure gaps, lower trust
        if occ == "Retired":
            avg_score -= 0.2
            
        # Generate random answers matching this profile
        answers = {}
        for q in survey.QUESTIONS:
            # Random score centered around our profile
            std_dev = 0.8
            val = int(round(np.clip(np.random.normal(avg_score, std_dev), 1, 5)))
            
            # Apply specific biases for specific variables
            # Rural areas evaluate Geographic Coverage lower
            if dist in ["Kapit", "Betong", "Limbang"] and q["variable"] == "V5.1":
                val = int(round(np.clip(val - 1.5, 1, 5)))
            # Students evaluate Privacy Resignation lower
            if occ == "Student" and q["variable"] == "V3.1":
                val = int(round(np.clip(val - 1.2, 1, 5)))
            # Security concerns are generally higher across the board
            if q["pillar"] == "P4" and q["variable"] == "V4.1":
                val = int(round(np.clip(val - 0.5, 1, 5)))
                
            answers[q["code"]] = val

        # Calculate scores
        results = survey.calculate_sttb_index(answers)
        
        # Save respondent
        sub_date = start_time + timedelta(days=float(np.random.uniform(0, 90)))
        cursor.execute("""
        INSERT INTO respondents (age_group, gender, occupation, district, submitted_at)
        VALUES (?, ?, ?, ?, ?)
        """, (age, gender, occ, dist, sub_date.strftime("%Y-%m-%d %H:%M:%S")))
        
        resp_id = cursor.lastrowid
        
        # Save responses json
        import json
        cursor.execute("""
        INSERT INTO survey_responses (respondent_id, responses_json)
        VALUES (?, ?)
        """, (resp_id, json.dumps(answers)))
        
        # Save computed scores
        cursor.execute("""
        INSERT INTO computed_scores (
            respondent_id, ps1_transparency, ps2_ethics, ps3_privacy, ps4_security, ps5_inclusion, sttb_index, trust_level
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            resp_id, 
            results["pillar_scores"]["P1"],
            results["pillar_scores"]["P2"],
            results["pillar_scores"]["P3"],
            results["pillar_scores"]["P4"],
            results["pillar_scores"]["P5"],
            results["sttb_index"],
            results["trust_evaluation"]["level"]
        ))
        
    conn.commit()
    conn.close()


def save_survey_submission(demographics, answers):
    """Saves a raw submission, calculates scores, and returns results dict."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Insert respondent
        cursor.execute("""
        INSERT INTO respondents (age_group, gender, occupation, district)
        VALUES (?, ?, ?, ?)
        """, (demographics["age"], demographics["gender"], demographics["occupation"], demographics["district"]))
        
        resp_id = cursor.lastrowid
        
        # 2. Compute index scores
        results = survey.calculate_sttb_index(answers)
        
        # 3. Save raw answers as JSON
        import json
        cursor.execute("""
        INSERT INTO survey_responses (respondent_id, responses_json)
        VALUES (?, ?)
        """, (resp_id, json.dumps(answers)))
        
        # 4. Save computed results
        cursor.execute("""
        INSERT INTO computed_scores (
            respondent_id, ps1_transparency, ps2_ethics, ps3_privacy, ps4_security, ps5_inclusion, sttb_index, trust_level
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            resp_id,
            results["pillar_scores"]["P1"],
            results["pillar_scores"]["P2"],
            results["pillar_scores"]["P3"],
            results["pillar_scores"]["P4"],
            results["pillar_scores"]["P5"],
            results["sttb_index"],
            results["trust_evaluation"]["level"]
        ))
        
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        st.error(f"Failed to record survey submission: {e}")
        return None
    finally:
        conn.close()


# ---------------------------------------------------------
# 3. GEOGRAPHIC DATA AND MAP SETUP
# ---------------------------------------------------------
# Center coordinates of the 12 divisions of Sarawak
SARAWAK_DIVISIONS = {
    "Kuching": {"lat": 1.5533, "lon": 110.3592},
    "Samarahan": {"lat": 1.4842, "lon": 110.4988},
    "Serian": {"lat": 1.1687, "lon": 110.5692},
    "Sri Aman": {"lat": 1.2333, "lon": 111.5000},
    "Betong": {"lat": 1.4167, "lon": 111.5333},
    "Sarikei": {"lat": 2.1167, "lon": 111.5167},
    "Sibu": {"lat": 2.3000, "lon": 111.8333},
    "Kapit": {"lat": 2.0167, "lon": 112.9333},
    "Mukah": {"lat": 2.9000, "lon": 112.0833},
    "Bintulu": {"lat": 3.1667, "lon": 113.0333},
    "Miri": {"lat": 4.3833, "lon": 113.9833},
    "Limbang": {"lat": 4.7500, "lon": 115.0000}
}


# Initialize DB
init_db()

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "Welcome & Overview"

if "language" not in st.session_state:
    st.session_state["language"] = "English"

# Secure Hidden Admin Portal Initialization
if "admin_mode" not in st.session_state:
    st.session_state["admin_mode"] = False

# Enable admin mode securely via secret URL query parameters
if "admin" in st.query_params and st.query_params["admin"] == "true":
    st.session_state["admin_mode"] = True
elif "audit" in st.query_params and st.query_params["audit"] == "uts":
    st.session_state["admin_mode"] = True

# Normalize legacy language selections
if st.session_state.get("language") == "Bahasa Malaysia":
    st.session_state["language"] = "Bahasa Melayu"

# Dynamic Multilanguage Translation Dictionary (English and Bahasa Melayu only)
TRANSLATIONS = {
    "English": {
        "overview": "Overview",
        "survey": "Survey",
        "dashboard": "Dashboard",
        "map": "Map",
        "help": "Help",
        "admin": "Admin"
    },
    "Bahasa Melayu": {
        "overview": "Ringkasan",
        "survey": "Soal Selidik",
        "dashboard": "Papan Pemuka",
        "map": "Peta Kawasan",
        "help": "Bantuan",
        "admin": "Admin"
    }
}

lang = st.session_state.get("language", "English")

# ---------------------------------------------------------
# 4. TOP NAVIGATION BAR & THEME SYMBOL
# ---------------------------------------------------------
# Determine theme variables for navbar styling
if st.session_state.get("theme_mode", "Dark Mode") == "Dark Mode":
    nav_bg = "rgba(22, 22, 26, 0.85)"
    nav_border = "rgba(255, 199, 44, 0.2)"
    nav_text = "#ffffff"
    nav_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.4)"
else:
    nav_bg = "rgba(255, 255, 255, 0.85)"
    nav_border = "rgba(0, 0, 0, 0.08)"
    nav_text = "#1a1a24"
    nav_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.08)"

# Container/styling for unified horizontal navbar strip
st.markdown(f"""
<style>
    /* Styling to make the first stHorizontalBlock a premium unified navbar strip */
    div[data-testid="stHorizontalBlock"]:first-of-type {{
        background: {nav_bg} !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid {nav_border} !important;
        border-radius: 12px !important;
        padding: 10px 25px !important;
        margin-bottom: 30px !important;
        box-shadow: {nav_shadow} !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    /* Center columns vertically in the nav container */
    div[data-testid="stHorizontalBlock"]:first-of-type > div {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    /* Override standard button styling inside the top navbar block to look like premium text links */
    div[data-testid="stHorizontalBlock"]:first-of-type div.stButton > button {{
        background: transparent !important;
        color: {nav_text} !important;
        border: none !important;
        box-shadow: none !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1.02rem !important;
        border-radius: 0px !important;
        padding: 4px 0px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        height: auto !important;
        margin: 0 !important;
        border-bottom: 2px solid transparent !important;
    }}
    
    /* Highlight the active page/language selection with dynamic word color and a clean underline */
    div[data-testid="stHorizontalBlock"]:first-of-type div.stButton > button[kind="primary"] {{
        background: transparent !important;
        color: #FFC72C !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        border-bottom: 2px solid #DA291C !important;
    }}
    
    /* Hover effect: text turns yellow/gold and shows a faint bottom underline */
    div[data-testid="stHorizontalBlock"]:first-of-type div.stButton > button:hover {{
        background: transparent !important;
        color: #FFC72C !important;
        border-bottom: 2px solid rgba(255, 199, 44, 0.5) !important;
    }}
</style>
""", unsafe_allow_html=True)

# Determine dynamic navigation layout based on admin_mode status
has_admin_tab = st.session_state.get("admin_mode", False)

if has_admin_tab:
    # 8-column layout: Logo, 5 Menu Buttons, Language, Theme Toggle
    nav_cols = st.columns([0.8, 1.1, 1.2, 1.2, 1.2, 1.0, 1.2, 0.5], vertical_alignment="center")
    menu_options = [
        ("Welcome & Overview", TRANSLATIONS[lang]["overview"]),
        ("Public Survey Form", TRANSLATIONS[lang]["survey"]),
        ("Analytics Dashboard", TRANSLATIONS[lang]["dashboard"]),
        ("Help / Feedback", TRANSLATIONS[lang]["help"]),
        ("Admin Panel", TRANSLATIONS[lang]["admin"])
    ]
    lang_col_idx = 6
    theme_col_idx = 7
    sub_strip_widths = [5.6, 1.4, 1.8]
else:
    # 7-column layout: Logo, 4 Menu Buttons, Language, Theme Toggle
    nav_cols = st.columns([1.0, 1.3, 1.3, 1.4, 1.3, 1.5, 0.6], vertical_alignment="center")
    menu_options = [
        ("Welcome & Overview", TRANSLATIONS[lang]["overview"]),
        ("Public Survey Form", TRANSLATIONS[lang]["survey"]),
        ("Analytics Dashboard", TRANSLATIONS[lang]["dashboard"]),
        ("Help / Feedback", TRANSLATIONS[lang]["help"])
    ]
    lang_col_idx = 5
    theme_col_idx = 6
    sub_strip_widths = [5.3, 1.5, 2.0]

# Column 0: Premium STTB Hornbill Logo
with nav_cols[0]:
    st.image("Frontend/sttb_official_logo.png", width=65 if has_admin_tab else 80)

# Columns 1-5 or 1-6: Horizontal Navigation Menus
for idx, (page_val, label) in enumerate(menu_options):
    with nav_cols[idx + 1]:
        is_active = (st.session_state["page"] == page_val)
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_{page_val}", type=btn_type, use_container_width=True):
            st.session_state["page"] = page_val
            st.rerun()

# Column 6 or 7: Minimalist Language toggle link
with nav_cols[lang_col_idx]:
    is_lang_menu_open = st.session_state.get("show_lang_options", False)
    btn_kind = "primary" if is_lang_menu_open else "secondary"
    if st.button("Language", key="nav_language_toggle", type=btn_kind, use_container_width=True):
        st.session_state["show_lang_options"] = not is_lang_menu_open
        st.rerun()

# Column 7 or 8: Theme Selector Symbol (☾ for Dark, ☀ for Light)
with nav_cols[theme_col_idx]:
    current_symbol = "☀" if st.session_state["theme_mode"] == "Dark Mode" else "☾"
    if st.button(current_symbol, key="theme_toggle_btn", use_container_width=True):
        if st.session_state["theme_mode"] == "Dark Mode":
            st.session_state["theme_mode"] = "Light Mode"
        else:
            st.session_state["theme_mode"] = "Dark Mode"
        st.rerun()

# ---------------------------------------------------------
# DYNAMIC LANGUAGE DROPDOWN SUB-STRIP
# ---------------------------------------------------------
if st.session_state.get("show_lang_options", False):
    # Render language options right-aligned in a clean, non-wrapping thin row (English and Bahasa Melayu only)
    st.markdown("<div style='margin-top: -15px;'></div>", unsafe_allow_html=True)
    sub_cols = st.columns(sub_strip_widths)
    
    with sub_cols[1]:
        if st.button("English", key="lang_opt_English", type="primary" if lang == "English" else "secondary", use_container_width=True):
            st.session_state["language"] = "English"
            st.session_state["show_lang_options"] = False
            st.rerun()
            
    with sub_cols[2]:
        if st.button("Bahasa Melayu", key="lang_opt_Malay", type="primary" if lang == "Bahasa Melayu" else "secondary", use_container_width=True):
            st.session_state["language"] = "Bahasa Melayu"
            st.session_state["show_lang_options"] = False
            st.rerun()
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)


# Get current page selection from session state
page = st.session_state.get("page", "Welcome & Overview")

# ---------------------------------------------------------
# ---------------------------------------------------------
# PAGE 1: WELCOME & OVERVIEW
# ---------------------------------------------------------
if page == "Welcome & Overview":
    if lang == "Bahasa Melayu":
        st.markdown('<div class="glass-header"><h1>Barometer Kepercayaan Teknologi Sarawak (STTB)</h1><div class="subtitle">Kerangka Sosio-Teknikal untuk Pengukuran Kepercayaan Digital di Sarawak</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-header"><h1>Sarawak Tech-Trust Barometer (STTB)</h1><div class="subtitle">A Social-Technical Framework for Digital Trust Measurement in Sarawak</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        if lang == "Bahasa Melayu":
            st.markdown(f"""
            <div class="glass-card">
                <h3>Mengenai Projek</h3>
                <p><b>Barometer Kepercayaan Teknologi Sarawak (STTB)</b> ialah projek tahun akhir Research and Development(R&D) yang dibangunkan untuk menangani jurang kritikal dalam mengukur dan menjejaki kepercayaan orang ramai terhadap teknologi digital dan institusi di seluruh bahagian pentadbiran di Sarawak.</p>
                <p>Sejajar secara langsung dengan <b>Strategi Perbadanan Ekonomi Digital Sarawak (SDEC)</b> dan dasar digital kebangsaan, platform ini menyediakan pembuat dasar, penyelidik akademik, dan rakyat dengan penunjuk telus dan masa nyata mengenai cara platform digital mengendalikan privasi data, etika, kebolehcapaian dan keselamatan.</p>
                <p>Seni bina pemarkahan kami distrukturkan secara saintifik merentasi <b>5 teras tonggak kepercayaan digital</b>, dipetakan terhadap <b>15 pemboleh ubah analisis</b>, dan dikira daripada instrumen tinjauan <b>75-item komprehensif</b> yang berasaskan Teori Institusi sosiologi oleh W. Richard Scott (1995) dan diperhalusi melalui paradigma etika perundangan Islam.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="glass-card">
                <h3>Lima Tonggak Kepercayaan Digital</h3>
                <p>Setiap tonggak mewakili paksi kritikal penilaian awam:</p>
                <ul>
                    <li><b>1. Ketelusan & Kebolehcapaian (Sidq & Tabayyun)</b>: Membuka proses algoritma, dasar bahasa mudah, dan menangani jurang maklumat antara kerajaan dan rakyat.</li>
                    <li><b>2. Etika & Tanggungjawab (Amanah)</b>: Mempromosikan reka bentuk perisian yang adil, tanpa kecenderungan algoritma, dan pemimpin yang mengambil alih pengurusan kebajikan sivik.</li>
                    <li><b>3. Privasi & Kawalan (Tajassus & Haya)</b>: Mencegah pencerobohan tanpa kebenaran, memberikan pilihan persetujuan terperinci, dan mengurangkan peletakan jawatan digital.</li>
                    <li><b>4. Keselamatan & Kebolehpercayaan (Itqan)</b>: Memintasi kecemerlangan teknikal, daya tahan infrastruktur, dan masa henti perkhidmatan yang rendah.</li>
                    <li><b>5. Inklusi Digital & Kesaksamaan (Adl)</b>: Mengimbangi liputan geografi antara zon bandar dan luar bandar, menyokong literasi digital, dan kebolehcapaian untuk kumpulan terpinggir.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="glass-card">
                <h3>About The Project</h3>
                <p>The <b>Sarawak Tech-Trust Barometer (STTB)</b> is an R&D final year project developed to address the critical gaps in measuring and tracking public trust in digital technologies and institutions across the administrative divisions of Sarawak.</p>
                <p>Aligning directly with the <b>Sarawak Digital Economy Corporation (SDEC) Strategy</b> and national digital policies, the platform provides policymakers, academic researchers, and citizens with transparent, real-time indicators regarding how digital platforms handle data privacy, ethics, accessibility, and security.</p>
                <p>Our scoring architecture is scientifically structured across <b>5 core digital trust pillars</b>, mapped against <b>15 analytical variables</b>, and calculated from a comprehensive <b>75-item survey instrument</b> grounded in the sociological Institutional Theory by W. Richard Scott (1995) and refined through the ethical paradigms of Islamic jurisprudence.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="glass-card">
                <h3>The Five Digital Trust Pillars</h3>
                <p>Each pillar represents a critical axis of public evaluation:</p>
                <ul>
                    <li><b>1. Transparency & Accessibility (Sidq & Tabayyun)</b>: Opening algorithmic processes, plain language policies, and addressing information gaps between state and citizen.</li>
                    <li><b>2. Ethics & Responsibility (Amanah)</b>: Promoting fair software designs, algorithmic non-bias, and leaders taking stewardship of civic welfare.</li>
                    <li><b>3. Privacy & Control (Tajassus & Haya)</b>: Preventing unauthorized intrusion, giving granular consent options, and mitigating digital resignation.</li>
                    <li><b>4. Security & Reliability (Itqan)</b>: Ensuring technical excellence, infrastructure resilience, and low service downtime.</li>
                    <li><b>5. Digital Inclusion & Equity (Adl)</b>: Balancing geographic coverage between urban and rural zones, supporting digital literacy, and accessibility for marginalized groups.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # Display current dashboard statistics
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM respondents")
        total_resp = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(sttb_index) FROM computed_scores")
        state_avg = cursor.fetchone()[0]
        
        conn.close()
        
        if total_resp == 0:
            if lang == "Bahasa Melayu":
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <h3>Metrik Barometer Langsung</h3>
                    <div style="margin: 20px 0;">
                        <div class="metric-label">Indeks Kepercayaan Teknologi Sarawak</div>
                        <div class="metric-value" style="font-size: 2.2rem; color: #bdc3c7; margin: 15px 0;">Menunggu Data</div>
                        <div class="metric-label" style="color: #bdc3c7; font-weight:bold;">Belum Ada Hantaran</div>
                    </div>
                    <p style="font-size:0.85rem; color:#bdc3c7;">
                        Jadilah responden pertama untuk memulakan barometer kepercayaan digital!
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <h3>Live Barometer Metrics</h3>
                    <div style="margin: 20px 0;">
                        <div class="metric-label">Sarawak Tech-Trust Index</div>
                        <div class="metric-value" style="font-size: 2.2rem; color: #bdc3c7; margin: 15px 0;">Awaiting Data</div>
                        <div class="metric-label" style="color: #bdc3c7; font-weight:bold;">No Submissions Yet</div>
                    </div>
                    <p style="font-size:0.85rem; color:#bdc3c7;">
                        Be the very first respondent to initialize the digital trust barometer!
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            t_eval = survey.get_trust_level(state_avg)
            bm_levels = {
                "High Trust": "Kepercayaan Tinggi",
                "Moderate Trust": "Kepercayaan Sederhana",
                "Low Trust": "Kepercayaan Rendah",
                "Very Low Trust": "Kepercayaan Sangat Rendah"
            }
            level_str = bm_levels.get(t_eval["level"], t_eval["level"]) if lang == "Bahasa Melayu" else t_eval["level"]
            
            if lang == "Bahasa Melayu":
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <h3>Metrik Barometer Langsung</h3>
                    <div style="margin: 20px 0;">
                        <div class="metric-label">Indeks Kepercayaan Teknologi Sarawak</div>
                        <div class="metric-value">{state_avg:.2f}</div>
                        <div class="metric-label" style="color: {t_eval['color']}; font-weight:bold;">
                            {level_str}
                        </div>
                    </div>
                    <p style="font-size:0.85rem; color:#bdc3c7;">
                        Indeks dikemas kini secara automatik dalam masa nyata apabila respons tinjauan awam baharu direkodkan.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <h3>Live Barometer Metrics</h3>
                    <div style="margin: 20px 0;">
                        <div class="metric-label">Sarawak Tech-Trust Index</div>
                        <div class="metric-value">{state_avg:.2f}</div>
                        <div class="metric-label" style="color: {t_eval['color']}; font-weight:bold;">
                            {t_eval['level']}
                        </div>
                    </div>
                    <p style="font-size:0.85rem; color:#bdc3c7;">
                        Index updates automatically in real-time as new public survey responses are recorded.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Take survey redirect button
        btn_label = "Mulakan Tinjauan Kepercayaan Digital" if lang == "Bahasa Melayu" else "Begin Digital Trust Survey"
        if st.button(btn_label, use_container_width=True):
            st.session_state["page"] = "Public Survey Form"
            st.rerun()
        
        if lang == "Bahasa Melayu":
            st.markdown("""
            <div class="glass-card">
                <h3>Integrasi Kerangka Teori</h3>
                <p>Skema pangkalan data dan model pemarkahan bipartit kami disintesis di sekitar Tiga Tonggak Institusi W. Richard Scott:</p>
                <ol>
                    <li><b>Tonggak Regulatif</b>: Dipetakan kepada peraturan Keselamatan dan Privasi (pematuhan PDPA 2010).</li>
                    <li><b>Tonggak Normatif</b>: Dipetakan kepada Ketelusan dan Etika (piawaian kebolehpercayaan).</li>
                    <li><b>Tonggak Budaya-Kognitif</b>: Dipetakan kepada Inklusi Digital (pengagihan adil, literasi digital kognitif).</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card">
                <h3>Theoretical Framework Integration</h3>
                <p>Our database schema and bipartite scoring models are synthesized around W. Richard Scott's <b>Three Pillars of Institutions</b>:</p>
                <ol>
                    <li><b>Regulative Pillar</b>: Mapped to <i>Security</i> and <i>Privacy</i> rules (PDPA 2010 compliance).</li>
                    <li><b>Normative Pillar</b>: Mapped to <i>Transparency</i> and <i>Ethics</i> (trustworthiness standards).</li>
                    <li><b>Cultural-Cognitive Pillar</b>: Mapped to <i>Digital Inclusion</i> (fair distribution, cognitive digital literacy).</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)


# ---------------------------------------------------------
# PAGE 2: PUBLIC SURVEY FORM
elif page == "Public Survey Form":
    if lang == "Bahasa Melayu":
        st.markdown('<div class="glass-header"><h1>Borang Tinjauan Awam STTB</h1><div class="subtitle">Kerangka Maklum Balas Sivik Tanpa Nama (Patuh PDPA 2010)</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-header"><h1>STTB Public Survey Form</h1><div class="subtitle">Anonymized Civic Feedback Framework (PDPA 2010 Compliant)</div></div>', unsafe_allow_html=True)
    
    # Minimalist dynamic QR sharing code on top
    if lang == "Bahasa Melayu":
        st.markdown(f"""
        <div class="glass-card" style="padding: 15px; margin-bottom: 20px;">
            <h4 style="margin: 0 0 5px 0; color:{gold_color};">Imbas & Kongsi Tinjauan</h4>
            <p style="font-size: 0.85rem; color: #bdc3c7; margin: 0 0 12px 0;">Gunakan kod QR di bawah untuk mengakses dan mengedarkan tinjauan kepercayaan digital ini secara dalam talian!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="glass-card" style="padding: 15px; margin-bottom: 20px;">
            <h4 style="margin: 0 0 5px 0; color:{gold_color};">Scan & Share Survey</h4>
            <p style="font-size: 0.85rem; color: #bdc3c7; margin: 0 0 12px 0;">Use the QR code below to access and distribute this digital trust survey online!</p>
        </div>
        """, unsafe_allow_html=True)
    
    qr_col1, qr_col2 = st.columns([1, 4])
    with qr_col1:
        target_url = "https://sarawak-tech-trust.streamlit.app"
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&color=003366&data={target_url}"
        st.markdown(f'<img src="{qr_api_url}" style="border: 3px solid white; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);" width="110" height="110">', unsafe_allow_html=True)
    with qr_col2:
        if lang == "Bahasa Melayu":
            st.markdown(f"""
            <div style="padding-top: 10px;">
                <span style="font-size:0.85rem; color:#bdc3c7;"><b>Pautan Langsung:</b></span><br>
                <a href="{target_url}" target="_blank" style="color:{gold_color}; font-size:1.05rem; font-weight:bold; text-decoration:none;">{target_url}</a>
                <p style="font-size:0.8rem; color:#888888; margin-top:5px; margin-bottom:0;">Klik kanan imej kod QR untuk menyimpan atau menyalinnya terus ke dalam slaid tesis atau risalah.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="padding-top: 10px;">
                <span style="font-size:0.85rem; color:#bdc3c7;"><b>Direct Link:</b></span><br>
                <a href="{target_url}" target="_blank" style="color:{gold_color}; font-size:1.05rem; font-weight:bold; text-decoration:none;">{target_url}</a>
                <p style="font-size:0.8rem; color:#888888; margin-top:5px; margin-bottom:0;">Right-click the QR code image to save or copy it directly into thesis slides or brochures.</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")
    
    if lang == "Bahasa Melayu":
        st.markdown("""
        <div class="glass-card">
            <h3>Arahan</h3>
            <p>Tinjauan ini mengumpul penilaian anda mengenai alat digital dan platform negeri di Sarawak. <b>Tiada data pengenalan peribadi (PII) disimpan.</b> Sila pilih demografi anda dan jawab soalan di bawah.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card">
            <h3>Instructions</h3>
            <p>This survey collects your evaluation regarding digital tools and state platforms in Sarawak. <b>No personally identifiable data (PII) is stored.</b> Please select your demographics and answer the questions below.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 1. Capture Demographics
    dem_title = "Langkah 1: Demarkasi Demografi" if lang == "Bahasa Melayu" else "Step 1: Demographic Demarcation"
    st.markdown(f"<h3 style='color:{gold_color};'>{dem_title}</h3>", unsafe_allow_html=True)
    
    age_label = "Kumpulan Umur" if lang == "Bahasa Melayu" else "Age Group"
    age_group = st.selectbox(age_label, ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"])
    
    gender_label = "Jantina" if lang == "Bahasa Melayu" else "Gender"
    gender_options = ["Lelaki", "Perempuan"] if lang == "Bahasa Melayu" else ["Male", "Female"]
    gender_selected = st.selectbox(gender_label, gender_options)
    gender = "Male" if gender_selected in ["Male", "Lelaki"] else "Female"
    
    occ_label = "Pekerjaan" if lang == "Bahasa Melayu" else "Occupation"
    occ_options_en = ["Student", "Civil Servant", "Private Sector", "Self-Employed", "Retired", "Unemployed"]
    occ_options_bm = ["Pelajar", "Penjawat Awam", "Sektor Swasta", "Bekerja Sendiri", "Pesara", "Tidak Bekerja"]
    occ_selected = st.selectbox(occ_label, occ_options_bm if lang == "Bahasa Melayu" else occ_options_en)
    occ_mapping = dict(zip(occ_options_bm, occ_options_en))
    occupation = occ_mapping.get(occ_selected, occ_selected)
    
    div_label = "Bahagian Sarawak" if lang == "Bahasa Melayu" else "Sarawak Division"
    div_options = list(SARAWAK_DIVISIONS.keys()) + (["Lain-lain"] if lang == "Bahasa Melayu" else ["Others"])
    div_selected = st.selectbox(div_label, div_options)
    district = "Others" if div_selected in ["Others", "Lain-lain"] else div_selected
        
    st.markdown("---")
    
    # 2. Select Survey Type to avoid exhaustion
    mode_label = "Pilih Mod Tinjauan:" if lang == "Bahasa Melayu" else "Choose Survey Mode:"
    mode_options = [
        "Tinjauan Akademik Penuh (75 Soalan - Boleh Dilipat)" if lang == "Bahasa Melayu" else "Full Academic Survey (75 Questions - Collapsible)",
        "Tinjauan Mini Pantas (15 Soalan - Disyorkan untuk ujian cepat)" if lang == "Bahasa Melayu" else "Rapid Mini-Survey (15 Questions - Recommended for quick testing)"
    ]
    survey_type_selected = st.radio(mode_label, mode_options, horizontal=True)
    survey_type = "75" if "75" in survey_type_selected else "15"
    
    survey_answers = {}
    
    if "75" in survey_type:
        sec_title = "Langkah 2: Penilaian Teras Kepercayaan Digital (75 Item)" if lang == "Bahasa Melayu" else "Step 2: Core Digital Trust Evaluation (75 Items)"
        sec_desc = "Soalan dikategorikan mengikut 5 tonggak utama kepercayaan digital kami. Kembangkan setiap tab untuk menjawab. Skala: 1 = Sangat Tidak Setuju, 5 = Sangat Setuju." if lang == "Bahasa Melayu" else "Questions are categorized by our 5 key digital trust pillars. Expand each tab to answer. Scale: 1 = Strongly Disagree, 5 = Strongly Agree."
        st.markdown(f"<h3 style='color:{gold_color};'>{sec_title}</h3>", unsafe_allow_html=True)
        st.write(sec_desc)
        
        # We render 5 expanding tabs (one for each pillar)
        p_codes = ["P1", "P2", "P3", "P4", "P5"]
        for p_code in p_codes:
            pillar_info = survey.SURVEY_METADATA["pillars"][p_code]
            
            # Localized pillars
            bm_pillar_names = {
                "P1": ("Ketelusan & Kebolehcapaian", "Sidq (Kebenaran) & Tabayyun (Pengesahan)"),
                "P2": ("Etika & Tanggungjawab", "Amanah (Kebolehpercayaan) & Kewalihan (Stewardship)"),
                "P3": ("Privasi & Kawalan", "Larangan Tajassus (Larangan Mengintip) & Haya (Kehormatan/Kesopanan)"),
                "P4": ("Keselamatan & Kebolehpercayaan", "Itqan (Kecemerlangan dan Ketepatan)"),
                "P5": ("Inklusi Digital & Kesaksamaan", "Adl (Keadilan dan Kesaksamaan)")
            }
            bm_pillar_defs = {
                "P1": "Tahap di mana institusi digital di Sarawak bersikap terbuka, jujur, dan mudah diakses dalam penyampaian maklumat penggunaan data, dasar, dan keputusan.",
                "P2": "Tahap di mana institusi digital di Sarawak mengutamakan tingkah laku beretika, kebertanggungjawaban, dan tadbir urus yang bertanggungjawab melebihi sekadar pematuhan undang-undang.",
                "P3": "Tahap di mana pengguna merasa diberi kuasa dengan agensi yang bermakna ke atas maklumat peribadi mereka, dilindungi daripada pencerobohan, selaras dengan PDPA 2010.",
                "P4": "Tahap di mana infrastruktur dan perkhidmatan digital Sarawak dilindungi secara teknikal, berdaya tahan, dan sentiasa tersedia secara konsisten.",
                "P5": "Tahap di mana perkhidmatan digital, infrastruktur, dan sokongan literasi boleh diakses secara saksama kepada semua komuniti di seluruh Sarawak."
            }
            
            p_name = bm_pillar_names[p_code][0] if lang == "Bahasa Melayu" else pillar_info['name']
            p_concept = bm_pillar_names[p_code][1] if lang == "Bahasa Melayu" else pillar_info['islamic_concept']
            p_def = bm_pillar_defs[p_code] if lang == "Bahasa Melayu" else pillar_info['definition']
            
            with st.expander(f"Pillar: {p_name} ({p_concept})"):
                st.write(f"*{p_def}*")
                
                # Variables translations mapping for BM
                bm_var_names = {
                    "V1.1": "Asimetri Maklumat",
                    "V1.2": "Pengecualian Digital",
                    "V1.3": "Penyembunyian Kebenaran",
                    "V2.1": "Bias Algoritma",
                    "V2.2": "Kekurangan Kebertanggungjawaban",
                    "V2.3": "Pecah Amanah",
                    "V3.1": "Kepasrahan Digital",
                    "V3.2": "Pencerobohan Tanpa Kebenaran (Tajassus)",
                    "V3.3": "Kecurian Identiti & Pemalsuan Data",
                    "V4.1": "Kerapuhan Sistemik",
                    "V4.2": "Gangguan Perkhidmatan Kerap",
                    "V4.3": "Jurang Integriti Perisian",
                    "V5.1": "Liputan Geografi",
                    "V5.2": "Sokongan Literasi Digital",
                    "V5.3": "Inklusiviti untuk Kumpulan Terpinggir"
                }
                
                # Group questions by variable inside the expander
                for var_code, var_name_en in pillar_info["variables"].items():
                    var_display_name = bm_var_names[var_code] if lang == "Bahasa Melayu" else var_name_en
                    var_prefix = "Pemboleh Ubah:" if lang == "Bahasa Melayu" else "Variable:"
                    st.markdown(f"<h4 style='color:{gold_color}; margin-top:20px; margin-bottom:10px;'>Pillar: {p_name} — {var_prefix} {var_display_name}</h4>", unsafe_allow_html=True)
                    
                    var_questions = [q for q in survey.QUESTIONS if q["pillar"] == p_code and q["variable"] == var_code]
                    for q in var_questions:
                        q_text = survey.QUESTIONS_BM.get(q["code"], q["question"]) if lang == "Bahasa Melayu" else q["question"]
                        key = f"q_{q['code']}"
                        
                        options_list = [
                            "Sangat Tidak Setuju" if lang == "Bahasa Melayu" else "Strongly Disagree",
                            "Tidak Setuju" if lang == "Bahasa Melayu" else "Disagree",
                            "Neutral" if lang == "Bahasa Melayu" else "Neutral",
                            "Setuju" if lang == "Bahasa Melayu" else "Agree",
                            "Sangat Setuju" if lang == "Bahasa Melayu" else "Strongly Agree"
                        ]
                        
                        selected_ans = st.radio(
                            q_text,
                            options=options_list,
                            index=2,
                            horizontal=True,
                            key=key
                        )
                        survey_answers[q["code"]] = options_list.index(selected_ans) + 1
    else:
        sec_title = "Langkah 2: Penilaian Teras Kepercayaan Digital (15 Item Perwakilan)" if lang == "Bahasa Melayu" else "Step 2: Core Digital Trust Evaluation (15 Representative Items)"
        sec_desc = "Tinjauan mini ini mengandungi tepat 1 soalan bagi setiap pemboleh ubah (15 jumlah) yang mewakili skala kerangka kerja lengkap. Purata akan diekstrapolasi secara automatik." if lang == "Bahasa Melayu" else "This mini-survey contains exactly 1 question per variable (15 total) representing the complete framework scale. Averages will be extrapolated automatically."
        st.markdown(f"<h3 style='color:{gold_color};'>{sec_title}</h3>", unsafe_allow_html=True)
        st.write(sec_desc)
        
        # Interactive printable survey PDF download (Emoji-free)
        pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sttb_rapid_survey.pdf'))
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            dl_label = "Muat Turun Borang Tinjauan PDF (Boleh Dicetak)" if lang == "Bahasa Melayu" else "Download Printable Survey PDF"
            st.download_button(
                label=dl_label,
                data=pdf_bytes,
                file_name="sttb_rapid_survey.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # Render exactly one question per variable
        variables_featured = [
            "TA1.2", "TA2.2", "TA3.3",  # Pillar 1
            "ER1.3", "ER2.1", "ER3.1",  # Pillar 2
            "PC1.2", "PC2.1", "PC3.1",  # Pillar 3
            "SR1.1", "SR2.2", "SR3.4",  # Pillar 4
            "DI1.1", "DI2.3", "DI3.3",  # Pillar 5
        ]
        
        bm_var_names = {
            "V1.1": "Asimetri Maklumat",
            "V1.2": "Pengecualian Digital",
            "V1.3": "Penyembunyian Kebenaran",
            "V2.1": "Bias Algoritma",
            "V2.2": "Kekurangan Kebertanggungjawaban",
            "V2.3": "Pecah Amanah",
            "V3.1": "Kepasrahan Digital",
            "V3.2": "Pencerobohan Tanpa Kebenaran (Tajassus)",
            "V3.3": "Kecurian Identiti & Pemalsuan Data",
            "V4.1": "Kerapuhan Sistemik",
            "V4.2": "Gangguan Perkhidmatan Kerap",
            "V4.3": "Jurang Integriti Perisian",
            "V5.1": "Liputan Geografi",
            "V5.2": "Sokongan Literasi Digital",
            "V5.3": "Inklusiviti untuk Kumpulan Terpinggir"
        }
        
        rep_questions = [q for q in survey.QUESTIONS if q["code"] in variables_featured]
        for q in rep_questions:
            q_text = survey.QUESTIONS_BM.get(q["code"], q["question"]) if lang == "Bahasa Melayu" else q["question"]
            key = f"mini_{q['code']}"
            
            # Retrieve variable name and pillar name dynamically
            p_code = q["pillar"]
            v_code = q["variable"]
            bm_pillar_names = {
                "P1": "Ketelusan & Kebolehcapaian",
                "P2": "Etika & Tanggungjawab",
                "P3": "Privasi & Kawalan",
                "P4": "Keselamatan & Kebolehkenyamanan",
                "P5": "Inklusi Digital & Kesaksamaan"
            }
            pillar_info = survey.SURVEY_METADATA["pillars"][p_code]
            p_name = bm_pillar_names[p_code] if lang == "Bahasa Melayu" else pillar_info['name']
            
            var_name_en = pillar_info["variables"][v_code]
            var_display_name = bm_var_names[v_code] if lang == "Bahasa Melayu" else var_name_en
            var_prefix = "Pemboleh Ubah:" if lang == "Bahasa Melayu" else "Variable:"
            
            st.markdown(f"<h4 style='color:{gold_color}; margin-top:20px; margin-bottom:5px;'>Pillar: {p_name} — {var_prefix} {var_display_name}</h4>", unsafe_allow_html=True)
            
            options_list = [
                "Sangat Tidak Setuju" if lang == "Bahasa Melayu" else "Strongly Disagree",
                "Tidak Setuju" if lang == "Bahasa Melayu" else "Disagree",
                "Neutral" if lang == "Bahasa Melayu" else "Neutral",
                "Setuju" if lang == "Bahasa Melayu" else "Agree",
                "Sangat Setuju" if lang == "Bahasa Melayu" else "Strongly Agree"
            ]
            
            selected_ans = st.radio(
                q_text,
                options=options_list,
                index=2,
                horizontal=True,
                key=key
            )
            survey_answers[q["code"]] = options_list.index(selected_ans) + 1
            
        # Map remaining questions to the answered variable value to preserve database structure
        for q in survey.QUESTIONS:
            if q["code"] not in survey_answers:
                rep_code = [c for c in variables_featured if c.startswith(q['code'][:2])][0]
                survey_answers[q["code"]] = survey_answers[rep_code]
 
    sub_btn_label = "Hantar Penilaian Tanpa Nama" if lang == "Bahasa Melayu" else "Submit Anonymous Evaluation"
    submit_btn = st.button(sub_btn_label, use_container_width=True)
    
    if submit_btn:
        demographics = {
            "age": age_group,
            "gender": gender,
            "occupation": occupation,
            "district": district
        }
        
        results = save_survey_submission(demographics, survey_answers)
        
        if results:
            st.balloons()
            success_msg = "Terima kasih! Maklum balas kepercayaan digital tanpa nama anda telah berjaya dikira dan direkodkan." if lang == "Bahasa Melayu" else "Thank you! Your anonymous digital trust feedback has been securely computed and recorded."
            st.success(success_msg)
            
            # Show interactive report card
            card_title = "Kad Laporan Kepercayaan Digital Peribadi Anda" if lang == "Bahasa Melayu" else "Your Personal Digital Trust Report Card"
            idx_label = "Indeks STTB yang Dikira" if lang == "Bahasa Melayu" else "Computed STTB Index"
            
            bm_interpretations = {
                "High Trust": "Kepercayaan awam yang kuat terhadap institusi digital.",
                "Moderate Trust": "Kepercayaan digital awam yang munasabah tetapi boleh dipertingkatkan.",
                "Low Trust": "Defisit kepercayaan yang ketara memerlukan perhatian dasar.",
                "Very Low Trust": "Ketidakpercayaan digital yang meluas memerlukan pembaharuan segera."
            }
            bm_levels = {
                "High Trust": "Kepercayaan Tinggi",
                "Moderate Trust": "Kepercayaan Sederhana",
                "Low Trust": "Kepercayaan Rendah",
                "Very Low Trust": "Kepercayaan Sangat Rendah"
            }
            level_str = bm_levels.get(results['trust_evaluation']['level'], results['trust_evaluation']['level']) if lang == "Bahasa Melayu" else results['trust_evaluation']['level']
            interp_str = bm_interpretations.get(results['trust_evaluation']['level'], results['trust_evaluation']['interpretation']) if lang == "Bahasa Melayu" else results['trust_evaluation']['interpretation']
            
            st.markdown(f"""
            <div class="glass-card" style="border: 2px solid {results['trust_evaluation']['color']};">
                <h3 style="color: {results['trust_evaluation']['color']}; text-align: center;">
                    {card_title}
                </h3>
                <div style="text-align: center; margin: 20px 0;">
                    <div class="metric-label">{idx_label}</div>
                    <div class="metric-value" style="background:none; -webkit-text-fill-color: {results['trust_evaluation']['color']};">
                        {results['sttb_index']:.2f}
                    </div>
                    <div style="font-weight: 800; font-size: 1.3rem; color: {results['trust_evaluation']['color']};">
                        {level_str}
                    </div>
                    <p style="margin-top: 10px; font-size:0.9rem; color:#bdc3c7;">
                        {interp_str}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show breakdown
            col1, col2, col3, col4, col5 = st.columns(5)
            pillars_map_en = {
                "P1": "Transparency",
                "P2": "Ethics",
                "P3": "Privacy",
                "P4": "Security",
                "P5": "Inclusion"
            }
            pillars_map_bm = {
                "P1": "Ketelusan",
                "P2": "Etika",
                "P3": "Privasi",
                "P4": "Keselamatan",
                "P5": "Inklusi"
            }
            pillars_map = pillars_map_bm if lang == "Bahasa Melayu" else pillars_map_en
            
            for i, p_code in enumerate(["P1", "P2", "P3", "P4", "P5"]):
                score = results["pillar_scores"][p_code]
                color = survey.get_trust_level(score)["color"]
                with [col1, col2, col3, col4, col5][i]:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align:center; padding:15px; margin-bottom:0;">
                        <h4 style="margin:0; font-size:0.9rem;">{pillars_map[p_code]}</h4>
                        <div style="font-size:1.8rem; font-weight:800; color:{color};">{score:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# PAGE 3: ANALYTICS DASHBOARD
# --------------------------------------------------# ---------------------------------------------------------
# PAGE 3: ANALYTICS DASHBOARD
# ---------------------------------------------------------
elif page == "Analytics Dashboard":
    if lang == "Bahasa Melayu":
        st.markdown('<div class="glass-header"><h1>Papan Pemuka Analisis STTB</h1><div class="subtitle">Penunjuk Kepercayaan Masa Nyata & Penapis Demografi</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-header"><h1>STTB Analytics Dashboard</h1><div class="subtitle">Real-time Trust Indicators & Demographic Filters</div></div>', unsafe_allow_html=True)
    
    # Fetch all data from DB
    conn = get_db_connection()
    df_resp = pd.read_sql_query("SELECT * FROM respondents", conn)
    df_scores = pd.read_sql_query("SELECT * FROM computed_scores", conn)
    conn.close()
    
    # Merge datasets
    df = pd.merge(df_resp, df_scores, left_on="id", right_on="respondent_id")
    
    # Filter controls in sidebar-style layout inside dashboard
    filter_title = "Penapis Segmen Demografi" if lang == "Bahasa Melayu" else "Demographic Segment Filters"
    st.markdown(f"<h3 style='color:#ffd700;'>{filter_title}</h3>", unsafe_allow_html=True)
    
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    # Translate segment filters
    f_dist_lbl = "Tapis Bahagian" if lang == "Bahasa Melayu" else "Filter Division"
    f_age_lbl = "Tapis Kumpulan Umur" if lang == "Bahasa Melayu" else "Filter Age Group"
    f_gen_lbl = "Tapis Jantina" if lang == "Bahasa Melayu" else "Filter Gender"
    f_occ_lbl = "Tapis Pekerjaan" if lang == "Bahasa Melayu" else "Filter Occupation"
    
    all_label = "Semua" if lang == "Bahasa Melayu" else "All"
    
    # Map options for display
    occ_mapping_bm_en = {
        "Semua": "All",
        "Pelajar": "Student",
        "Penjawat Awam": "Civil Servant",
        "Sektor Swasta": "Private Sector",
        "Bekerja Sendiri": "Self-Employed",
        "Pesara": "Retired",
        "Tidak Bekerja": "Unemployed"
    }
    
    with f_col1:
        f_district_raw = st.multiselect(f_dist_lbl, [all_label] + list(SARAWAK_DIVISIONS.keys()) + (["Lain-lain"] if lang == "Bahasa Melayu" else ["Others"]), default=all_label)
    with f_col2:
        f_age = st.multiselect(f_age_lbl, [all_label, "18-24", "25-34", "35-44", "45-54", "55-64", "65+"], default=all_label)
    with f_col3:
        f_gender_raw = st.multiselect(f_gen_lbl, [all_label, "Lelaki" if lang == "Bahasa Melayu" else "Male", "Perempuan" if lang == "Bahasa Melayu" else "Female"], default=all_label)
    with f_col4:
        f_occ_raw = st.multiselect(f_occ_lbl, [all_label, "Pelajar" if lang == "Bahasa Melayu" else "Student", "Penjawat Awam" if lang == "Bahasa Melayu" else "Civil Servant", "Sektor Swasta" if lang == "Bahasa Melayu" else "Private Sector", "Bekerja Sendiri" if lang == "Bahasa Melayu" else "Self-Employed", "Pesara" if lang == "Bahasa Melayu" else "Retired", "Tidak Bekerja" if lang == "Bahasa Melayu" else "Unemployed"], default=all_label)
        
    # Map filters to DB equivalents
    f_district = []
    for d in f_district_raw:
        if d == all_label:
            f_district.append("All")
        elif d == "Lain-lain":
            f_district.append("Others")
        else:
            f_district.append(d)
            
    f_gender = []
    for g in f_gender_raw:
        if g == all_label:
            f_gender.append("All")
        elif g == "Lelaki":
            f_gender.append("Male")
        elif g == "Perempuan":
            f_gender.append("Female")
        else:
            f_gender.append(g)
            
    f_occ = []
    for o in f_occ_raw:
        if o == all_label:
            f_occ.append("All")
        else:
            f_occ.append(occ_mapping_bm_en.get(o, o))
            
    # Apply filtering logic
    df_filtered = df.copy()
    if f_district and "All" not in f_district:
        df_filtered = df_filtered[df_filtered["district"].isin(f_district)]
    if f_age and "All" not in f_age:
        df_filtered = df_filtered[df_filtered["age_group"].isin(f_age)]
    if f_gender and "All" not in f_gender:
        df_filtered = df_filtered[df_filtered["gender"].isin(f_gender)]
    if f_occ and "All" not in f_occ:
        df_filtered = df_filtered[df_filtered["occupation"].isin(f_occ)]
        
    if df_filtered.empty:
        warn_msg = "Tiada hantaran tinjauan yang sepadan dengan penapis yang dipilih. Set semula penapis untuk melihat data." if lang == "Bahasa Melayu" else "No survey submissions match the selected filters. Reset filters to see data."
        st.warning(warn_msg)
    else:
        # Show key metric cards
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            lbl1 = "Saiz Sampel Aktif (N)" if lang == "Bahasa Melayu" else "Active Sample Size (N)"
            lbl2 = "Respons Ditapis" if lang == "Bahasa Melayu" else "Filtered Responses"
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div class="metric-label">{lbl1}</div>
                <div class="metric-value" style="color:#ffd700;">{len(df_filtered)}</div>
                <div class="metric-label">{lbl2}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            idx_avg = df_filtered["sttb_index"].mean()
            eval_info = survey.get_trust_level(idx_avg)
            
            lbl_avg = "Indeks STTB Segmen" if lang == "Bahasa Melayu" else "Segment STTB Index"
            bm_levels = {
                "High Trust": "Kepercayaan Tinggi",
                "Moderate Trust": "Kepercayaan Sederhana",
                "Low Trust": "Kepercayaan Rendah",
                "Very Low Trust": "Kepercayaan Sangat Rendah"
            }
            level_str = bm_levels.get(eval_info["level"], eval_info["level"]) if lang == "Bahasa Melayu" else eval_info["level"]
            
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div class="metric-label">{lbl_avg}</div>
                <div class="metric-value" style="background:none; -webkit-text-fill-color: {eval_info['color']};">{idx_avg:.2f}</div>
                <div class="metric-label" style="color: {eval_info['color']}; font-weight:bold;">{level_str}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            # Find weakest pillar
            pillar_cols = [
                ("ps1_transparency", "Transparency"),
                ("ps2_ethics", "Ethics"),
                ("ps3_privacy", "Privacy"),
                ("ps4_security", "Security"),
                ("ps5_inclusion", "Inclusion")
            ]
            pillar_averages = {label: df_filtered[col].mean() for col, label in pillar_cols}
            weakest = min(pillar_averages, key=pillar_averages.get)
            weakest_val = pillar_averages[weakest]
            
            bm_pillars = {
                "Transparency": "Ketelusan",
                "Ethics": "Etika",
                "Privacy": "Privasi",
                "Security": "Keselamatan",
                "Inclusion": "Inklusi"
            }
            weakest_str = bm_pillars.get(weakest, weakest) if lang == "Bahasa Melayu" else weakest
            lbl_weak = "Paksi Kepercayaan Terlemah" if lang == "Bahasa Melayu" else "Weakest Trust Axis"
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div class="metric-label">{lbl_weak}</div>
                <div class="metric-value" style="color:#C0392B; font-size:2.2rem; margin:15px 0;">{weakest_str}</div>
                <div class="metric-label">Score: {weakest_val:.1f} / 100</div>
            </div>
            """, unsafe_allow_html=True)

        # 1. Bar Chart of 5 Pillars
        comp_title = "Perbandingan Profil Kepercayaan Tonggak" if lang == "Bahasa Melayu" else "Pillar Trust Profile Comparison"
        st.markdown(f"<h3 style='color:#ffd700; margin-top:20px;'>{comp_title}</h3>", unsafe_allow_html=True)
        
        translated_pillar_keys = [bm_pillars.get(k, k) if lang == "Bahasa Melayu" else k for k in pillar_averages.keys()]
        chart_data = pd.DataFrame({
            "Trust Pillar" if lang == "Bahasa Melayu" else "Trust Pillar": translated_pillar_keys,
            "Index Score" if lang == "Bahasa Melayu" else "Index Score": list(pillar_averages.values())
        })
        
        st.bar_chart(chart_data, x="Trust Pillar" if lang == "Bahasa Melayu" else "Trust Pillar", y="Index Score" if lang == "Bahasa Melayu" else "Index Score", color="#ffd700")

        # 2. Division Rankings Table
        rank_title = "Kedudukan Bahagian Pentadbiran" if lang == "Bahasa Melayu" else "Administrative Division Rankings"
        st.markdown(f"<h3 style='color:#ffd700; margin-top:20px;'>{rank_title}</h3>", unsafe_allow_html=True)
        
        div_summary = df_filtered.groupby("district").agg(
            respondents_count=("respondent_id", "count"),
            sttb_index_avg=("sttb_index", "mean")
        ).reset_index()
        
        div_summary = div_summary.sort_values(by="sttb_index_avg", ascending=False)
        
        # Formatting for presentation
        div_presentation = div_summary.copy()
        div_presentation["sttb_index_avg"] = div_presentation["sttb_index_avg"].round(2)
        div_presentation = div_presentation.rename(columns={
            "district": "Bahagian Sarawak" if lang == "Bahasa Melayu" else "Sarawak Division",
            "respondents_count": "Sampel (N)" if lang == "Bahasa Melayu" else "Sample (N)",
            "sttb_index_avg": "Indeks STTB (0-100)" if lang == "Bahasa Melayu" else "STTB Index (0-100)"
        })
        
        if lang == "Bahasa Melayu":
            div_presentation["Bahagian Sarawak"] = div_presentation["Bahagian Sarawak"].replace({"Others": "Lain-lain"})
        
        st.dataframe(
            div_presentation[[
                "Bahagian Sarawak" if lang == "Bahasa Melayu" else "Sarawak Division",
                "Sampel (N)" if lang == "Bahasa Melayu" else "Sample (N)",
                "Indeks STTB (0-100)" if lang == "Bahasa Melayu" else "STTB Index (0-100)"
            ]],
            hide_index=True,
            use_container_width=True
        )
        
        # 3. Interactive Geographic Digital Trust Map
        map_title = "Peta Kepercayaan Geografi Sarawak" if lang == "Bahasa Melayu" else "Geographic Sarawak Digital Trust Map"
        st.markdown(f"<h3 style='color:{gold_color}; margin-top:20px;'>{map_title}</h3>", unsafe_allow_html=True)
        
        # Calculate division averages from df_filtered
        div_stats = df_filtered.groupby("district").agg(
            sttb_index=("sttb_index", "mean"),
            count=("respondent_id", "count"),
            transparency=("ps1_transparency", "mean"),
            ethics=("ps2_ethics", "mean"),
            privacy=("ps3_privacy", "mean"),
            security=("ps4_security", "mean"),
            inclusion=("ps5_inclusion", "mean")
        ).to_dict("index")
        
        # Setup Folium Map centered on Sarawak
        m = folium.Map(location=[2.5000, 113.0000], zoom_start=7, tiles="cartodbpositron")
        
        # Add colored markers representing division trust
        for div_name, coords in SARAWAK_DIVISIONS.items():
            stats = div_stats.get(div_name, {
                "sttb_index": None, "count": 0, 
                "transparency": None, "ethics": None, "privacy": None, "security": None, "inclusion": None
            })
            
            # If there are no data entries yet, count is 0
            if stats["count"] == 0:
                index_display = "N/A"
                level_str = "Tiada Data" if lang == "Bahasa Melayu" else "No Data"
                marker_color = "#7f8c8d"  # Neutral Gray
                
                t_val = "N/A"
                e_val = "N/A"
                p_val = "N/A"
                s_val = "N/A"
                i_val = "N/A"
            else:
                index_val = stats["sttb_index"]
                index_display = f"{index_val:.2f}"
                eval_info = survey.get_trust_level(index_val)
                marker_color = eval_info["color"]
                
                bm_levels = {
                    "High Trust": "Kepercayaan Tinggi",
                    "Moderate Trust": "Kepercayaan Sederhana",
                    "Low Trust": "Kepercayaan Rendah",
                    "Very Low Trust": "Kepercayaan Sangat Rendah"
                }
                level_str = bm_levels.get(eval_info["level"], eval_info["level"]) if lang == "Bahasa Melayu" else eval_info["level"]
                
                t_val = f"{stats['transparency']:.1f}"
                e_val = f"{stats['ethics']:.1f}"
                p_val = f"{stats['privacy']:.1f}"
                s_val = f"{stats['security']:.1f}"
                i_val = f"{stats['inclusion']:.1f}"
            
            if lang == "Bahasa Melayu":
                popup_html = f"""
                <div style="font-family: 'Outfit', sans-serif; width: 220px; color: #2c3e50;">
                    <h4 style="margin: 0 0 5px 0; color: #2980b9;">Bahagian {div_name}</h4>
                    <div style="font-size: 1.3rem; font-weight: 800; color: {marker_color}; margin-bottom: 5px;">
                        Indeks STTB: {index_display}
                    </div>
                    <div style="font-size: 0.85rem; font-weight: bold; margin-bottom: 10px;">
                        Tahap Kepercayaan: {level_str} <br>
                        Saiz Sampel (N): {stats['count']}
                    </div>
                    <hr style="border: 0; border-top: 1px solid #ddd; margin: 8px 0;">
                    <table style="width: 100%; font-size: 0.8rem;">
                        <tr><td>Ketelusan:</td><td style="text-align:right; font-weight:bold;">{t_val}</td></tr>
                        <tr><td>Etika:</td><td style="text-align:right; font-weight:bold;">{e_val}</td></tr>
                        <tr><td>Privasi:</td><td style="text-align:right; font-weight:bold;">{p_val}</td></tr>
                        <tr><td>Keselamatan:</td><td style="text-align:right; font-weight:bold;">{s_val}</td></tr>
                        <tr><td>Inklusi:</td><td style="text-align:right; font-weight:bold;">{i_val}</td></tr>
                    </table>
                </div>
                """
            else:
                popup_html = f"""
                <div style="font-family: 'Outfit', sans-serif; width: 220px; color: #2c3e50;">
                    <h4 style="margin: 0 0 5px 0; color: #2980b9;">{div_name} Division</h4>
                    <div style="font-size: 1.3rem; font-weight: 800; color: {marker_color}; margin-bottom: 5px;">
                        STTB Index: {index_display}
                    </div>
                    <div style="font-size: 0.85rem; font-weight: bold; margin-bottom: 10px;">
                        Trust Level: {level_str} <br>
                        Sample Size (N): {stats['count']}
                    </div>
                    <hr style="border: 0; border-top: 1px solid #ddd; margin: 8px 0;">
                    <table style="width: 100%; font-size: 0.8rem;">
                        <tr><td>Transparency:</td><td style="text-align:right; font-weight:bold;">{t_val}</td></tr>
                        <tr><td>Ethics:</td><td style="text-align:right; font-weight:bold;">{e_val}</td></tr>
                        <tr><td>Privacy:</td><td style="text-align:right; font-weight:bold;">{p_val}</td></tr>
                        <tr><td>Security:</td><td style="text-align:right; font-weight:bold;">{s_val}</td></tr>
                        <tr><td>Inclusion:</td><td style="text-align:right; font-weight:bold;">{i_val}</td></tr>
                    </table>
                </div>
                """
            
            folium.CircleMarker(
                location=[coords["lat"], coords["lon"]],
                radius=12 + (stats["count"] * 0.1),
                popup=folium.Popup(popup_html, max_width=250),
                color=marker_color,
                fill=True,
                fill_color=marker_color,
                fill_opacity=0.6,
                tooltip=f"{div_name}: Index = {index_display}"
            ).add_to(m)
            
        st_folium(m, width=1200, height=600, key="dashboard_trust_map")
        
        # Collapsible Database Administration Panel (Admin Only)
        st.markdown("<br>", unsafe_allow_html=True)
        admin_title = "Tetapan Sistem & Pentadbiran (UTS Admin Sahaja)" if lang == "Bahasa Melayu" else "System Settings & Administration (UTS Admin Only)"
        with st.expander(admin_title):
            if lang == "Bahasa Melayu":
                st.markdown("""
                <div style="padding: 10px; border-left: 3px solid #DA291C;">
                    <h4 style="color:#DA291C; margin: 0 0 10px 0;">Panel Pentadbiran Pangkalan Data</h4>
                    <p style="font-size:0.85rem; color:#bdc3c7; margin:0 0 15px 0;">
                        Untuk memindahkan kerangka kerja ini daripada fasa penilaian rintisan kepada pengumpulan data akademik dunia sebenar, anda boleh memadamkan semua rekod olok-olok pra-pemuatan di sini. Ini akan mengosongkan pangkalan data sepenuhnya kepada sifar penyerahan dan menghentikan enjin pemuatan automatik secara kekal.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="padding: 10px; border-left: 3px solid #DA291C;">
                    <h4 style="color:#DA291C; margin: 0 0 10px 0;">Database Administration Panel</h4>
                    <p style="font-size:0.85rem; color:#bdc3c7; margin:0 0 15px 0;">
                        To transition this framework from the pilot evaluation phase to real-world academic data collection, you can purge all pre-seeded mock records here. This will clear the database entirely to a 0-submission slate and permanently stop the automated seed engine.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            purge_btn_lbl = "Padam Semua Rekod Pangkalan Data Rintisan" if lang == "Bahasa Melayu" else "Purge All Pilot Database Records"
            if st.button(purge_btn_lbl, type="secondary", use_container_width=True, key="admin_purge_btn"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM respondents")
                cursor.execute("DELETE FROM responses")
                cursor.execute("DELETE FROM computed_scores")
                cursor.execute("CREATE TABLE IF NOT EXISTS system_config (key TEXT UNIQUE, val TEXT)")
                cursor.execute("INSERT OR REPLACE INTO system_config (key, val) VALUES ('seeded', 'false')")
                conn.commit()
                conn.close()
                succ_purge = "Pangkalan data berjaya dipadamkan kepada keadaan bersih! Mengarah semula..." if lang == "Bahasa Melayu" else "Database successfully purged to a clean state! Redirecting..."
                st.success(succ_purge)
                st.session_state["page"] = "Welcome & Overview"
                st.rerun()


# ---------------------------------------------------------
# PAGE 5: HELP & CIVIC FEEDBACK FORM
# ---------------------------------------------------------
elif page == "Help / Feedback":
    if lang == "Bahasa Melayu":
        st.markdown('<div class="glass-header"><h1>Meja Bantuan & Maklum Balas Sivik</h1><div class="subtitle">Pusat Aduan & Repositori Maklum Balas Tanpa Nama</div></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <h3>Maklum Balas Sokongan & Penyelarasan</h3>
            <p>Untuk menyokong penambahbaikan kualiti yang berterusan dan mematuhi piawaian audit projek tahun akhir UTS, pelajar UTS, pentadbir, dan orang awam boleh mengemukakan pertanyaan, laporan pepijat teknikal, atau cadangan penyelarasan di sini. <b>Semua maklum balas adalah tanpa nama dan dikatalogkan dengan selamat untuk semakan.</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-header"><h1>Help Desk & Civic Feedback</h1><div class="subtitle">Anonymized Complaint & Feedback Repository</div></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <h3>Support & Alignment Feedback</h3>
            <p>To support continuous quality improvements and comply with final year project audit standards, UTS students, administrators, and the general public can submit inquiries, technical bug reports, or alignment suggestions here. <b>All feedback is anonymous and securely cataloged for review.</b></p>
        </div>
        """, unsafe_allow_html=True)
        
    # 2-column layout for Form
    f_col1, f_col2 = st.columns(2)
    
    with f_col1:
        step1_title = "Langkah 1: Peranan Pihak Berkepentingan" if lang == "Bahasa Melayu" else "Step 1: Stakeholder Role"
        st.markdown(f"<h3 style='color:#ffd700; margin-bottom:15px;'>{step1_title}</h3>", unsafe_allow_html=True)
        
        role_lbl = "Saya menyerahkan sebagai:" if lang == "Bahasa Melayu" else "I am submitting as a:"
        role_options_en = ["General Public Respondent", "UTS Student", "UTS Academic Faculty", "System Auditor / Admin"]
        role_options_bm = ["Responden Awam", "Pelajar UTS", "Fakulti Akademik UTS", "Auditor Sistem / Pentadbir"]
        user_role_selected = st.selectbox(role_lbl, role_options_bm if lang == "Bahasa Melayu" else role_options_en, key="feedback_role")
        role_mapping = dict(zip(role_options_bm, role_options_en))
        user_role = role_mapping.get(user_role_selected, user_role_selected)
        
        cat_lbl = "Kategori Maklum Balas:" if lang == "Bahasa Melayu" else "Feedback Category:"
        cat_options_en = ["Technical Bug / Interface Error", "Data Validation / Accuracy Inquiry", "Academic Theoretical Alignment (Scott's Pillars)", "General Feature Suggestion"]
        cat_options_bm = ["Pepijat Teknikal / Ralat Antara Muka", "Pertanyaan Pengesahan Data / Ketepatan", "Penyelarasan Teori Akademik (Tonggak Scott)", "Cadangan Ciri Umum"]
        category_selected = st.selectbox(cat_lbl, cat_options_bm if lang == "Bahasa Melayu" else cat_options_en, key="feedback_category")
        cat_mapping = dict(zip(cat_options_bm, cat_options_en))
        category = cat_mapping.get(category_selected, category_selected)
        
        sat_lbl = "Penarafan Pengalaman Sistem Keseluruhan (1 = Lemah, 5 = Premium):" if lang == "Bahasa Melayu" else "Overall System Experience Rating (1 = Poor, 5 = Premium):"
        satisfaction = st.slider(sat_lbl, 1, 5, 5, key="feedback_rating")

    with f_col2:
        step2_title = "Langkah 2: Butiran Mesej" if lang == "Bahasa Melayu" else "Step 2: Message Details"
        st.markdown(f"<h3 style='color:#ffd700; margin-bottom:15px;'>{step2_title}</h3>", unsafe_allow_html=True)
        
        sub_lbl = "Subjek / Ringkasan Maklum Balas:" if lang == "Bahasa Melayu" else "Feedback Subject / Summary:"
        sub_holder = "cth. Cadangan Penyelarasan Navigasi" if lang == "Bahasa Melayu" else "e.g. Navigation Alignment Suggestion"
        subject = st.text_input(sub_lbl, placeholder=sub_holder, key="feedback_subject")
        
        desc_lbl = "Penerangan Terperinci / Aduan:" if lang == "Bahasa Melayu" else "Detailed Description / Complaint:"
        desc_holder = "Sila berikan butiran terperinci supaya pasukan pembangunan boleh menangani maklum balas anda." if lang == "Bahasa Melayu" else "Please provide exact details so the development team can address your feedback."
        description = st.text_area(desc_lbl, placeholder=desc_holder, key="feedback_desc")
        
    st.markdown("<br>", unsafe_allow_html=True)
    submit_feed_lbl = "Hantar Maklum Balas Sistem Tanpa Nama" if lang == "Bahasa Melayu" else "Submit Anonymous System Feedback"
    if st.button(submit_feed_lbl, type="primary", use_container_width=True, key="submit_feedback_btn"):
        if not subject.strip() or not description.strip():
            err_msg = "Sila isi kedua-dua ruangan Subjek dan Penerangan sebelum menyerahkan." if lang == "Bahasa Melayu" else "Please fill in both the Subject and Description fields before submitting."
            st.error(err_msg)
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO system_feedback (user_role, category, subject, description, satisfaction)
            VALUES (?, ?, ?, ?, ?)
            """, (user_role, category, subject, description, satisfaction))
            conn.commit()
            conn.close()
            succ_msg = "Maklum balas tanpa nama anda telah selamat dihantar! Terima kasih kerana membantu kami menambah baik Barometer Kepercayaan Teknologi Sarawak." if lang == "Bahasa Melayu" else "Your anonymous feedback has been safely submitted! Thank you for helping us improve the Sarawak Tech-Trust Barometer."
            st.success(succ_msg)
            st.balloons()


# ---------------------------------------------------------
# PAGE 6: ADMIN PANEL & CIVIC AUDITING PORTAL
# ---------------------------------------------------------
elif page == "Admin Panel":
    if lang == "Bahasa Melayu":
        st.markdown('<div class="glass-header"><h1>Portal Audit Pentadbir STTB</h1><div class="subtitle">Akses Selamat & Pengurusan Maklum Balas Pelajar UTS & Orang Awam</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-header"><h1>STTB Admin Audit Portal</h1><div class="subtitle">Secure Access & Management of UTS Student & Public Feedback</div></div>', unsafe_allow_html=True)

    # Password Gate
    pwd_placeholder = "Masukkan kata laluan pentadbiran..." if lang == "Bahasa Melayu" else "Enter administrative password..."
    pwd_lbl = "Pengesahan Akses Pentadbir:" if lang == "Bahasa Melayu" else "Administrator Access Verification:"
    
    col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
    with col_p2:
        admin_pwd = st.text_input(pwd_lbl, type="password", placeholder=pwd_placeholder, key="admin_pwd_gate")
        
    if admin_pwd != "uts2026" and admin_pwd != "admin123":
        if admin_pwd != "":
            st.error("Kata laluan tidak sah! Akses ditolak." if lang == "Bahasa Melayu" else "Invalid password! Access denied.")
        else:
            st.warning("Sila masukkan kata laluan untuk mengakses portal aduan & audit." if lang == "Bahasa Melayu" else "Please enter the password to access the complaints & auditing portal.")
            
        # Display academic information card in the gate page
        if lang == "Bahasa Melayu":
            st.markdown("""
            <div class="glass-card" style="text-align: center; border-color: rgba(218, 41, 28, 0.4);">
                <h4 style="color: #DA291C;">Akses Terperingkat Maklum Balas Civik</h4>
                <p style="font-size: 0.9rem;">Halaman ini bertujuan untuk digunakan oleh ahli fakulti UTS, penyelidik universiti, dan auditor ekonomi digital Sarawak bagi memeriksa aduan teknikal sistem, pengesahan statistik data, dan cadangan penyelarasan kerangka sosiologi.</p>
                <p style="font-size: 0.8rem; color: #888888;">Petunjuk: Gunakan kata laluan akademik <b>uts2026</b> untuk log masuk.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align: center; border-color: rgba(218, 41, 28, 0.4);">
                <h4 style="color: #DA291C;">Classified Civic Feedback Access</h4>
                <p style="font-size: 0.9rem;">This page is intended for UTS academic faculty members, university researchers, and Sarawak digital economy auditors to inspect technical system complaints, data accuracy verifications, and theoretical framework alignments.</p>
                <p style="font-size: 0.8rem; color: #888888;">Tip: Use the academic password <b>uts2026</b> to log in.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # User is authenticated!
        st.success("Akses Dibenarkan." if lang == "Bahasa Melayu" else "Access Granted.")
        
        # Lock Auditing Portal / Logout Button (Dynamic Security)
        l_col1, l_col2 = st.columns([4, 1])
        with l_col2:
            lock_label = "Kunci Portal & Keluar" if lang == "Bahasa Melayu" else "Lock Portal & Logout"
            if st.button(lock_label, type="secondary", use_container_width=True, key="lock_portal_btn"):
                st.session_state["admin_mode"] = False
                st.session_state["page"] = "Welcome & Overview"
                st.query_params.clear()
                st.rerun()
                
        # Initialize Admin Tabs Workspace
        admin_tab_1, admin_tab_2, admin_tab_3 = st.tabs([
            "✉️ Maklum Balas Civik / Civic Feedback" if lang == "Bahasa Melayu" else "✉️ Civic Feedback & Complaints",
            "📊 Data Respon Tinjauan / Survey Responses" if lang == "Bahasa Melayu" else "📊 Survey Responses Manager",
            "🛡️ Log Audit Pentadbir / Admin Audit Logs" if lang == "Bahasa Melayu" else "🛡️ Admin Activity & Audit Logs"
        ])
        
        # ---------------------------------------------------------
        # TAB 1: CIVIC FEEDBACK WORKSPACE
        # ---------------------------------------------------------
        with admin_tab_1:
            # Load feedback data
            conn = get_db_connection()
            df_feed = pd.read_sql_query("SELECT * FROM system_feedback ORDER BY submitted_at DESC", conn)
            conn.close()
            
            total_feedback = len(df_feed)
            
            if total_feedback == 0:
                st.info("Tiada maklum balas sistem yang telah dikemukakan lagi." if lang == "Bahasa Melayu" else "No system feedback has been submitted yet.")
            else:
                # 1. KPI Panel Cards
                avg_sat = df_feed["satisfaction"].mean()
                bugs_count = len(df_feed[df_feed["category"].str.contains("Technical|Pepijat")])
                academic_count = len(df_feed[df_feed["category"].str.contains("Academic|Teori|Tonggak")])
                
                kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
                
                with kpi_c1:
                    title_lbl = "Jumlah Maklum Balas" if lang == "Bahasa Melayu" else "Total Feedback Entries"
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center; padding: 15px;">
                        <div class="metric-label">{title_lbl}</div>
                        <div class="metric-value" style="font-size: 2.2rem;">{total_feedback}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with kpi_c2:
                    title_lbl = "Purata Kepuasan" if lang == "Bahasa Melayu" else "Avg System Rating"
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center; padding: 15px;">
                        <div class="metric-label">{title_lbl}</div>
                        <div class="metric-value" style="font-size: 2.2rem; color: #ffd700;">{avg_sat:.2f}/5.00</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with kpi_c3:
                    title_lbl = "Laporan Pepijat/Ralat" if lang == "Bahasa Melayu" else "Bug Reports"
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center; padding: 15px;">
                        <div class="metric-label">{title_lbl}</div>
                        <div class="metric-value" style="font-size: 2.2rem; color: #ff4d4d;">{bugs_count}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with kpi_c4:
                    title_lbl = "Penyelarasan Akademik" if lang == "Bahasa Melayu" else "Academic Inquiries"
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center; padding: 15px;">
                        <div class="metric-label">{title_lbl}</div>
                        <div class="metric-value" style="font-size: 2.2rem; color: #4da6ff;">{academic_count}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                st.markdown("<br>", unsafe_allow_html=True)
                
                # 2. Main Double-Column Layout
                d_col1, d_col2 = st.columns([3, 2])
                
                with d_col1:
                    st.subheader("Carian & Tapis Senarai Maklum Balas" if lang == "Bahasa Melayu" else "Search & Filter Feedback Submissions")
                    
                    # Filters
                    f_role_lbl = "Tapis Peranan:" if lang == "Bahasa Melayu" else "Filter Role:"
                    f_cat_lbl = "Tapis Kategori:" if lang == "Bahasa Melayu" else "Filter Category:"
                    
                    roles_available = sorted(list(df_feed["user_role"].unique()))
                    cats_available = sorted(list(df_feed["category"].unique()))
                    
                    sf_col1, sf_col2 = st.columns(2)
                    with sf_col1:
                        selected_roles = st.multiselect(f_role_lbl, roles_available, default=roles_available)
                    with sf_col2:
                        selected_cats = st.multiselect(f_cat_lbl, cats_available, default=cats_available)
                        
                    # Apply filter
                    filtered_df = df_feed[
                        df_feed["user_role"].isin(selected_roles) & 
                        df_feed["category"].isin(selected_cats)
                    ]
                    
                    # Display DataFrame
                    st.markdown(f"<div style='font-size: 0.9rem; margin-bottom: 10px; color:#888;'>Hasil carian: {len(filtered_df)} entri</div>", unsafe_allow_html=True)
                    
                    display_cols = ["id", "user_role", "category", "subject", "satisfaction", "submitted_at"]
                    renamed_df = filtered_df[display_cols].copy()
                    if lang == "Bahasa Melayu":
                        renamed_df.columns = ["ID", "Peranan", "Kategori", "Subjek Mesej", "Kepuasan", "Tarikh Dihantar"]
                    else:
                        renamed_df.columns = ["ID", "Stakeholder Role", "Feedback Category", "Subject / Summary", "Rating", "Submitted At"]
                        
                    st.dataframe(renamed_df, use_container_width=True, hide_index=True)
                    
                with d_col2:
                    st.subheader("Panel Perincian & Penyelesaian" if lang == "Bahasa Melayu" else "Feedback Detail & Resolution Panel")
                    
                    if len(filtered_df) == 0:
                        st.info("Tiada padanan dijumpai untuk kriteria tapis semasa." if lang == "Bahasa Melayu" else "No matching entries found for current filters.")
                    else:
                        select_lbl = "Pilih ID entri untuk audit perperincian:" if lang == "Bahasa Melayu" else "Select entry ID to audit details:"
                        selected_id = st.selectbox(select_lbl, filtered_df["id"].tolist())
                        
                        # Fetch selected record
                        record = filtered_df[filtered_df["id"] == selected_id].iloc[0]
                        
                        # Display clean card
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 5px solid #FFC72C;">
                            <h4 style="margin: 0 0 5px 0; color: #FFC72C;">{record['subject']}</h4>
                            <div style="font-size: 0.8rem; color: #888888; margin-bottom: 15px;">
                                ID: #{record['id']} | {record['submitted_at']} <br>
                                <b>Peranan:</b> {record['user_role']} <br>
                                <b>Kategori:</b> {record['category']}
                            </div>
                            <p style="font-size: 0.95rem; border-top: 1px solid rgba(255,199,44,0.15); padding-top: 15px;">
                                {record['description']}
                            </p>
                            <div style="margin-top: 15px; font-weight: bold; color: #ffd700;">
                                Skor Penarafan Sistem: {"⭐" * record['satisfaction']} ({record['satisfaction']}/5)
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Delete action
                        res_btn = "Tandakan Selesai & Padam Aduan" if lang == "Bahasa Melayu" else "Mark Resolved & Purge Entry"
                        if st.button(res_btn, type="primary", use_container_width=True, key=f"del_feed_{selected_id}"):
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM system_feedback WHERE id = ?", (int(selected_id),))
                            conn.commit()
                            conn.close()
                            
                            # Log Action
                            log_admin_action(
                                "Delete Feedback", 
                                f"Deleted system feedback entry ID {selected_id} (subject: '{record['subject']}')"
                            )
                            
                            succ_purge = "Aduan berjaya diselesaikan dan dipadamkan daripada pangkalan data!" if lang == "Bahasa Melayu" else "Feedback entry resolved and purged from the database successfully!"
                            st.success(succ_purge)
                            st.rerun()
                            
                # 3. Quick Visual Breakdown Charts
                st.markdown("<br><hr style='border:0; border-top:1px solid rgba(255,255,255,0.15);'><br>", unsafe_allow_html=True)
                st.subheader("Pecahan Statistik Maklum Balas" if lang == "Bahasa Melayu" else "Statistical Feedback Breakdown")
                
                c_chart1, c_chart2 = st.columns(2)
                with c_chart1:
                    # Category counts chart
                    cat_counts = df_feed["category"].value_counts().reset_index()
                    cat_counts.columns = ["Kategori" if lang == "Bahasa Melayu" else "Category", "Jumlah" if lang == "Bahasa Melayu" else "Count"]
                    st.bar_chart(data=cat_counts, x="Kategori" if lang == "Bahasa Melayu" else "Category", y="Jumlah" if lang == "Bahasa Melayu" else "Count", color="#FFC72C")
                    
                with c_chart2:
                    # Satisfaction frequency chart
                    sat_counts = df_feed["satisfaction"].value_counts().reset_index()
                    sat_counts.columns = ["Skor" if lang == "Bahasa Melayu" else "Score", "Jumlah" if lang == "Bahasa Melayu" else "Count"]
                    st.bar_chart(data=sat_counts, x="Skor" if lang == "Bahasa Melayu" else "Score", y="Jumlah" if lang == "Bahasa Melayu" else "Count", color="#DA291C")

            # 4. Database Administration Panel
            st.markdown("<br><hr style='border:0; border-top:1px solid rgba(255,255,255,0.15);'><br>", unsafe_allow_html=True)
            if lang == "Bahasa Melayu":
                st.markdown("""
                <div style="padding: 10px; border-left: 3px solid #DA291C;">
                    <h4 style="color:#DA291C; margin: 0 0 10px 0;">Panel Pentadbiran Pangkalan Data</h4>
                    <p style="font-size:0.85rem; color:#bdc3c7; margin:0 0 15px 0;">
                        Untuk memindahkan kerangka kerja ini daripada fasa penilaian rintisan kepada pengumpulan data akademik dunia sebenar, anda boleh memadamkan semua rekod olok-olok pra-pemuatan di sini. Ini akan mengosongkan pangkalan data sepenuhnya kepada sifar penyerahan dan menghentikan enjin pemuatan automatik secara kekal.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="padding: 10px; border-left: 3px solid #DA291C;">
                    <h4 style="color:#DA291C; margin: 0 0 10px 0;">Database Administration Panel</h4>
                    <p style="font-size:0.85rem; color:#bdc3c7; margin:0 0 15px 0;">
                        To transition this framework from the pilot evaluation phase to real-world academic data collection, you can purge all pre-seeded mock records here. This will clear the database entirely to a 0-submission slate and permanently stop the automated seed engine.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            purge_btn_lbl = "Padam Semua Rekod Pangkalan Data Rintisan" if lang == "Bahasa Melayu" else "Purge All Pilot Database Records"
            if st.button(purge_btn_lbl, type="secondary", use_container_width=True, key="admin_purge_btn"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM respondents")
                cursor.execute("DELETE FROM responses")
                cursor.execute("DELETE FROM computed_scores")
                cursor.execute("CREATE TABLE IF NOT EXISTS system_config (key TEXT UNIQUE, val TEXT)")
                cursor.execute("INSERT OR REPLACE INTO system_config (key, val) VALUES ('seeded', 'false')")
                conn.commit()
                conn.close()
                
                # Log action
                log_admin_action("Purge Database", "Purged all pre-seeded pilot database records and respondents")
                
                succ_purge = "Pangkalan data berjaya dipadamkan kepada keadaan bersih! Mengarah semula..." if lang == "Bahasa Melayu" else "Database successfully purged to a clean state! Redirecting..."
                st.success(succ_purge)
                st.session_state["page"] = "Welcome & Overview"
                st.rerun()

        # ---------------------------------------------------------
        # TAB 2: SURVEY RESPONSES WORKSPACE (Auditing & Deleting & CSV Load)
        # ---------------------------------------------------------
        with admin_tab_2:
            st.subheader("Pengurusan Data Respon Tinjauan" if lang == "Bahasa Melayu" else "Survey Response Data Auditing")
            
            # Load all survey respondents
            conn = get_db_connection()
            df_resp = pd.read_sql_query("""
                SELECT r.id, r.age_group, r.gender, r.occupation, r.district, r.submitted_at, c.sttb_index, c.trust_level
                FROM respondents r
                LEFT JOIN computed_scores c ON r.id = c.respondent_id
                ORDER BY r.id DESC
            """, conn)
            conn.close()
            
            total_resp = len(df_resp)
            st.markdown(f"<div style='font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;'>Jumlah Penyerahan Tinjauan: {total_resp} entri</div>", unsafe_allow_html=True)
            
            if total_resp == 0:
                st.info("Tiada respon tinjauan dalam pangkalan data lagi." if lang == "Bahasa Melayu" else "No survey responses found in the database.")
            else:
                # Layout
                dm_col1, dm_col2 = st.columns([3, 2])
                
                with dm_col1:
                    # Filter Controls
                    st.markdown("#### Carian & Tapis Respon" if lang == "Bahasa Melayu" else "#### Search & Filter Responses")
                    f_col_div, f_col_age = st.columns(2)
                    with f_col_div:
                        districts_avail = ["All"] + sorted(list(df_resp["district"].dropna().unique()))
                        selected_dist = st.selectbox("Tapis Bahagian / District:" if lang == "Bahasa Melayu" else "Filter Sarawak Division:", districts_avail)
                    with f_col_age:
                        ages_avail = ["All"] + sorted(list(df_resp["age_group"].dropna().unique()))
                        selected_age = st.selectbox("Tapis Kumpulan Umur / Age Group:" if lang == "Bahasa Melayu" else "Filter Age Group:", ages_avail)
                        
                    # Apply filter
                    filtered_resp = df_resp.copy()
                    if selected_dist != "All":
                        filtered_resp = filtered_resp[filtered_resp["district"] == selected_dist]
                    if selected_age != "All":
                        filtered_resp = filtered_resp[filtered_resp["age_group"] == selected_age]
                        
                    # Display Dataframe
                    disp_resp_df = filtered_resp.copy()
                    if lang == "Bahasa Melayu":
                        disp_resp_df.columns = ["Responden ID", "Kumpulan Umur", "Jantina", "Pekerjaan", "Bahagian", "Tarikh Hantar", "Indeks STTB", "Tahap Kepercayaan"]
                    else:
                        disp_resp_df.columns = ["Respondent ID", "Age Group", "Gender", "Occupation", "Sarawak Division", "Submitted At", "STTB Index", "Trust Level"]
                        
                    st.dataframe(disp_resp_df, use_container_width=True, hide_index=True)
                    
                with dm_col2:
                    st.markdown("#### Audit & Pemadaman Respon" if lang == "Bahasa Melayu" else "#### Response Auditor & Individual Purge")
                    
                    audit_resp_id = st.selectbox(
                        "Pilih ID Responden untuk diaudit / Select Respondent ID to audit:" if lang == "Bahasa Melayu" else "Select Respondent ID for details & purge:",
                        filtered_resp["id"].tolist()
                    )
                    
                    if audit_resp_id:
                        selected_resp = filtered_resp[filtered_resp["id"] == audit_resp_id].iloc[0]
                        
                        # Load raw answers
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT responses_json FROM survey_responses WHERE respondent_id = ?", (int(audit_resp_id),))
                        row_json = cursor.fetchone()
                        conn.close()
                        
                        # Extract demographics safely to avoid f-string nested key syntax issues
                        resp_id_val = selected_resp['id']
                        resp_date_val = selected_resp['submitted_at']
                        resp_age_val = selected_resp['age_group']
                        resp_gender_val = selected_resp['gender']
                        resp_occ_val = selected_resp['occupation']
                        resp_dist_val = selected_resp['district']
                        resp_sttb_val = float(selected_resp['sttb_index']) if pd.notnull(selected_resp['sttb_index']) else 0.0
                        formatted_sttb_val = f"{resp_sttb_val:.2f}"
                        resp_level_val = selected_resp['trust_level']
                        
                        # Display clean card
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 5px solid #DA291C;">
                            <h4 style="margin: 0 0 5px 0; color: #DA291C;">Responden #{resp_id_val}</h4>
                            <div style="font-size: 0.8rem; color: #888888; margin-bottom: 10px;">
                                <b>Tarikh:</b> {resp_date_val} <br>
                                <b>Kumpulan Umur:</b> {resp_age_val} | <b>Jantina:</b> {resp_gender_val} <br>
                                <b>Pekerjaan:</b> {resp_occ_val} | <b>Bahagian:</b> {resp_dist_val}
                            </div>
                            <div style="font-size: 1rem; font-weight: bold; margin-top: 10px; color:#ffd700;">
                                Skor Indeks STTB: {formatted_sttb_val} ({resp_level_val})
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Expand raw answers json preview
                        if row_json:
                            try:
                                answers_dict = json.loads(row_json[0])
                                with st.expander("Pratonton Jawapan Mentah (Raw Answers)" if lang == "Bahasa Melayu" else "View Raw Answers JSON"):
                                    st.json(answers_dict)
                            except Exception:
                                pass
                                
                        # Delete action
                        del_btn_lbl = f"Padam Data Responden #{audit_resp_id} Secara Kekal" if lang == "Bahasa Melayu" else f"Permanently Delete Respondent #{audit_resp_id} Data"
                        
                        if st.button(del_btn_lbl, type="primary", use_container_width=True, key=f"del_resp_{audit_resp_id}"):
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM respondents WHERE id = ?", (int(audit_resp_id),))
                            cursor.execute("DELETE FROM survey_responses WHERE respondent_id = ?", (int(audit_resp_id),))
                            cursor.execute("DELETE FROM computed_scores WHERE respondent_id = ?", (int(audit_resp_id),))
                            conn.commit()
                            conn.close()
                            
                            # Log action
                            log_admin_action(
                                "Delete Respondent Data", 
                                f"Deleted individual respondent ID {audit_resp_id} (demographics: {selected_resp['age_group']}, {selected_resp['gender']}, {selected_resp['occupation']}, {selected_resp['district']})"
                            )
                            
                            succ_del = f"Responden #{audit_resp_id} berjaya dipadamkan daripada pangkalan data!" if lang == "Bahasa Melayu" else f"Respondent #{audit_resp_id} successfully deleted from the database!"
                            st.success(succ_del)
                            st.rerun()
                            
            # 4. External Data Import Panel (Google Form CSV Loader)
            st.markdown("<br><hr style='border:0; border-top:1px solid rgba(255,255,255,0.15);'><br>", unsafe_allow_html=True)
            csv_import_title = "Pemuat Data Tinjauan Luaran (.csv)" if lang == "Bahasa Melayu" else "External CSV Survey Data Loader (.csv)"
            st.subheader(csv_import_title)
            
            if lang == "Bahasa Melayu":
                st.markdown("""
                <div class="glass-card" style="border-left: 3px solid #FFC72C;">
                    <p><b>Muat Naik Data Tinjauan Google Form:</b> Jika anda mengumpul data menggunakan Google Form luar, anda boleh mengimport entri di sini. Pemuat menyokong pemetaan lajur automatik atau manual untuk disesuaikan dengan soalan mini-tinjauan anda.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="glass-card" style="border-left: 3px solid #FFC72C;">
                    <p><b>Upload Google Form Survey Data:</b> If you collected responses via an external Google Form, you can import them here. The loader supports automatic detection or manual column mapping for the 15 mini-survey questions.</p>
                </div>
                """, unsafe_allow_html=True)
                
            uploaded_file = st.file_uploader(
                "Pilih fail CSV tinjauan..." if lang == "Bahasa Melayu" else "Choose survey CSV file...", 
                type=["csv"],
                key="survey_csv_uploader"
            )
            
            if uploaded_file is not None:
                try:
                    import pandas as pd
                    import io
                    import json
                    import re
                    
                    df_upload = pd.read_csv(uploaded_file)
                    st.success("Fail berjaya dimuat naik!" if lang == "Bahasa Melayu" else "File uploaded successfully!")
                    
                    # Display preview
                    st.write("Pratonton Data (5 Baris Pertama):" if lang == "Bahasa Melayu" else "Data Preview (First 5 Rows):")
                    st.dataframe(df_upload.head(), use_container_width=True)
                    
                    # Mapping Column Options
                    all_columns = df_upload.columns.tolist()
                    
                    # Auto-detect defaults
                    def auto_detect(keywords, default):
                        for col in all_columns:
                            col_l = col.lower()
                            if any(k in col_l for k in keywords):
                                return col
                        return default
                        
                    age_col_detected = auto_detect(["age", "umur", "kumpulan"], all_columns[0] if all_columns else None)
                    gender_col_detected = auto_detect(["gender", "jantina", "sex"], all_columns[1] if len(all_columns) > 1 else None)
                    occ_col_detected = auto_detect(["occup", "pekerj", "role"], all_columns[2] if len(all_columns) > 2 else None)
                    dist_col_detected = auto_detect(["dist", "divis", "bahag", "kawasa"], all_columns[3] if len(all_columns) > 3 else None)
                    
                    # Show mapping controls
                    st.markdown("---")
                    st.markdown("#### Pemetaan Lajur Demografi" if lang == "Bahasa Melayu" else "#### Demographic Column Mapping")
                    
                    col_dm1, col_dm2, col_dm3, col_dm4 = st.columns(4)
                    with col_dm1:
                        age_col = st.selectbox("Umur / Age Group:" if lang == "Bahasa Melayu" else "Age Group:", all_columns, index=all_columns.index(age_col_detected) if age_col_detected in all_columns else 0)
                    with col_dm2:
                        gender_col = st.selectbox("Jantina / Gender:" if lang == "Bahasa Melayu" else "Gender:", all_columns, index=all_columns.index(gender_col_detected) if gender_col_detected in all_columns else 0)
                    with col_dm3:
                        occ_col = st.selectbox("Pekerjaan / Occupation:" if lang == "Bahasa Melayu" else "Occupation:", all_columns, index=all_columns.index(occ_col_detected) if occ_col_detected in all_columns else 0)
                    with col_dm4:
                        dist_col = st.selectbox("Bahagian / Division:" if lang == "Bahasa Melayu" else "Division:", all_columns, index=all_columns.index(dist_col_detected) if dist_col_detected in all_columns else 0)
                        
                    st.markdown("---")
                    st.markdown("#### Pemetaan 15 Soalan Mini-Tinjauan" if lang == "Bahasa Melayu" else "#### 15 Mini-Survey Questions Mapping")
                    
                    mini_q_codes = [
                        "TA1.2", "TA2.2", "TA3.3",  # P1
                        "ER1.3", "ER2.1", "ER3.1",  # P2
                        "PC1.2", "PC2.1", "PC3.1",  # P3
                        "SR1.1", "SR2.2", "SR3.4",  # P4
                        "DI1.1", "DI2.3", "DI3.3"   # P5
                    ]
                    
                    mapped_q_cols = {}
                    
                    q_hints = {
                        "TA1.2": "P1-Ketelusan (Information Transparency)",
                        "TA2.2": "P1-Kebolehcapaian (Accessibility of Platforms)",
                        "TA3.3": "P1-Sidq (Truthfulness of Channels)",
                        "ER1.3": "P2-Algorithmic Bias (Bias Algoritma)",
                        "ER2.1": "P2-Accountability (Kewalihan/Stewardship)",
                        "ER3.1": "P2-Amanah (Trustworthiness of Intent)",
                        "PC1.2": "P3-Privacy Resignation (Kepasrahan Privasi)",
                        "PC2.1": "P3-Tajassus (Unauthorized Surveillance)",
                        "PC3.1": "P3-Haya (Identity Theft Protection)",
                        "SR1.1": "P4-System Vulnerability (Kerapuhan Sistem)",
                        "SR2.2": "P4-Service Disruption (Gangguan Perkhidmatan)",
                        "SR3.4": "P4-Itqan (Software Integration Integrity)",
                        "DI1.1": "P5-Geographic Coverage (Liputan Geografi)",
                        "DI2.3": "P5-Digital Literacy (Sokongan Literasi)",
                        "DI3.3": "P5-Adl (Inclusivity for Marginalized)"
                    }
                    
                    st.info("Penyelaras lajur automatik telah dijalankan berdasarkan nama soalan." if lang == "Bahasa Melayu" else "Automated column mapping performed based on question codes/texts.")
                    
                    q_cols_layout = st.columns(3)
                    
                    for idx, q_code in enumerate(mini_q_codes):
                        col_idx = idx % 3
                        q_detected = None
                        for col in all_columns:
                            if q_code.lower() in col.lower() or f"q{idx+1}" in col.lower():
                                q_detected = col
                                break
                        if not q_detected and len(all_columns) > 4 + idx:
                            q_detected = all_columns[4 + idx]
                            
                        with q_cols_layout[col_idx]:
                            mapped_q_cols[q_code] = st.selectbox(
                                f"{q_code} - {q_hints[q_code]}:", 
                                all_columns, 
                                index=all_columns.index(q_detected) if q_detected in all_columns else (4 + idx if 4 + idx < len(all_columns) else 0),
                                key=f"csv_map_{q_code}"
                            )
                            
                    st.markdown("---")
                    import_btn_lbl = f"Import {len(df_upload)} Entri Tinjauan ke Pangkalan Data" if lang == "Bahasa Melayu" else f"Import {len(df_upload)} Survey Entries into Database"
                    
                    if st.button(import_btn_lbl, type="primary", use_container_width=True, key="process_csv_import"):
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        
                        success_count = 0
                        error_count = 0
                        
                        for idx_row, row in df_upload.iterrows():
                            try:
                                raw_age = str(row[age_col]).strip()
                                raw_gender = str(row[gender_col]).strip()
                                raw_occ = str(row[occ_col]).strip()
                                raw_dist = str(row[dist_col]).strip()
                                
                                age_val = "18-24"
                                if "25" in raw_age or "30" in raw_age:
                                    age_val = "25-34"
                                elif "35" in raw_age or "40" in raw_age:
                                    age_val = "35-44"
                                elif "45" in raw_age or "50" in raw_age:
                                    age_val = "45-54"
                                elif "55" in raw_age or "60" in raw_age:
                                    age_val = "55-64"
                                elif "65" in raw_age or "+" in raw_age:
                                    age_val = "65+"
                                    
                                gender_val = "Male"
                                if "fem" in raw_gender.lower() or "peremp" in raw_gender.lower() or "wita" in raw_gender.lower():
                                    gender_val = "Female"
                                    
                                occ_val = "Student"
                                occ_lower = raw_occ.lower()
                                if "civil" in occ_lower or "kerajaan" in occ_lower or "awam" in occ_lower:
                                    occ_val = "Civil Servant"
                                elif "swasta" in occ_lower or "private" in occ_lower or "corpor" in occ_lower:
                                    occ_val = "Private Sector"
                                elif "self" in occ_lower or "sendiri" in occ_lower or "freelance" in occ_lower:
                                    occ_val = "Self-Employed"
                                elif "retired" in occ_lower or "pesara" in occ_lower:
                                    occ_val = "Retired"
                                elif "unemploy" in occ_lower or "tidak bekerja" in occ_lower or "penganggur" in occ_lower:
                                    occ_val = "Unemployed"
                                    
                                dist_val = "Others"
                                for d_name in SARAWAK_DIVISIONS.keys():
                                    if d_name.lower() in raw_dist.lower():
                                        dist_val = d_name
                                        break
                                        
                                mini_answers = {}
                                for q_code, csv_col in mapped_q_cols.items():
                                    raw_val = row[csv_col]
                                    try:
                                        if isinstance(raw_val, str):
                                            digits = re.findall(r'\d', raw_val)
                                            if digits:
                                                val = int(digits[0])
                                            else:
                                                val_l = raw_val.lower()
                                                if "strongly disagree" in val_l or "sangat tidak" in val_l:
                                                    val = 1
                                                elif "strongly agree" in val_l or "sangat setuju" in val_l:
                                                    val = 5
                                                elif "disagree" in val_l or "tidak setuju" in val_l:
                                                    val = 2
                                                elif "agree" in val_l or "setuju" in val_l:
                                                    val = 4
                                                else:
                                                    val = 3
                                        else:
                                            val = int(raw_val)
                                            
                                        val = max(1, min(5, val))
                                    except Exception:
                                        val = 3
                                    mini_answers[q_code] = val
                                    
                                survey_answers = {}
                                variables_featured = [
                                    "TA1.2", "TA2.2", "TA3.3",
                                    "ER1.3", "ER2.1", "ER3.1",
                                    "PC1.2", "PC2.1", "PC3.1",
                                    "SR1.1", "SR2.2", "SR3.4",
                                    "DI1.1", "DI2.3", "DI3.3"
                                ]
                                for q in survey.QUESTIONS:
                                    q_code = q["code"]
                                    if q_code in mini_answers:
                                        survey_answers[q_code] = mini_answers[q_code]
                                    else:
                                        rep_code = [c for c in variables_featured if c.startswith(q_code[:2])][0]
                                        survey_answers[q_code] = mini_answers[rep_code]
                                        
                                cursor.execute("""
                                INSERT INTO respondents (age_group, gender, occupation, district)
                                VALUES (?, ?, ?, ?)
                                """, (age_val, gender_val, occ_val, dist_val))
                                resp_id = cursor.lastrowid
                                
                                results = survey.calculate_sttb_index(survey_answers)
                                
                                cursor.execute("""
                                INSERT INTO survey_responses (respondent_id, responses_json)
                                VALUES (?, ?)
                                """, (resp_id, json.dumps(survey_answers)))
                                
                                cursor.execute("""
                                INSERT INTO computed_scores (
                                    respondent_id, ps1_transparency, ps2_ethics, ps3_privacy, ps4_security, ps5_inclusion, sttb_index, trust_level
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    resp_id,
                                    results["pillar_scores"]["P1"],
                                    results["pillar_scores"]["P2"],
                                    results["pillar_scores"]["P3"],
                                    results["pillar_scores"]["P4"],
                                    results["pillar_scores"]["P5"],
                                    results["sttb_index"],
                                    results["trust_evaluation"]["level"]
                                ))
                                success_count += 1
                            except Exception as e:
                                error_count += 1
                                continue
                                
                        conn.commit()
                        conn.close()
                        
                        # Log Action
                        log_admin_action(
                            "CSV Import", 
                            f"Imported {success_count} survey responses from CSV file (errors: {error_count})"
                        )
                        
                        st.success(
                            f"Proses import CSV selesai! {success_count} rekod berjaya diimport. {error_count} ralat dikesan." 
                            if lang == "Bahasa Melayu" else 
                            f"CSV import completed! {success_count} records successfully imported. {error_count} errors encountered."
                        )
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Gagal memproses fail CSV: {str(e)}" if lang == "Bahasa Melayu" else f"Failed to process CSV file: {str(e)}")

        # ---------------------------------------------------------
        # TAB 3: ADMIN ACTIVITY & AUDIT LOGS Trail Viewer
        # ---------------------------------------------------------
        with admin_tab_3:
            st.subheader("Log Audit & Aktiviti Pentadbiran" if lang == "Bahasa Melayu" else "Administrative Activity & Audit Trail")
            
            st.markdown(
                "<p style='font-size:0.9rem; color:#bdc3c7;'>Sebagai sebahagian daripada keperluan pematuhan audit UTS, semua tindakan pentadbir dipantau dan disimpan secara kekal dalam log sejarah ini untuk rujukan masa hadapan.</p>"
                if lang == "Bahasa Melayu" else
                "<p style='font-size:0.9rem; color:#bdc3c7;'>As part of UTS research audit compliance requirements, all administrative actions are securely tracked and logged below for historical validation and activity monitoring.</p>",
                unsafe_allow_html=True
            )
            
            # Load Audit Logs
            conn = get_db_connection()
            df_audit = pd.read_sql_query("SELECT id, action_type, details, timestamp FROM admin_audit_logs ORDER BY timestamp DESC", conn)
            conn.close()
            
            total_actions = len(df_audit)
            st.markdown(f"<div style='font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;'>Jumlah Rekod Aktiviti Pentadbiran: {total_actions} tindakan</div>", unsafe_allow_html=True)
            
            if total_actions == 0:
                st.info("Tiada rekod aktiviti pentadbiran yang didokumenkan lagi." if lang == "Bahasa Melayu" else "No administrative activities recorded in the system yet.")
            else:
                # Add action type filter
                action_types_avail = ["All"] + sorted(list(df_audit["action_type"].unique()))
                selected_action_type = st.selectbox(
                    "Tapis Tindakan / Filter Action Type:" if lang == "Bahasa Melayu" else "Filter by Activity Type:",
                    action_types_avail
                )
                
                filtered_audit = df_audit.copy()
                if selected_action_type != "All":
                    filtered_audit = filtered_audit[filtered_audit["action_type"] == selected_action_type]
                    
                # Format DF
                disp_audit_df = filtered_audit.copy()
                if lang == "Bahasa Melayu":
                    disp_audit_df.columns = ["Log ID", "Jenis Tindakan", "Butiran Terperinci", "Masa Kejadian"]
                else:
                    disp_audit_df.columns = ["Log ID", "Action Type", "Detailed Summary", "Timestamp"]
                    
                st.dataframe(disp_audit_df, use_container_width=True, hide_index=True)
                
                # Provide CSV Download compliance button
                csv_data = filtered_audit.to_csv(index=False).encode('utf-8')
                dl_lbl = "Muat Turun Log Audit (.csv)" if lang == "Bahasa Melayu" else "Download Official Audit Log (.csv)"
                st.download_button(
                    label=dl_lbl,
                    data=csv_data,
                    file_name="sttb_admin_audit_logs.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_audit_logs_btn"
                )


# ---------------------------------------------------------
# 5. PERMANENT CENTRALIZED PAGE FOOTER
# ---------------------------------------------------------
st.markdown("---")
footer_text = "Barometer Kepercayaan Teknologi Sarawak © 2026." if lang == "Bahasa Melayu" else "Sarawak Tech-Trust Barometer © 2026."
st.markdown(f"<div style='text-align: center; color: #888888; font-size: 0.85rem; padding: 25px 0 10px 0;'>{footer_text}</div>", unsafe_allow_html=True)

