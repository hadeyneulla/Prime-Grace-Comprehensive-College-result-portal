import os
import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
import io

# -------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="Prime Grace Comprehensive College - Result Portal",
    page_icon="🎓",
    layout="centered"
)

# -------------------------------------------------------------
# SLEEK PROFESSIONAL STYLING (BUTTON & THEME FIX)
# -------------------------------------------------------------
st.markdown("""
    <style>
    /* Force main app background to clean white in ALL modes */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    
    /* Force School Name to be visible in deep green across all modes */
    .main-title { 
        text-align: center !important; 
        color: #0A4D2E !important; 
        font-weight: 800 !important; 
        font-size: 2rem !important; 
        margin-top: 15px !important;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
    }
    
    /* Force Subtitle to be visible in clean charcoal grey */
    .sub-title { 
        text-align: center !important; 
        color: #333333 !important; 
        margin-bottom: 25px !important; 
        font-size: 1.1rem !important; 
        font-weight: 600 !important;
    }
    
    /* Professional Welcome Card */
    .welcome-card { 
        background-color: #F8FBF9 !important; 
        padding: 22px !important; 
        border-radius: 12px !important; 
        border-left: 6px solid #0A4D2E !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.06) !important; 
        margin-bottom: 25px !important;
        color: #222222 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Force ALL buttons (Retrieve & Download) to have high contrast white text */
    div.stButton > button, div.stDownloadButton > button { 
        width: 100% !important; 
        background-color: #0A4D2E !important; 
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
    }
    
    /* Force button text, paragraph, and span inside buttons to be bright white */
    div.stButton > button *, div.stDownloadButton > button * {
        color: #FFFFFF !important; 
        font-weight: bold !important; 
        font-size: 1.05rem !important;
    }
    
    div.stButton > button:hover, div.stDownloadButton > button:hover { 
        background-color: #073820 !important; 
    }
    
    /* Ensure general text labels are crisp */
    label, p, span {
        color: #222222 !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🏫 SCHOOL LOGO & HEADER (PERFECTLY CENTERED)
# -------------------------------------------------------------
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    logo_file = "logo.png" if os.path.exists("logo.png") else ("logo.png.png" if os.path.exists("logo.png.png") else None)
    if logo_file:
        st.image(logo_file, use_container_width=True)

st.markdown("<h1 class='main-title'>Prime Grace Comprehensive College</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-title'>Official Student Result & Assessment Portal</h4>", unsafe_allow_html=True)

# Thoughtful Welcome Note
st.markdown("""
    <div class="welcome-card">
        <strong>Dear Parents and Guardians,</strong><br><br>
        Greetings from Prime Grace Comprehensive College.<br><br>
        We hope your child is doing wonderfully. You can use this secure portal to check and download your child's academic results for the term.<br><br>
        We deeply appreciate the support and partnership you continue to give us in your child's education—it truly makes a difference. 
        <br><br>
        <em>Warm regards,</em><br>
        <strong>Prime Grace Comprehensive College Administration</strong>
    </div>
""", unsafe_allow_html=True)

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
# FORM INPUT & RETRIEVAL
# -------------------------------------------------------------
st.markdown("<h3 style='color: #0A4D2E !important; margin-bottom: 0px;'>🔍 Check Student Result</h3>", unsafe_allow_html=True)
matric_input = st.text_input("Enter Student Matric / Admission Number:", placeholder="e.g. PGCC20100001").strip()

search_clicked = st.button("Retrieve Result")

if search_clicked:
    if not matric_input:
        st.warning("Please enter a valid Admission/Matric number.")
    else:
        clean_user_input = clean_string(matric_input)
        
        # Check if student is restricted
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
                st.markdown("<h3 style='color: #0A4D2E !important;'>🔒 Important Security Notice</h3>", unsafe_allow_html=True)
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
