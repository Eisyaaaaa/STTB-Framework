import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import sqlite3
from datetime import datetime, timedelta
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

if st.session_state["theme_mode"] == "Dark Mode":
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,600;1,400&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #070708 0%, #111115 50%, #180909 100%);
            color: #f5f6f9;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #070708 0%, #111115 100%) !important;
            border-right: 1px solid rgba(255, 199, 44, 0.15) !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #f5f6f9 !important;
        }
        
        /* Ensure selectbox text has perfect dark contrast on its white background */
        div[data-baseweb="select"] * {
            color: #1a1a24 !important;
        }
        
        /* Make standard input widget labels fully readable in Dark Mode */
        label p {
            color: #f5f6f9 !important;
            font-weight: 600 !important;
        }
        
        div[data-testid="stSidebarUserContent"] .stRadio label {
            color: #f5f6f9 !important;
        }
        
        .glass-card {
            background: rgba(22, 22, 26, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 199, 44, 0.15);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease-in-out;
            color: #f5f6f9 !important;
        }
        
        .glass-card:hover {
            border: 1px solid rgba(255, 199, 44, 0.35);
            box-shadow: 0 12px 40px 0 rgba(218, 41, 28, 0.12);
            transform: translateY(-2px);
        }
        
        .glass-header {
            background: linear-gradient(90deg, rgba(255, 199, 44, 0.12) 0%, rgba(218, 41, 28, 0.04) 60%, rgba(0, 0, 0, 0) 100%);
            border-left: 5px solid #FFC72C;
            border-radius: 4px 16px 16px 4px;
            padding: 20px;
            margin-bottom: 25px;
        }
        
        h1 {
            font-family: 'Outfit', sans-serif;
            font-weight: 800 !important;
            letter-spacing: -1px;
            color: #FFC72C !important;
            text-shadow: 0px 4px 12px rgba(255, 199, 44, 0.25);
        }
        
        h2, h3 {
            font-family: 'Outfit', sans-serif;
            font-weight: 600 !important;
            color: #f5f6f9 !important;
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
            background: linear-gradient(45deg, #FFC72C, #DA291C);
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
            background: linear-gradient(135deg, #DA291C 0%, #B81D13 100%) !important;
            color: #ffffff !important;
            border: 1px solid #FFC72C !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            box-shadow: 0 4px 15px rgba(218, 41, 28, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #FFC72C 0%, #E0AE1B 100%) !important;
            color: #070708 !important;
            border: 1px solid #DA291C !important;
            box-shadow: 0 4px 15px rgba(255, 199, 44, 0.4) !important;
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
DB_FILE = "sttb.db"

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
    
    conn.commit()
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

# ---------------------------------------------------------
# 4. TOP NAVIGATION BAR & THEME SYMBOL
# ---------------------------------------------------------
# Container/styling for top menu buttons
st.markdown("""
<style>
    /* Styling for Streamlit buttons inside the top navigation bar to look like premium nav elements */
    div.stButton > button {
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
</style>
""", unsafe_allow_html=True)

# 6-column layout for top navbar: Logo (1.2), 4 Navigation Buttons (2 each), and Theme Toggle Symbol (0.8)
nav_cols = st.columns([1.2, 2, 2, 2, 2, 0.8], vertical_alignment="center")

# Column 0: Sarawak State Flag Logo
with nav_cols[0]:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/7e/Flag_of_Sarawak.svg", width=65)

# Columns 1-4: Horizontal Navigation Menus
menu_options = [
    ("Welcome & Overview", "Overview"),
    ("Public Survey Form", "Survey"),
    ("Analytics Dashboard", "Dashboard"),
    ("Geographic Trust Map", "Map")
]

for idx, (page_val, label) in enumerate(menu_options):
    with nav_cols[idx + 1]:
        # Style active page with primary format, and others with secondary format
        is_active = (st.session_state["page"] == page_val)
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_{page_val}", type=btn_type, use_container_width=True):
            st.session_state["page"] = page_val
            st.rerun()

# Column 5: Theme Selector Symbol (☾ for Dark, ☀ for Light)
with nav_cols[5]:
    current_symbol = "☀" if st.session_state["theme_mode"] == "Dark Mode" else "☾"
    if st.button(current_symbol, key="theme_toggle_btn", use_container_width=True):
        if st.session_state["theme_mode"] == "Dark Mode":
            st.session_state["theme_mode"] = "Light Mode"
        else:
            st.session_state["theme_mode"] = "Dark Mode"
        st.rerun()


# Get current page selection from session state
page = st.session_state.get("page", "Welcome & Overview")

# ---------------------------------------------------------
# PAGE 1: WELCOME & OVERVIEW
# ---------------------------------------------------------
if page == "Welcome & Overview":
    st.markdown('<div class="glass-header"><h1>Sarawak Tech-Trust Barometer (STTB)</h1><div class="subtitle">A Social-Technical Framework for Digital Trust Measurement in Sarawak</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
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
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h3>Live Barometer Metrics</h3>
                <div style="margin: 20px 0;">
                    <div class="metric-label">Sarawak Tech-Trust Index</div>
                    <div class="metric-value">{state_avg:.2f}</div>
                    <div class="metric-label" style="color: {survey.get_trust_level(state_avg)['color']}; font-weight:bold;">
                        {survey.get_trust_level(state_avg)['level']}
                    </div>
                </div>
                <p style="font-size:0.85rem; color:#bdc3c7;">
                    Index updates automatically in real-time as new public survey responses are recorded.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Take survey redirect button
        if st.button("Begin Digital Trust Survey", use_container_width=True):
            st.session_state["page"] = "Public Survey Form"
            st.rerun()
        
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
    st.markdown('<div class="glass-header"><h1>STTB Public Survey Form</h1><div class="subtitle">Anonymized Civic Feedback Framework (PDPA 2010 Compliant)</div></div>', unsafe_allow_html=True)
    
    # Minimalist dynamic QR sharing code on top
    st.markdown("""
    <div class="glass-card" style="padding: 15px; margin-bottom: 20px;">
        <h4 style="margin: 0 0 5px 0; color:#ffd700;">Scan & Share Survey</h4>
        <p style="font-size: 0.85rem; color: #bdc3c7; margin: 0 0 12px 0;">Use the QR code below to access and distribute this digital trust survey online!</p>
    </div>
    """, unsafe_allow_html=True)
    
    qr_col1, qr_col2 = st.columns([1, 4])
    with qr_col1:
        target_url = "https://sarawak-tech-trust.streamlit.app"
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&color=003366&data={target_url}"
        st.markdown(f'<img src="{qr_api_url}" style="border: 3px solid white; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);" width="110" height="110">', unsafe_allow_html=True)
    with qr_col2:
        st.markdown(f"""
        <div style="padding-top: 10px;">
            <span style="font-size:0.85rem; color:#bdc3c7;"><b>Direct Link:</b></span><br>
            <a href="{target_url}" target="_blank" style="color:#ffd700; font-size:1.05rem; font-weight:bold; text-decoration:none;">{target_url}</a>
            <p style="font-size:0.8rem; color:#888888; margin-top:5px; margin-bottom:0;">Right-click the QR code image to save or copy it directly into thesis slides or brochures.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div class="glass-card">
        <h3>Instructions</h3>
        <p>This survey collects your evaluation regarding digital tools and state platforms in Sarawak. <b>No personally identifiable data (PII) is stored.</b> Please select your demographics and answer the questions below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Capture Demographics
    st.markdown("<h3 style='color:#ffd700;'>Step 1: Demographic Demarcation</h3>", unsafe_allow_html=True)
    
    age_group = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    occupation = st.selectbox("Occupation", ["Student", "Civil Servant", "Private Sector", "Self-Employed", "Retired", "Unemployed"])
    district = st.selectbox("Sarawak Division", list(SARAWAK_DIVISIONS.keys()) + ["Others"])
        
    st.markdown("---")
    
    # 2. Select Survey Type to avoid exhaustion
    survey_type = st.radio(
        "Choose Survey Mode:",
        ["Full Academic Survey (75 Questions - Collapsible)", "Rapid Mini-Survey (15 Questions - Recommended for quick testing)"],
        horizontal=True
    )
    
    survey_answers = {}
    
    if "75" in survey_type:
        st.markdown("<h3 style='color:#ffd700;'>Step 2: Core Digital Trust Evaluation (75 Items)</h3>", unsafe_allow_html=True)
        st.write("Questions are categorized by our 5 key digital trust pillars. Expand each tab to answer. Scale: 1 = Strongly Disagree, 5 = Strongly Agree.")
        
        # We render 5 expanding tabs (one for each pillar)
        p_codes = ["P1", "P2", "P3", "P4", "P5"]
        for p_code in p_codes:
            pillar_info = survey.SURVEY_METADATA["pillars"][p_code]
            with st.expander(f"Pillar: {pillar_info['name']} ({pillar_info['islamic_concept']})"):
                st.write(f"*{pillar_info['definition']}*")
                
                p_questions = [q for q in survey.QUESTIONS if q["pillar"] == p_code]
                for q in p_questions:
                    # Provide radio input
                    key = f"q_{q['code']}"
                    survey_answers[q["code"]] = st.slider(
                        f"[{q['code']}] {q['question']}",
                        min_value=1, max_value=5, value=3, step=1,
                        key=key
                    )
    else:
        st.markdown("<h3 style='color:#ffd700;'>Step 2: Core Digital Trust Evaluation (15 Representative Items)</h3>", unsafe_allow_html=True)
        st.write("This mini-survey contains exactly 1 question per variable (15 total) representing the complete framework scale. Averages will be extrapolated automatically.")
        
        # Render exactly one question per variable
        variables_featured = [
            "TA1.2", "TA2.2", "TA3.3",  # Pillar 1
            "ER1.3", "ER2.1", "ER3.1",  # Pillar 2
            "PC1.2", "PC2.1", "PC3.1",  # Pillar 3
            "SR1.1", "SR2.2", "SR3.4",  # Pillar 4
            "DI1.1", "DI2.3", "DI3.3",  # Pillar 5
        ]
        
        rep_questions = [q for q in survey.QUESTIONS if q["code"] in variables_featured]
        for q in rep_questions:
            key = f"mini_{q['code']}"
            survey_answers[q["code"]] = st.slider(
                f"[{q['code']}] {q['question']}",
                min_value=1, max_value=5, value=3, step=1,
                key=key
            )
            
        # Map remaining questions to the answered variable value to preserve database structure
        for q in survey.QUESTIONS:
            if q["code"] not in survey_answers:
                # Find matching representative code for that variable
                rep_code = [c for c in variables_featured if c.startswith(q['code'][:2])][0]
                survey_answers[q["code"]] = survey_answers[rep_code]
 
    submit_btn = st.button("Submit Anonymous Evaluation", use_container_width=True)
    
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
            st.success("Thank you! Your anonymous digital trust feedback has been securely computed and recorded.")
            
            # Show interactive report card
            st.markdown(f"""
            <div class="glass-card" style="border: 2px solid {results['trust_evaluation']['color']};">
                <h3 style="color: {results['trust_evaluation']['color']}; text-align: center;">
                    Your Personal Digital Trust Report Card
                </h3>
                <div style="text-align: center; margin: 20px 0;">
                    <div class="metric-label">Computed STTB Index</div>
                    <div class="metric-value" style="background:none; -webkit-text-fill-color: {results['trust_evaluation']['color']};">
                        {results['sttb_index']:.2f}
                    </div>
                    <div style="font-weight: 800; font-size: 1.3rem; color: {results['trust_evaluation']['color']};">
                        {results['trust_evaluation']['level']}
                    </div>
                    <p style="margin-top: 10px; font-size:0.9rem; color:#bdc3c7;">
                        {results['trust_evaluation']['interpretation']}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show breakdown
            col1, col2, col3, col4, col5 = st.columns(5)
            pillars_map = {
                "P1": "Transparency",
                "P2": "Ethics",
                "P3": "Privacy",
                "P4": "Security",
                "P5": "Inclusion"
            }
            
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
# ---------------------------------------------------------
elif page == "Analytics Dashboard":
    st.markdown('<div class="glass-header"><h1>STTB Analytics Dashboard</h1><div class="subtitle">Real-time Trust Indicators & Demographic Filters</div></div>', unsafe_allow_html=True)
    
    # Fetch all data from DB
    conn = get_db_connection()
    df_resp = pd.read_sql_query("SELECT * FROM respondents", conn)
    df_scores = pd.read_sql_query("SELECT * FROM computed_scores", conn)
    conn.close()
    
    # Merge datasets
    df = pd.merge(df_resp, df_scores, left_on="id", right_on="respondent_id")
    
    # Filter controls in sidebar-style layout inside dashboard
    st.markdown("<h3 style='color:#ffd700;'>Demographic Segment Filters</h3>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        f_district = st.multiselect("Filter District", ["All"] + list(SARAWAK_DIVISIONS.keys()) + ["Others"], default="All")
    with f_col2:
        f_age = st.multiselect("Filter Age Group", ["All", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"], default="All")
    with f_col3:
        f_gender = st.multiselect("Filter Gender", ["All", "Male", "Female"], default="All")
    with f_col4:
        f_occ = st.multiselect("Filter Occupation", ["All", "Student", "Civil Servant", "Private Sector", "Self-Employed", "Retired"], default="All")
        
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
        st.warning("No survey submissions match the selected filters. Reset filters to see data.")
    else:
        # Show key metric cards
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div class="metric-label">Active Sample Size (N)</div>
                <div class="metric-value" style="color:#ffd700;">{len(df_filtered)}</div>
                <div class="metric-label">Filtered Responses</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            idx_avg = df_filtered["sttb_index"].mean()
            eval_info = survey.get_trust_level(idx_avg)
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div class="metric-label">Segment STTB Index</div>
                <div class="metric-value" style="background:none; -webkit-text-fill-color: {eval_info['color']};">{idx_avg:.2f}</div>
                <div class="metric-label" style="color: {eval_info['color']}; font-weight:bold;">{eval_info['level']}</div>
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
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div class="metric-label">Weakest Trust Axis</div>
                <div class="metric-value" style="color:#C0392B; font-size:2.2rem; margin:15px 0;">{weakest}</div>
                <div class="metric-label" style="Score: {weakest_val:.1f} / 100">Score: {weakest_val:.1f} / 100</div>
            </div>
            """, unsafe_allow_html=True)

        # 1. Bar Chart of 5 Pillars
        st.markdown("<h3 style='color:#ffd700; margin-top:20px;'>Pillar Trust Profile Comparison</h3>", unsafe_allow_html=True)
        
        chart_data = pd.DataFrame({
            "Trust Pillar": list(pillar_averages.keys()),
            "Index Score": list(pillar_averages.values())
        })
        
        st.bar_chart(chart_data, x="Trust Pillar", y="Index Score", color="#ffd700")

        # 2. Division Rankings Table
        st.markdown("<h3 style='color:#ffd700; margin-top:20px;'>Administrative Division Rankings</h3>", unsafe_allow_html=True)
        
        div_summary = df_filtered.groupby("district").agg(
            respondents_count=("respondent_id", "count"),
            sttb_index_avg=("sttb_index", "mean"),
            transparency_avg=("ps1_transparency", "mean"),
            ethics_avg=("ps2_ethics", "mean"),
            privacy_avg=("ps3_privacy", "mean"),
            security_avg=("ps4_security", "mean"),
            inclusion_avg=("ps5_inclusion", "mean")
        ).reset_index()
        
        div_summary = div_summary.sort_values(by="sttb_index_avg", ascending=False)
        
        # Formatting for presentation
        div_presentation = div_summary.copy()
        div_presentation["sttb_index_avg"] = div_presentation["sttb_index_avg"].round(2)
        div_presentation = div_presentation.rename(columns={
            "district": "Sarawak Division",
            "respondents_count": "Sample (N)",
            "sttb_index_avg": "STTB Index (0-100)"
        })
        
        st.dataframe(
            div_presentation[["Sarawak Division", "Sample (N)", "STTB Index (0-100)"]],
            hide_index=True,
            use_container_width=True
        )
        
        # Collapsible Database Administration Panel (Admin Only)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🛠️ System Settings & Administration (UTS Admin Only)"):
            st.markdown("""
            <div style="padding: 10px; border-left: 3px solid #DA291C;">
                <h4 style="color:#DA291C; margin: 0 0 10px 0;">Database Administration Panel</h4>
                <p style="font-size:0.85rem; color:#bdc3c7; margin:0 0 15px 0;">
                    To transition this framework from the pilot evaluation phase to real-world academic data collection, you can purge all pre-seeded mock records here. This will clear the database entirely to a 0-submission slate and permanently stop the automated seed engine.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Purge All Pilot Database Records", type="secondary", use_container_width=True, key="admin_purge_btn"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM respondents")
                cursor.execute("DELETE FROM responses")
                cursor.execute("DELETE FROM computed_scores")
                cursor.execute("CREATE TABLE IF NOT EXISTS system_config (key TEXT UNIQUE, val TEXT)")
                cursor.execute("INSERT OR REPLACE INTO system_config (key, val) VALUES ('seeded', 'false')")
                conn.commit()
                conn.close()
                st.success("Database successfully purged to a clean state! Redirecting...")
                st.session_state["page"] = "Welcome & Overview"
                st.rerun()


# ---------------------------------------------------------
# PAGE 4: GEOGRAPHIC TRUST MAP
# ---------------------------------------------------------
elif page == "Geographic Trust Map":
    st.markdown('<div class="glass-header"><h1>Geographic Digital Trust Map</h1><div class="subtitle">Division-level Choropleth Trust Indicators (Grounded in Slocum et al., 2009)</div></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <p>This geographic model visualizes district-level public trust. Click on any colored division marker to inspect the detailed sample count, index averages, and custom-computed pillar variables.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load and process data
    conn = get_db_connection()
    df_resp = pd.read_sql_query("SELECT * FROM respondents", conn)
    df_scores = pd.read_sql_query("SELECT * FROM computed_scores", conn)
    conn.close()
    
    df = pd.merge(df_resp, df_scores, left_on="id", right_on="respondent_id")
    
    # Calculate division averages
    div_stats = df.groupby("district").agg(
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
            "sttb_index": 50.0, "count": 0, 
            "transparency": 50.0, "ethics": 50.0, "privacy": 50.0, "security": 50.0, "inclusion": 50.0
        })
        
        index_val = stats["sttb_index"]
        eval_info = survey.get_trust_level(index_val)
        
        popup_html = f"""
        <div style="font-family: 'Outfit', sans-serif; width: 220px; color: #2c3e50;">
            <h4 style="margin: 0 0 5px 0; color: #2980b9;">{div_name} Division</h4>
            <div style="font-size: 1.3rem; font-weight: 800; color: {eval_info['color']}; margin-bottom: 5px;">
                STTB Index: {index_val:.2f}
            </div>
            <div style="font-size: 0.85rem; font-weight: bold; margin-bottom: 10px;">
                Trust Level: {eval_info['level']} <br>
                Sample Size (N): {stats['count']}
            </div>
            <hr style="border: 0; border-top: 1px solid #ddd; margin: 8px 0;">
            <table style="width: 100%; font-size: 0.8rem;">
                <tr><td>Transparency:</td><td style="text-align:right; font-weight:bold;">{stats['transparency']:.1f}</td></tr>
                <tr><td>Ethics:</td><td style="text-align:right; font-weight:bold;">{stats['ethics']:.1f}</td></tr>
                <tr><td>Privacy:</td><td style="text-align:right; font-weight:bold;">{stats['privacy']:.1f}</td></tr>
                <tr><td>Security:</td><td style="text-align:right; font-weight:bold;">{stats['security']:.1f}</td></tr>
                <tr><td>Inclusion:</td><td style="text-align:right; font-weight:bold;">{stats['inclusion']:.1f}</td></tr>
            </table>
        </div>
        """
        
        # Color condition
        color_map = {
            "High Trust": "darkgreen",
            "Moderate Trust": "green",
            "Low Trust": "orange",
            "Very Low Trust": "red"
        }
        
        folium.CircleMarker(
            location=[coords["lat"], coords["lon"]],
            radius=12 + (stats["count"] * 0.1), # radius based on responses
            popup=folium.Popup(popup_html, max_width=250),
            color=eval_info["color"],
            fill=True,
            fill_color=eval_info["color"],
            fill_opacity=0.6,
            tooltip=f"{div_name}: Index = {index_val:.2f}"
        ).add_to(m)
        
    # Render folium map in Streamlit
    st_folium(m, width=1200, height=600)





# ---------------------------------------------------------
# 5. PERMANENT CENTRALIZED PAGE FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888888; font-size: 0.85rem; padding: 25px 0 10px 0;'>Sarawak Tech-Trust Barometer © 2026.</div>", unsafe_allow_html=True)

