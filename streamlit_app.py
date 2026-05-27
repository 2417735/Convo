
# Convo
import streamlit as st
import subprocess
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="HWP to DOCX - Clean Convert", 
    page_icon="📄",
    layout="centered" # Centered content for a focused UI
)

# --- Define Advanced Custom CSS for Background and UI ---
# This CSS handles the background gradient, the central card shadow, and text styling.
def local_css():
    st.markdown(
        """
        <style>
        /* Modern, professional background gradient (Blue tones) */
        .stApp {
            background: rgb(240,249,255);
            background: linear-gradient(135deg, rgba(240,249,255,1) 0%, rgba(224,242,254,1) 50%, rgba(191,219,254,1) 100%);
        }

        /* Styling the central Main container to look like a floating card */
        .main .block-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            margin-top: 3rem;
            max-width: 600px;
        }

        /* Modernize headers */
        h1, h2, h3 {
            color: #1e3a8a; /* Deep blue */
            font-weight: 700 !important;
        }

        /* Stylized subheading */
        .subheader-text {
            font-size: 1.1rem;
            color: #6b7280; /* Gray text */
            margin-bottom: 2rem;
        }

        /* Styling the file uploader widget slightly */
        .stFileUploader {
            border: 2px dashed #60a5fa; /* Blue dashed border */
            border-radius: 12px;
            padding: 10px;
            background-color: #f8fafc;
        }

        /* Success/Progress boxes customization */
        .stAlert > div {
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Inject the CSS
local_css()


# --- Main UI Area ---
# Using an illustrative logo or emoji
st.markdown("<div style='text-align: center;'><h1>📄 HWP <span style='color: #60a5fa;'>⇌</span> DOCX</h1></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;' class='subheader-text'>Clean, instant Hancom file converter. Built for everyone.</div>", unsafe_allow_html=True)

# Add a spacer
st.markdown("<br>", unsafe_allow_html=True)

# The Uploader Widget
uploaded_file = st.file_uploader("Drop your HWP file here", type=['hwp'], key="uploader")

# --- Core Logic ---
if uploaded_file is not None:
    # 1. Provide temporary filenames
    hwp_filename = "temp_input.hwp"
    docx_filename = "temp_input.docx"

    # 2. Save uploaded file to disk
    with open(hwp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 3. Visual Feedback: Conversion
    with st.spinner("Processing... translating formats..."):
        try:
            # 4. Run LibreOffice headless conversion
            process = subprocess.run([
                'soffice', '--headless', '--convert-to', 'docx', hwp_filename
            ], capture_output=True, text=True, check=True)

            # 5. Visual Feedback: Completion & Download
            if os.path.exists(docx_filename):
                # Calculate new filename for download
                clean_name = uploaded_file.name.rsplit('.', 1)[0] + ".docx"

                with open(docx_filename, "rb") as f:
                    docx_data = f.read()

                st.success("🎉 Conversion Complete!")
                
                # Big, primary download button
                st.download_button(
                    label=f"⬇️ Download {clean_name}",
                    data=docx_data,
                    file_name=clean_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True # Make button full width for modern look
                )

        except subprocess.CalledProcessError as e:
            st.error(f"**Error During Conversion:**\n\nIs LibreOffice installed? Standard output:\n{e.stdout}\n\nError output:\n{e.stderr}")
        except Exception as e:
            st.error(f"A generic error occurred: {e}")
        finally:
            # 6. Crucial Cleanup: Remove temporary files immediately after use
            if os.path.exists(hwp_filename):
                os.remove(hwp_filename)
            if os.path.exists(docx_filename):
                os.remove(docx_filename)

# --- Subtle Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9ca3af; font-size: 0.8rem;'>"
    "Hosted securely on Streamlit Cloud using LibreOffice engine.<br>"
    "Files are deleted immediately after conversion."
    "</div>", 
    unsafe_allow_html=True
)
