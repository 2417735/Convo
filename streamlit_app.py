import streamlit as st
import subprocess
import os
import uuid
import time

# --- Page Setup ---
st.set_page_config(page_title="Convo | HWP Converter", page_icon="📄", layout="centered")

# --- Simple Black Aesthetic Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main .block-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 3rem;
        margin-top: 5vh;
    }
    /* Simple White Button */
    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border-radius: 8px;
        font-weight: 700;
        height: 3em;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #cfcfcf; border: none; }
    /* File Uploader styling */
    .stFileUploader section { background-color: #0e1117; border: 1px dashed #30363d; }
    /* Hide branding */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Convo")
st.markdown("### Upload your HWP to convert into DOCX")
st.markdown("---")

uploaded_file = st.file_uploader("", type=['hwp'])

if uploaded_file is not None:
    # 1. Create unique, simple names to avoid Korean character errors in CMD
    file_id = str(uuid.uuid4())[:6]
    safe_in = f"file_{file_id}.hwp"
    safe_out = f"file_{file_id}.docx"
    final_name = uploaded_file.name.rsplit('.', 1)[0] + ".docx"
    
    # Save file
    with open(safe_in, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 2. Progress UI
    bar = st.progress(0)
    status = st.empty()
    
    try:
        # 3. Verify Engine Existence
        check_engine = subprocess.run(['which', 'soffice'], capture_output=True, text=True)
        
        if not check_engine.stdout:
            st.error("❌ Engine Error: LibreOffice is not installed yet.")
            st.info("Please ensure 'packages.txt' contains 'libreoffice' and wait 5 minutes for the server to update.")
        else:
            status.text("Converting... please wait.")
            # Start conversion
            process = subprocess.Popen([
                'soffice', '--headless', '--convert-to', 'docx', '--outdir', '.', safe_in
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 4. Progress Simulation
            pct = 0
            while process.poll() is None:
                time.sleep(0.6)
                if pct < 90:
                    pct += 2
                    bar.progress(pct)
            
            # 5. Check Output
            if os.path.exists(safe_out):
                bar.progress(100)
                status.empty()
                st.success("Conversion Complete")
                
                with open(safe_out, "rb") as f:
                    st.download_button(
                        label="DOWNLOAD DOCX",
                        data=f,
                        file_name=final_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
            else:
                stdout, stderr = process.communicate()
                st.error("Conversion failed.")
                with st.expander("Technical Log"):
                    st.code(stderr.decode())

    except Exception as e:
        st.error(f"System Error: {e}")
    
    finally:
        # Cleanup
        if os.path.exists(safe_in): os.remove(safe_in)
        if os.path.exists(safe_out): os.remove(safe_out)

else:
    st.write("Ready for upload.")
