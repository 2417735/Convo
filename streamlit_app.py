import streamlit as st
import subprocess
import os
import uuid
import time

# --- Page Setup ---
st.set_page_config(page_title="HWP Converter", page_icon="📄", layout="centered")

# --- Simple Black Aesthetic Styling ---
st.markdown("""
    <style>
    /* Dark background for the whole app */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* Simple black card for the content */
    .main .block-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 2.5rem;
        margin-top: 5vh;
    }
    /* Clean white buttons */
    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border-radius: 5px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #e2e2e2;
        color: #000000;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- UI Layout ---
st.title("Convo")
st.markdown("### Upload your HWP to convert into DOCX")
st.markdown("---")

uploaded_file = st.file_uploader("", type=['hwp'])

if uploaded_file is not None:
    # Safe naming for the 99MB file issue
    file_id = str(uuid.uuid4())[:6]
    in_file = f"conv_{file_id}.hwp"
    out_file = f"conv_{file_id}.docx"
    
    # Save the file to disk
    with open(in_file, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # --- Progress UI ---
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_text.text("Initializing conversion...")

    try:
        # Start conversion process
        process = subprocess.Popen([
            'soffice', '--headless', '--convert-to', 'docx', '--outdir', '.', in_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Simulate progress bar while converting
        percent = 0
        while process.poll() is None:
            time.sleep(0.7)
            if percent < 90:
                percent += 3
                progress_bar.progress(percent)
                status_text.text(f"Processing large document... {percent}%")
        
        # Check if output exists
        if os.path.exists(out_file):
            progress_bar.progress(100)
            status_text.text("Conversion Complete.")
            
            with open(out_file, "rb") as f:
                # The Download Option
                st.download_button(
                    label="DOWNLOAD DOCX",
                    data=f,
                    file_name=uploaded_file.name.replace(".hwp", ".docx"),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            st.success("File processed successfully.")
        else:
            st.error("Conversion failed. Please try a smaller file or check for corruption.")
            
    except Exception as e:
        st.error(f"Error: {e}")
    
    finally:
        # Cleanup
        if os.listdir('.'): # ensure we don't crash if folder is empty
            if os.path.exists(in_file): os.remove(in_file)
            if os.path.exists(out_file): os.remove(out_file)

else:
    st.info("Awaiting file upload...")
