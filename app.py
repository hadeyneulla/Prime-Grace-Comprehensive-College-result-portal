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
# SLEEK PROFESSIONAL STYLING
# -------------------------------------------------------------
st.markdown("""
    <style>
    /* Clean white background */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Sleek Typography for Title & Subtitle */
    .main-title { 
        text-align: center; 
        color: #0A4D2E; 
        font-weight: 800; 
        font-size: 2rem; 
        margin-top: 15px;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    .sub-title { 
        text-align: center; 
        color: #555555; 
        margin-bottom: 25px; 
        font-size: 1.1rem; 
        font-weight: 600;
    }
    
    /* Professional Welcome Card */
    .welcome-card { 
        background-color: #F8FBF9; 
        padding: 22px; 
        border-radius: 12px; 
        border-left: 6px solid #0A4D2E; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.04); 
        margin-bottom: 25px;
        color: #333333;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Sleek Button */
    .stButton>button { 
        width: 100%; 
        background-color: #0A4D2E; 
        color: white; 
        font-weight: bold; 
        font-size: 1.05rem;
        padding: 12px; 
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover { 
        background-color: #073820; 
        color: white; 
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
# To grant access to a student, simply remove or comment out their matric number from this list.
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
st.markdown("<h3 style='color: #0A4D2E; margin-bottom: 0px;'>🔍 Check Student Result</h3>", unsafe_allow_html=True)
matric_input = st.text_input("Enter Student Matric / Admission Number:", placeholder="e.g. PGCC20210118").strip()

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
                st.markdown("<h3 style='color: #0A4D2E;'>🔒 Important Security Notice</h3>", unsafe_allow_html=True)
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
