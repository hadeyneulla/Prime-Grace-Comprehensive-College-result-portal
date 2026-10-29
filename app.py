import os
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

# -------------------------------------------------------------
# SLEEK STYLING & HIGH-CONTRAST MOBILE SUPPORT
# -------------------------------------------------------------
st.markdown("""
    <style>
    /* Clean white background */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    
    /* Center logo */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: -10px;
    }
    
    /* Typography */
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
    
    /* Welcome & Notice Cards */
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
    
    /* Buttons */
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
    div.stButton > button:hover, div.stDownloadButton > button:hover { 
        background-color: #073820 !important; 
    }
    
    /* Tab Styling */
    button[data-baseweb="tab"] {
        font-size: 1rem !important;
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

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
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
# MINI WEBSITE TABS
# -------------------------------------------------------------
tab_results, tab_news, tab_timetable = st.tabs([
    "🎓 Student Result", 
    "📢 School Notice & News", 
    "📅 Class Timetable"
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
    
    st.markdown("<h3 style='color: #0A4D2E !important; margin-bottom: 0px;'>🔍 Check Student Result</h3>", unsafe_allow_html=True)
    matric_input = st.text_input("Enter Student Matric / Admission Number:", placeholder="e.g. PGCC20100001", key="matric_input_field").strip()
    search_clicked = st.button("Retrieve Result", key="retrieve_btn")

    if search_clicked:
        if not matric_input:
            st.warning("Please enter a valid Admission/Matric number.")
        else:
            clean_user_input = clean_string(matric_input)
            
            # Check if student access is restricted
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
# TAB 2: SCHOOL NEWS & ANNOUNCEMENTS
# =============================================================
with tab_news:
    st.markdown("<h3 style='color: #0A4D2E !important;'>📢 Notice Board & Updates</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="news-card">
            <span class="news-tag">ADMINISTRATION</span>
            <h4 style="margin: 0; color: #0A4D2E;">Resumption Date for Next Term</h4>
            <p style="margin-top: 5px; color: #555;">All boarding students are expected to resume on Sunday, while day students will commence full academic activities on Monday at 7:45 AM prompt.</p>
        </div>
        
        <div class="news-card">
            <span class="news-tag">ACADEMICS</span>
            <h4 style="margin: 0; color: #0A4D2E;">BECE & WAEC Extension Classes</h4>
            <p style="margin-top: 5px; color: #555;">Special tutorial sessions for JSS 3 and SS 3 students will continue as scheduled. Attendance is mandatory for all examination candidates.</p>
        </div>

        <div class="news-card">
            <span class="news-tag">ANNOUNCEMENT</span>
            <h4 style="margin: 0; color: #0A4D2E;">Parent-Teacher Association (PTA) Meeting</h4>
            <p style="margin-top: 5px; color: #555;">The general PTA meeting is scheduled to hold at the school assembly hall. Time: 10:00 AM. Your prompt attendance is appreciated.</p>
        </div>
    """, unsafe_allow_html=True)

# =============================================================
# TAB 3: CLASS TIMETABLE
# =============================================================
with tab_timetable:
    st.markdown("<h3 style='color: #0A4D2E !important;'>📅 Class Academic Timetable</h3>", unsafe_allow_html=True)
    
    selected_class = st.selectbox("Select Class to View Timetable:", [
        "JSS 1", "JSS 2", "JSS 3", "SS 1", "SS 2", "SS 3"
    ])
    
    # Sample daily schedule structure (edit or expand as needed)
    timetable_data = {
        "Period": ["Period 1 (8:00 - 8:45 AM)", "Period 2 (8:45 - 9:30 AM)", "Short Break (9:30 - 9:45 AM)", "Period 3 (9:45 - 10:30 AM)", "Period 4 (10:30 - 11:15 AM)", "Long Break (11:15 - 11:55 AM)", "Period 5 (11:55 - 12:40 PM)", "Period 6 (12:40 - 1:25 PM)"],
        "Monday": ["Mathematics", "English Studies", "Break", "Basic Science", "Social Studies", "Break", "Business Studies", "Computer Studies"],
        "Tuesday": ["English Studies", "Mathematics", "Break", "Civic Education", "Agricultural Sci.", "Break", "Christian Rel. Studies", "Fine Arts"],
        "Wednesday": ["Basic Technology", "Mathematics", "Break", "English Studies", "French", "Break", "Yoruba", "Physical & Health Edu."],
        "Thursday": ["Mathematics", "English Studies", "Break", "Social Studies", "Basic Science", "Break", "Home Economics", "Music"],
        "Friday": ["Civic Education", "Mathematics", "Break", "English Studies", "Library Period", "Break", "Clubs & Societies", "Closing Assembly"]
    }
    
    st.caption(f"Displaying regular academic timetable for **{selected_class}**:")
    df_timetable = pd.DataFrame(timetable_data)
    st.dataframe(df_timetable, hide_index=True, use_container_width=True)
    
    st.info("💡 Morning Assembly commences by 7:45 AM every weekday.")
