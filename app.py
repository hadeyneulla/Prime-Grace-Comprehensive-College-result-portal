import os
import json
import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
import io

# -------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="Prime Grace Comprehensive College - Portal",
    page_icon="🎓",
    layout="centered"
)

DATA_FILE = "portal_data.json"
ADMIN_PIN = "PGCC2026"  # 👉 Set your preferred Admin secret code here

# -------------------------------------------------------------
# PERSISTENT DATA HANDLERS (LOAD & SAVE)
# -------------------------------------------------------------
def load_portal_data():
    default_data = {
        "news": [
            {
                "tag": "ADMINISTRATION",
                "title": "Resumption Date for Next Term",
                "body": "All boarding students are expected to resume on Sunday, while day students commence on Monday at 7:45 AM prompt."
            },
            {
                "tag": "ACADEMICS",
                "title": "BECE & WAEC Extension Classes",
                "body": "Special tutorial sessions for JSS 3 and SS 3 students will continue as scheduled. Attendance is compulsory."
            }
        ],
        "timetable_type": "Regular Class Timetable",
        "timetable_rows": [
            {"Period": "Period 1 (8:00 - 8:45 AM)", "Monday": "Mathematics", "Tuesday": "English Studies", "Wednesday": "Basic Tech", "Thursday": "Mathematics", "Friday": "Civic Edu."},
            {"Period": "Period 2 (8:45 - 9:30 AM)", "Monday": "English Studies", "Tuesday": "Mathematics", "Wednesday": "Mathematics", "Thursday": "English Studies", "Friday": "Mathematics"},
            {"Period": "Break (9:30 - 9:45 AM)", "Monday": "Break", "Tuesday": "Break", "Wednesday": "Break", "Thursday": "Break", "Friday": "Break"},
            {"Period": "Period 3 (9:45 - 10:30 AM)", "Monday": "Basic Science", "Tuesday": "Civic Edu.", "Wednesday": "French", "Thursday": "Social Studies", "Friday": "Library"},
            {"Period": "Period 4 (10:30 - 11:15 AM)", "Monday": "Social Studies", "Tuesday": "Agric Sci.", "Wednesday": "Yoruba", "Thursday": "Basic Science", "Friday": "Clubs"}
        ]
    }
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(default_data, f, indent=4)
        return default_data
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return default_data

def save_portal_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

portal_data = load_portal_data()

# -------------------------------------------------------------
# PROFESSIONAL STYLING (MOBILE THEME OVERRIDES)
# -------------------------------------------------------------
st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: -10px;
    }
    .main-title { 
        text-align: center !important; 
        color: #0A4D2E !important; 
        font-weight: 800 !important; 
        font-size: 2rem !important; 
        margin-top: 15px !important;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
    }
    .sub-title { 
        text-align: center !important; 
        color: #555555 !important; 
        margin-bottom: 20px !important; 
        font-size: 1rem !important; 
        font-weight: 600 !important;
    }
    .welcome-card { 
        background-color: #F8FBF9 !important; 
        padding: 20px !important; 
        border-radius: 12px !important; 
        border-left: 6px solid #0A4D2E !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important; 
        margin-bottom: 20px !important;
        color: #222222 !important;
        font-size: 0.98rem !important;
        line-height: 1.6 !important;
    }
    .news-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E0E7E3 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03) !important;
    }
    .news-tag {
        background-color: #E8F5E9 !important;
        color: #0A4D2E !important;
        font-size: 0.8rem !important;
        font-weight: bold !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
        display: inline-block !important;
        margin-bottom: 8px !important;
    }
    div.stButton > button, div.stDownloadButton > button { 
        width: 100% !important; 
        background-color: #0A4D2E !important; 
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
    }
    div.stButton > button *, div.stDownloadButton > button * {
        color: #FFFFFF !important; 
        font-weight: bold !important; 
        font-size: 1.05rem !important;
    }
    button[data-baseweb="tab"] {
        font-size: 0.95rem !important;
        font-weight: bold !important;
        color: #333333 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0A4D2E !important;
        border-bottom-color: #0A4D2E !important;
    }
    label, p, span {
        color: #222222 !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🏫 HEADER & LOGO
# -------------------------------------------------------------
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    logo_file = "logo.png" if os.path.exists("logo.png") else ("logo.png.png" if os.path.exists("logo.png.png") else None)
    if logo_file:
        st.image(logo_file, use_container_width=True)

st.markdown("<h1 class='main-title'>Prime Grace Comprehensive College</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-title'>Excellency of His Grace • Student & Parent Portal</h4>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🔒 RESTRICTED MATRIC NUMBERS
# -------------------------------------------------------------
RESTRICTED_MATRIC_NUMBERS = [
    "PGCC20250215",  # Ogunsola Muiz (JSS 2)
    "PGCC20250218",  # Fatai Feranmi (JSS 3)
    "PGCC20230162",  # Akinlesi Semilore (JSS 3)
    "PGCC20230167",  # Dauda Muibat (JSS 3)
    "PGCC20230171",  # Ogunmuyiwa Roheem (JSS 3)
    "PGCC20250221",  # Ogunsola Waliyat (SS 1)
    "PGCC20220145",  # Olatokun Oyinkansola (SS 1)
    "PGCC20250227",  # Ogunsola Ramat (SS 2)
]

def clean_string(text):
    if not text:
        return ""
    return str(text).strip().upper().replace("/", "").replace("\\", "").replace(" ", "").replace("-", "_")

def encrypt_pdf(file_path, password):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(user_password=password, owner_password=f"OWNER_{password}")
    buffer = io.BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer

# -------------------------------------------------------------
# TABS (INCLUDES SECRET ADMIN/STAFF TAB)
# -------------------------------------------------------------
tab_results, tab_news, tab_timetable, tab_admin = st.tabs([
    "🎓 Student Result", 
    "📢 News & Notices", 
    "📅 Timetable",
    "🔐 Staff Admin"
])

# =============================================================
# TAB 1: RESULT CHECKER
# =============================================================
with tab_results:
    st.markdown("""
        <div class="welcome-card">
            <strong>Dear Parents and Guardians,</strong><br>
            Welcome to the official academic results portal. Enter your child's Matric/Admission number below to view and download their assessment sheet.<br><br>
            <em>Please note that downloaded results are password-protected using your child's exact matric number.</em>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #0A4D2E !important;'>🔍 Check Student Result</h3>", unsafe_allow_html=True)
    matric_input = st.text_input("Enter Student Matric / Admission Number:", placeholder="e.g. PGCC20100001", key="matric_input_field").strip()
    search_clicked = st.button("Retrieve Result", key="retrieve_btn")

    if search_clicked:
        if not matric_input:
            st.warning("Please enter a valid Admission/Matric number.")
        else:
            clean_user_input = clean_string(matric_input)
            is_blocked = any(clean_user_input == clean_string(m) for m in RESTRICTED_MATRIC_NUMBERS)
            
            if is_blocked:
                st.warning("⚠️ **Result Not Available**")
                st.info("Your child's result portal access is currently restricted or pending clearance. Please contact the school administration for further details.")
            else:
                pdf_folder = "." 
                found_file = None
                if os.path.exists(pdf_folder):
                    for file in os.listdir(pdf_folder):
                        if file.lower().endswith(".pdf"):
                            clean_filename = clean_string(file.replace(".pdf", "").replace(".PDF", ""))
                            if clean_user_input in clean_filename or clean_filename in clean_user_input:
                                found_file = os.path.join(pdf_folder, file)
                                break

                if found_file:
                    st.success("✅ Result Record Found Successfully!")
                    protected_pdf_buffer = encrypt_pdf(found_file, matric_input)
                    
                    st.markdown("---")
                    st.markdown("<h3 style='color: #0A4D2E !important;'>🔒 Security Notice</h3>", unsafe_allow_html=True)
                    st.info(
                        f"This PDF file is password-protected for privacy.\n\n"
                        f"**Password to open the PDF:** `{matric_input}`\n\n"
                        f"*(Type it exactly as shown — it is case-sensitive)*"
                    )
                    
                    st.download_button(
                        label="📥 Download Password-Protected PDF Result",
                        data=protected_pdf_buffer,
                        file_name=f"PrimeGrace_Result_{clean_user_input}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("❌ No result file found matching that Admission/Matric Number.")
                    st.caption("Please check for typing errors or contact the school administration.")

# =============================================================
# TAB 2: LIVE NOTICES
# =============================================================
with tab_news:
    st.markdown("<h3 style='color: #0A4D2E !important;'>📢 Notice Board & Updates</h3>", unsafe_allow_html=True)
    for item in portal_data.get("news", []):
        st.markdown(f"""
            <div class="news-card">
                <span class="news-tag">{item.get('tag', 'NOTICE')}</span>
                <h4 style="margin: 0; color: #0A4D2E;">{item.get('title', '')}</h4>
                <p style="margin-top: 5px; color: #555;">{item.get('body', '')}</p>
            </div>
        """, unsafe_allow_html=True)

# =============================================================
# TAB 3: LIVE TIMETABLE
# =============================================================
with tab_timetable:
    tt_title = portal_data.get("timetable_type", "School Timetable")
    st.markdown(f"<h3 style='color: #0A4D2E !important;'>📅 {tt_title}</h3>", unsafe_allow_html=True)
    
    df_tt = pd.DataFrame(portal_data.get("timetable_rows", []))
    if not df_tt.empty:
        st.dataframe(df_tt, hide_index=True, use_container_width=True)
    else:
        st.info("Timetable is currently being updated by the administration.")

# =============================================================
# TAB 4: HIDDEN ADMIN PORTAL (PROTECTED BY PIN)
# =============================================================
with tab_admin:
    st.markdown("<h3 style='color: #0A4D2E !important;'>🔐 Staff & Admin Dashboard</h3>", unsafe_allow_html=True)
    st.caption("Enter the administrator passcode to update announcements or change timetables.")
    
    entered_pin = st.text_input("Enter Admin Secret PIN:", type="password", key="admin_pin_input")
    
    if entered_pin == ADMIN_PIN:
        st.success("✅ Access Granted: Welcome Administrator!")
        
        # --- Section A: Manage News ---
        st.markdown("#### ✏️ Update School Notices")
        with st.expander("➕ Add New Announcement / Notice"):
            new_tag = st.selectbox("Category Tag:", ["ADMINISTRATION", "ACADEMICS", "ANNOUNCEMENT", "EXAMINATION", "EVENT"])
            new_title = st.text_input("Notice Title:")
            new_body = st.text_area("Notice Description:")
            if st.button("Publish Notice"):
                if new_title and new_body:
                    portal_data["news"].insert(0, {"tag": new_tag, "title": new_title, "body": new_body})
                    save_portal_data(portal_data)
                    st.success("Announcement published! Refresh the page to see live updates.")
                    st.rerun()
                else:
                    st.warning("Please fill out both the title and details.")
        
        # --- Section B: Manage Timetable ---
        st.markdown("#### ✏️ Update Timetable Mode & Schedule")
        new_tt_type = st.selectbox("Timetable Schedule Mode:", [
            "Regular Class Timetable",
            "Mid-Term Test Timetable",
            "Terminal Examination Timetable"
        ], index=0)
        
        st.caption("Edit timetable rows below (you can add rows, change subjects, and modify times):")
        editable_df = st.data_editor(pd.DataFrame(portal_data.get("timetable_rows", [])), num_rows="dynamic", use_container_width=True)
        
        if st.button("💾 Save All Timetable Changes"):
            portal_data["timetable_type"] = new_tt_type
            portal_data["timetable_rows"] = editable_df.to_dict(orient="records")
            save_portal_data(portal_data)
            st.success("Timetable updated successfully!")
            st.rerun()

    elif entered_pin:
        st.error("❌ Incorrect Admin PIN. Access denied.")
