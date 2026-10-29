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

DATA_FILE = "portal_data_v2.json"
ADMIN_PIN = "PGCC2026"  # 👉 Admin secret code

CLASSES = ["JSS 1", "JSS 2", "JSS 3", "SS 1", "SS 2", "SS 3"]
TIMETABLE_MODES = [
    "Regular Class Timetable",
    "Mid-Term Test Timetable",
    "Terminal Examination Timetable"
]

# -------------------------------------------------------------
# DEFAULT TIMETABLE TEMPLATES
# -------------------------------------------------------------
def get_default_regular_schedule():
    return [
        {"Period / Time": "8:00 - 8:45 AM", "Monday": "Mathematics", "Tuesday": "English Studies", "Wednesday": "Basic Science", "Thursday": "Mathematics", "Friday": "Civic Education"},
        {"Period / Time": "8:45 - 9:30 AM", "Monday": "English Studies", "Tuesday": "Mathematics", "Wednesday": "Mathematics", "Thursday": "English Studies", "Friday": "Mathematics"},
        {"Period / Time": "9:30 - 9:45 AM", "Monday": "SHORT BREAK", "Tuesday": "SHORT BREAK", "Wednesday": "SHORT BREAK", "Thursday": "SHORT BREAK", "Friday": "SHORT BREAK"},
        {"Period / Time": "9:45 - 10:30 AM", "Monday": "Basic Science", "Tuesday": "Civic Education", "Wednesday": "English Studies", "Thursday": "Social Studies", "Friday": "English Studies"},
        {"Period / Time": "10:30 - 11:15 AM", "Monday": "Social Studies", "Tuesday": "Agricultural Sci.", "Wednesday": "Business Studies", "Thursday": "Basic Tech", "Friday": "Library Period"},
        {"Period / Time": "11:15 - 11:55 AM", "Monday": "LONG BREAK", "Tuesday": "LONG BREAK", "Wednesday": "LONG BREAK", "Thursday": "LONG BREAK", "Friday": "LONG BREAK"},
        {"Period / Time": "11:55 - 12:40 PM", "Monday": "Business Studies", "Tuesday": "C.R.S", "Wednesday": "Yoruba / French", "Thursday": "Home Economics", "Friday": "Clubs & Societies"},
        {"Period / Time": "12:40 - 1:25 PM", "Monday": "Computer Studies", "Tuesday": "Fine Arts", "Wednesday": "P.H.E", "Thursday": "Computer Studies", "Friday": "Closing Assembly"}
    ]

def get_default_test_schedule():
    return [
        {"Date / Day": "Day 1 (Monday)", "Morning Session (9:00 - 10:00 AM)": "Mathematics", "Mid-Morning (11:00 - 12:00 PM)": "Civic Education", "Afternoon (1:00 - 2:00 PM)": "Basic Science"},
        {"Date / Day": "Day 2 (Tuesday)", "Morning Session (9:00 - 10:00 AM)": "English Studies", "Mid-Morning (11:00 - 12:00 PM)": "Social Studies", "Afternoon (1:00 - 2:00 PM)": "Computer Studies"},
        {"Date / Day": "Day 3 (Wednesday)", "Morning Session (9:00 - 10:00 AM)": "Business Studies", "Mid-Morning (11:00 - 12:00 PM)": "Agricultural Sci.", "Afternoon (1:00 - 2:00 PM)": "C.R.S"},
        {"Date / Day": "Day 4 (Thursday)", "Morning Session (9:00 - 10:00 AM)": "Basic Technology", "Mid-Morning (11:00 - 12:00 PM)": "Yoruba / French", "Afternoon (1:00 - 2:00 PM)": "Home Economics"},
        {"Date / Day": "Day 5 (Friday)", "Morning Session (9:00 - 10:00 AM)": "P.H.E", "Mid-Morning (11:00 - 12:00 PM)": "Fine Arts", "Afternoon (1:00 - 2:00 PM)": "Revision / Normal Classes"}
    ]

def get_default_exam_schedule():
    return [
        {"Date / Day": "Monday", "Paper 1 (8:30 - 10:30 AM)": "Mathematics", "Paper 2 (11:30 - 1:30 PM)": "Civic Education"},
        {"Date / Day": "Tuesday", "Paper 1 (8:30 - 10:30 AM)": "English Studies", "Paper 2 (11:30 - 1:30 PM)": "Agricultural Science"},
        {"Date / Day": "Wednesday", "Paper 1 (8:30 - 10:30 AM)": "Basic Science / Biology", "Paper 2 (11:30 - 1:30 PM)": "Business Studies / Economics"},
        {"Date / Day": "Thursday", "Paper 1 (8:30 - 10:30 AM)": "Social Studies / Government", "Paper 2 (11:30 - 1:30 PM)": "Computer Studies"},
        {"Date / Day": "Friday", "Paper 1 (8:30 - 10:30 AM)": "C.R.S", "Paper 2 (11:30 - 1:30 PM)": "Yoruba / Literature"}
    ]

# -------------------------------------------------------------
# PERSISTENT DATA HANDLERS (LOAD & SAVE)
# -------------------------------------------------------------
def load_portal_data():
    default_timetables = {}
    for cls in CLASSES:
        default_timetables[cls] = {
            "Regular Class Timetable": get_default_regular_schedule(),
            "Mid-Term Test Timetable": get_default_test_schedule(),
            "Terminal Examination Timetable": get_default_exam_schedule()
        }

    default_data = {
        "active_timetable_mode": "Regular Class Timetable",
        "news": [
            {
                "tag": "ADMINISTRATION",
                "title": "Resumption Date & Academic Calendar",
                "body": "All boarding students are expected to resume on Sunday, while day students commence on Monday at 7:45 AM prompt."
            },
            {
                "tag": "ACADEMICS",
                "title": "BECE & WAEC Extension Classes",
                "body": "Special tutorial sessions for JSS 3 and SS 3 students will continue as scheduled. Attendance is compulsory."
            },
            {
                "tag": "ANNOUNCEMENT",
                "title": "Parent-Teacher Association (PTA) Meeting",
                "body": "The general PTA meeting will hold at the school assembly hall by 10:00 AM. Your prompt attendance is appreciated."
            }
        ],
        "timetables": default_timetables
    }

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(default_data, f, indent=4)
        return default_data
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Ensure structure is complete
            if "timetables" not in data:
                data["timetables"] = default_timetables
            if "active_timetable_mode" not in data:
                data["active_timetable_mode"] = "Regular Class Timetable"
            return data
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
# TABS
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
    news_list = portal_data.get("news", [])
    if not news_list:
        st.info("No announcements posted at the moment.")
    for item in news_list:
        st.markdown(f"""
            <div class="news-card">
                <span class="news-tag">{item.get('tag', 'NOTICE')}</span>
                <h4 style="margin: 0; color: #0A4D2E;">{item.get('title', '')}</h4>
                <p style="margin-top: 5px; color: #555;">{item.get('body', '')}</p>
            </div>
        """, unsafe_allow_html=True)

# =============================================================
# TAB 3: MULTI-CLASS & MULTI-MODE TIMETABLE
# =============================================================
with tab_timetable:
    st.markdown("<h3 style='color: #0A4D2E !important;'>📅 Academic & Examination Timetables</h3>", unsafe_allow_html=True)
    
    active_default_mode = portal_data.get("active_timetable_mode", "Regular Class Timetable")
    default_mode_index = TIMETABLE_MODES.index(active_default_mode) if active_default_mode in TIMETABLE_MODES else 0

    col_cls, col_mode = st.columns(2)
    with col_cls:
        selected_class = st.selectbox("Select Student Class:", CLASSES, key="public_class_select")
    with col_mode:
        selected_mode = st.selectbox("Select Timetable Type:", TIMETABLE_MODES, index=default_mode_index, key="public_mode_select")
    
    st.caption(f"Showing **{selected_mode}** for **{selected_class}** (School Active Mode: *{active_default_mode}*):")
    
    class_schedules = portal_data.get("timetables", {}).get(selected_class, {})
    rows = class_schedules.get(selected_mode, [])
    
    df_tt = pd.DataFrame(rows)
    if not df_tt.empty:
        st.dataframe(df_tt, hide_index=True, use_container_width=True)
    else:
        st.info(f"No {selected_mode} has been uploaded for {selected_class} yet.")
    
    st.info("💡 Morning Assembly commences by 7:45 AM every weekday.")

# =============================================================
# TAB 4: STAFF ADMIN DASHBOARD (PROTECTED BY PIN)
# =============================================================
with tab_admin:
    st.markdown("<h3 style='color: #0A4D2E !important;'>🔐 Staff & Admin Dashboard</h3>", unsafe_allow_html=True)
    st.caption("Enter the administrator passcode to manage announcements and class timetables.")
    
    entered_pin = st.text_input("Enter Admin Secret PIN:", type="password", key="admin_pin_input")
    
    if entered_pin == ADMIN_PIN:
        st.success("✅ Access Granted: Welcome Administrator!")
        
        # --- Section A: Manage News ---
        st.markdown("---")
        st.markdown("#### 📢 1. Manage School Notices & News")
        
        with st.expander("➕ Publish a New Announcement"):
            new_tag = st.selectbox("Category Tag:", ["ADMINISTRATION", "ACADEMICS", "ANNOUNCEMENT", "EXAMINATION", "EVENT"])
            new_title = st.text_input("Notice Title:")
            new_body = st.text_area("Notice Details:")
            if st.button("Publish Notice", key="pub_news_btn"):
                if new_title and new_body:
                    portal_data["news"].insert(0, {"tag": new_tag, "title": new_title, "body": new_body})
                    save_portal_data(portal_data)
                    st.success("Announcement published!")
                    st.rerun()
                else:
                    st.warning("Please fill out both the title and details.")
        
        with st.expander("🗑️ Delete an Existing Announcement"):
            if portal_data.get("news"):
                news_titles = [f"{idx+1}. [{n['tag']}] {n['title']}" for idx, n in enumerate(portal_data["news"])]
                to_delete = st.selectbox("Select announcement to remove:", news_titles)
                if st.button("Delete Selected Notice", key="del_news_btn"):
                    del_idx = news_titles.index(to_delete)
                    portal_data["news"].pop(del_idx)
                    save_portal_data(portal_data)
                    st.success("Notice removed!")
                    st.rerun()
            else:
                st.write("No notices available to delete.")

        # --- Section B: Manage Timetables ---
        st.markdown("---")
        st.markdown("#### 📅 2. Edit Class & Exam Timetables")
        
        # Set Default Active Timetable Mode for Parents
        current_active = portal_data.get("active_timetable_mode", "Regular Class Timetable")
        active_idx = TIMETABLE_MODES.index(current_active) if current_active in TIMETABLE_MODES else 0
        
        new_default_mode = st.selectbox(
            "📌 Set Default Timetable Mode Shown to Parents First:",
            TIMETABLE_MODES,
            index=active_idx,
            help="When parents open the Timetable tab, this mode will automatically be selected first."
        )
        if new_default_mode != current_active:
            if st.button("Update Default Timetable Mode"):
                portal_data["active_timetable_mode"] = new_default_mode
                save_portal_data(portal_data)
                st.success(f"Default view set to: {new_default_mode}!")
                st.rerun()

        st.markdown("##### ✏️ Select Class & Timetable to Edit:")
        adm_col1, adm_col2 = st.columns(2)
        with adm_col1:
            edit_class = st.selectbox("Target Class:", CLASSES, key="admin_edit_class")
        with adm_col2:
            edit_mode = st.selectbox("Timetable Type to Edit:", TIMETABLE_MODES, key="admin_edit_mode")
        
        current_table_data = portal_data["timetables"].get(edit_class, {}).get(edit_mode, [])
        
        st.caption(f"Editing **{edit_mode}** for **{edit_class}** (Click any cell to edit, or use the '+' at the bottom of the table to add rows):")
        editable_df = st.data_editor(
            pd.DataFrame(current_table_data),
            num_rows="dynamic",
            use_container_width=True,
            key=f"editor_{edit_class}_{edit_mode}"
        )
        
        col_save_one, col_save_all = st.columns(2)
        with col_save_one:
            if st.button(f"💾 Save for {edit_class} Only", key="save_single_tt"):
                portal_data["timetables"][edit_class][edit_mode] = editable_df.to_dict(orient="records")
                portal_data["active_timetable_mode"] = edit_mode
                save_portal_data(portal_data)
                st.success(f"Saved {edit_mode} for {edit_class}!")
                st.rerun()
        with col_save_all:
            if st.button(f"📋 Copy This to ALL Classes", key="save_all_tt"):
                for cls in CLASSES:
                    portal_data["timetables"][cls][edit_mode] = editable_df.to_dict(orient="records")
                portal_data["active_timetable_mode"] = edit_mode
                save_portal_data(portal_data)
                st.success(f"Copied and saved {edit_mode} across all classes (JSS 1 - SS 3)!")
                st.rerun()

    elif entered_pin:
        st.error("❌ Incorrect Admin PIN. Access denied.")
