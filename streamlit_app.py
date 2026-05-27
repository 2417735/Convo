import streamlit as st
import subprocess
import os

st.set_page_config(page_title="HWP to DOCX Fix", page_icon="📄")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #4A90E2; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 HWP to DOCX Converter")

uploaded_file = st.file_uploader("Upload HWP file", type=['hwp'])

if uploaded_file:
    # Use the original filename to avoid path issues
    hwp_name = uploaded_file.name
    docx_name = hwp_name.replace(".hwp", ".docx")

    # Save file
    with open(hwp_name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info(f"Converting {hwp_name}...")

    try:
        # THE FIX: We add '--outdir .' to force it to save in the current folder
        # We also use 'lowriter' which is the specific LibreOffice Writer command
        result = subprocess.run([
            'soffice', 
            '--headless', 
            '--convert-to', 'docx', 
            '--outdir', '.', 
            hwp_name
        ], capture_output=True, text=True)

        # DEBUG: Let's see what LibreOffice said
        if result.returncode != 0:
            st.error("Conversion engine failed.")
            st.code(result.stderr) # This shows the actual error
        else:
            # Check if the file actually exists now
            if os.path.exists(docx_name):
                with open(docx_name, "rb") as f:
                    st.success("Ready for download!")
                    st.download_button(
                        label="Click to Download DOCX",
                        data=f,
                        file_name=docx_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            else:
                st.warning("Conversion finished but the file wasn't found. Checking directory...")
                st.write("Files in folder:", os.listdir("."))

    except Exception as e:
        st.error(f"System Error: {e}")
    
    # Cleanup (Optional: keep these commented out while debugging)
    # os.remove(hwp_name)
    # if os.path.exists(docx_name): os.remove(docx_name)
