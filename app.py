import os
import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
import io

# -------------------------------------------------------------
# PAGE CONFIGURATION & SCHOOL STYLING
# -------------------------------------------------------------
st.set_page_config(
    page_title="Prime Grace Comprehensive College - Result Portal",
    page_icon="🎓",
    layout="centered"
)

# Custom School Styling
st.markdown("""
    <style>
    .main-title { text-align: center; color: #1F4E79; font-weight: bold; font-size: 2rem; margin-top: 10px; }
    .sub-title { text-align: center; color: #555; margin-bottom: 20px; font-size: 1.1rem; }
    .welcome-card { 
        background-color: #F0F4F8; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #1F4E79;
        margin-bottom: 25px;
        color: #333;
    }
    .stButton>button { width: 100%; background-color: #1F4E79; color: white; font-weight: bold; padding: 10px; }
    .stButton>button:hover { background-color: #153859; color: white; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🏫 SCHOOL LOGO & HEADER
# -------------------------------------------------------------
LOGO_URL = "logo.png"

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try:
        st.image(LOGO_URL, width=120)
    except:
        pass # Fallback if image is missing

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
# 🔒 CONTROL ACCESS LIST (Approved Parents Only)
# -------------------------------------------------------------
ALLOW_ALL = False 

# 👉 PASTE YOUR APPROVED STUDENT MATRIC NUMBERS HERE:
ALLOWED_MATRIC_NUMBERS = [
    "PGCC20210118",
    "PGCC20210119",
    "PGCC20250198"
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
# FORM INPUT
# -------------------------------------------------------------
st.markdown("### 🔍 Check Student Result")
matric_input = st.text_input("Enter Student Matric / Admission Number:", placeholder="e.g. PGCC20210118").strip()

search_clicked = st.button("Retrieve Result")

if search_clicked:
    if not matric_input:
        st.warning("Please enter a valid Admission/Matric number.")
    else:
        clean_user_input = clean_string(matric_input)
        
        # Check Access Permission
        is_allowed = ALLOW_ALL or any(clean_user_input == clean_string(m) for m in ALLOWED_MATRIC_NUMBERS)
        
        if not is_allowed:
            st.warning("⚠️ **Result Not Yet Available**")
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
                st.markdown("### 🔒 Important Security Notice")
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
                
                st.markdown("<br><p style='text-align: center; color: #777; font-size: 0.9rem;'>For enquiries, please contact the school administration directly.</p>", unsafe_allow_html=True)
            else:
                st.error("❌ No result file found matching that Admission/Matric Number.")
                st.caption("Please check for typing errors or contact the school administration.")
