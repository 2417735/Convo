import streamlit as st
import subprocess
import os
import shutil

# --- Simple Black UI ---
st.set_page_config(page_title="Convo", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main .block-container { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 3rem; }
    .stButton>button { background-color: white; color: black; font-weight: 700; width: 100%; border: none; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Convo")
st.write("Convert HWP to DOCX (Simple & Fast)")

uploaded_file = st.file_uploader("Upload your file", type=['hwp', 'hwpx'])

if uploaded_file is not None:
    # 1. Use an extremely simple filename to avoid any encoding errors
    base_name = "workfile"
    in_file = f"{base_name}.hwp"
    out_file = f"{base_name}.docx"
    final_docx_name = uploaded_file.name.rsplit('.', 1)[0] + ".docx"
    
    # Clean up any leftover files from previous failed runs
    for f in [in_file, out_file]:
        if os.path.exists(f): os.remove(f)

    # 2. Save the uploaded file
    with open(in_file, "wb") as f:
        f.write(uploaded_file.getbuffer())

    bar = st.progress(0)
    status = st.empty()
    status.text("Engine processing...")

    try:
        # 3. The "Master Command"
        # We add '--convert-to docx' and set a custom user profile to avoid lock errors
        cmd = [
            'soffice',
            '--headless',
            '-env:UserInstallation=file:///tmp/libreoffice_user',
            '--convert-to', 'docx',
            in_file
        ]
        
        # Run with a 2-minute timeout
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        # 4. Success Check
        if os.path.exists(out_file):
            bar.progress(100)
            status.success("Conversion Complete!")
            with open(out_file, "rb") as f:
                st.download_button(
                    label="DOWNLOAD DOCX",
                    data=f,
                    file_name=final_docx_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        else:
            # Show specific engine error
            st.error("Conversion failed. The engine could not read this specific file structure.")
            with st.expander("Technical Log (Check this)"):
                st.write("STDOUT:", result.stdout)
                st.write("STDERR:", result.stderr)
                st.write("Current Files in Folder:", os.listdir("."))

    except Exception as e:
        st.error(f"Error: {e}")
    
    finally:
        # Cleanup
        if os.path.exists(in_file): os.remove(in_file)
        if os.path.exists(out_file): os.remove(out_file)
