import os
import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
import io

# -------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="Student Result Portal",
    page_icon="🎓",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title { text-align: center; color: #1F4E79; font-weight: bold; }
    .sub-title { text-align: center; color: #555; margin-bottom: 30px; }
    .stButton>button { width: 100%; background-color: #2E75B6; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎓 School Result Portal</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-title'>Check & Download Student Academic Results</h4>", unsafe_allow_html=True)

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
def clean_string(text):
    """Removes slashes, spaces, dashes for flexible matching."""
    if not text:
        return ""
    return str(text).strip().upper().replace("/", "").replace("\\", "").replace(" ", "").replace("-", "_")

def encrypt_pdf(file_path, password):
    """Encrypts the PDF on the fly using the student's matric number as password."""
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
with st.container():
    st.info("💡 Enter your child's Matric/Admission Number below to retrieve their result.")
    
    matric_input = st.text_input("Matric / Admission Number:", placeholder="e.g. PGCC/2020/045").strip()
    
    search_clicked = st.button("🔎 Search Result")

if search_clicked:
    if not matric_input:
        st.warning("Please enter a valid Admission/Matric number.")
    else:
        clean_user_input = clean_string(matric_input)
        pdf_folder = "results_pdf"
        
        found_file = None
        
        # Look for matching PDF file in results_pdf folder
        if os.path.exists(pdf_folder):
            for file in os.listdir(pdf_folder):
                if file.lower().endswith(".pdf"):
                    clean_filename = clean_string(file.replace(".pdf", "").replace(".PDF", ""))
                    if clean_user_input in clean_filename or clean_filename in clean_user_input:
                        found_file = os.path.join(pdf_folder, file)
                        break

        if found_file:
            st.success("✅ Result Record Found!")
            
            # Encrypt PDF on download using the matric input as the password
            protected_pdf_buffer = encrypt_pdf(found_file, matric_input)
            
            st.markdown("---")
            st.markdown("🔒 **Security Note:** Your downloaded PDF is password protected.")
            st.markdown(f"Use your child's Matric Number (`{matric_input}`) as the password to open it.")
            
            st.download_button(
                label="📥 Download Password-Protected PDF",
                data=protected_pdf_buffer,
                file_name=f"Result_{clean_user_input}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("❌ No result found matching that Admission/Matric Number.")
            st.caption("Please check for typing errors or contact the school administration.")
