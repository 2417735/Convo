import streamlit as st
import subprocess
import os
import uuid

st.set_page_config(page_title="Big File HWP Converter", layout="centered")

# --- UI Styling ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; }
    .main .block-container { background: white; border-radius: 15px; padding: 2rem; color: #333; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Large File HWP Converter")
st.write("Specialized for files up to 500MB.")

# --- The Logic ---
uploaded_file = st.file_uploader("Upload your large HWP file", type=['hwp'])

if uploaded_file is not None:
    # Use a unique ID to prevent file collisions
    file_id = str(uuid.uuid4())[:6]
    in_file = f"large_input_{file_id}.hwp"
    out_file = f"large_input_{file_id}.docx"
    
    # Process the file
    with st.status("Processing large file... this may take a moment.") as status:
        # Save file to disk immediately (avoids keeping it in RAM)
        with open(in_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Run LibreOffice with 'lowriter' for better large-doc handling
        try:
            result = subprocess.run([
                'soffice', '--headless', '--convert-to', 'docx', '--outdir', '.', in_file
            ], capture_output=True, text=True, timeout=120) # 2-minute timeout for big files

            if os.path.exists(out_file):
                status.update(label="Conversion Complete!", state="complete")
                with open(out_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Resulting Word File",
                        data=f,
                        file_name=uploaded_file.name.replace(".hwp", ".docx"),
                        use_container_width=True
                    )
            else:
                st.error("The server ran out of memory. Try a smaller version of the file.")
                st.expander("Details").write(result.stderr)
        
        except Exception as e:
            st.error(f"Error: {e}")
        
        finally:
            # Cleanup to keep the server clean
            if os.path.exists(in_file): os.remove(in_file)
            if os.path.exists(out_file): os.remove(out_file)
