import streamlit as st
import subprocess
import os
import uuid

# --- Page Config ---
st.set_page_config(page_title="HWP to DOCX Converter", page_icon="📄")

# --- Custom Styling for "Good Background" ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin-top: 5vh;
    }
    h1 { color: #4A5568; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 HWP to DOCX")
st.write("Upload your file below. Even with long Korean names, this version will handle it!")

uploaded_file = st.file_uploader("Choose an HWP file", type=['hwp'])

if uploaded_file is not None:
    # 1. Generate a "Safe" temporary name to avoid command line errors
    # We use a random ID so multiple users don't overwrite each other
    safe_id = str(uuid.uuid4())[:8]
    temp_hwp = f"input_{safe_id}.hwp"
    temp_docx = f"input_{safe_id}.docx"
    
    # Keep the original name for the final download
    original_name = uploaded_file.name.rsplit('.', 1)[0] + ".docx"

    # 2. Save the uploaded file using the SAFE name
    with open(temp_hwp, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("🔄 Converting... large files may take a minute.")

    try:
        # 3. Run conversion with the safe filename
        result = subprocess.run([
            'soffice', '--headless', '--convert-to', 'docx', '--outdir', '.', temp_hwp
        ], capture_output=True, text=True)

        # 4. Check if the safe docx was created
        if os.path.exists(temp_docx):
            with open(temp_docx, "rb") as f:
                st.success("✨ Success! Your file is ready.")
                st.download_button(
                    label=f"⬇️ Download {original_name}",
                    data=f,
                    file_name=original_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        else:
            st.error("Conversion failed. The file is likely too large or complex for the server.")
            with st.expander("Show Technical Error Details"):
                st.write(result.stderr)
                st.write("Folder contents:", os.listdir("."))

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    
    finally:
        # 5. Cleanup temporary files
        if os.path.exists(temp_hwp): os.remove(temp_hwp)
        if os.path.exists(temp_docx): os.remove(temp_docx)
