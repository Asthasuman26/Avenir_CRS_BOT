import streamlit as st
import subprocess
import sys
import os
import time

# PAGE CONFIG

st.set_page_config(
    page_title="Avenir International Engineers & Consultant | CRS Platform",
    layout="wide"
)

# IMPROVED PROFESSIONAL THEME

st.markdown("""
<style>

/* Slightly darker warm background */
html, body, [class*="css"]  {
    background-color: #eae7e2 !important;
    color: #0f172a !important;
}

/* Override streamlit containers */
[data-testid="stAppViewContainer"] {
    background-color: #eae7e2 !important;
}

[data-testid="stHeader"] {
    background-color: #eae7e2 !important;
}

/* Main container */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

/* Company Name */
.company-name {
    font-size: 32px;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 6px;
}

/* Platform Title */
.platform-title {
    font-size: 36px;
    font-weight: 700;
    color: #0f172a;
    margin-top: 10px;
}

/* Subtitle */
.subtitle {
    font-size: 16px;
    color: #475569;
    margin-bottom: 40px;
}

/* Cards */
.card {
    background: #ffffff;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Section Title */
.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #1f2937;
}

/* Button */
div.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: 500;
    border-radius: 12px;
    height: 48px;
    border: none;
    width: 100%;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
}

/* Footer */
.footer {
    text-align: center;
    font-size: 12px;
    color: #64748b;
    margin-top: 60px;
}

</style>
""", unsafe_allow_html=True)

# HEADER

st.markdown('<div class="company-name">Avenir International Engineers & Consultant</div>', unsafe_allow_html=True)
st.markdown('<div class="platform-title">CRS Automation Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Automated extraction and structured Comment Resolution Sheet generation for engineering drawings and review documents.</div>',
    unsafe_allow_html=True
)

# LAYOUT

left_col, right_col = st.columns([2, 1])

with left_col:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Upload Input Document</div>', unsafe_allow_html=True)

    uploaded_pdf = st.file_uploader(
        "Select Engineering Drawing or CRS PDF",
        type=["pdf"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Upload Output Template (Optional)</div>', unsafe_allow_html=True)

    uploaded_template = st.file_uploader(
        "Select Word Template (.docx)",
        type=["docx"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Processing</div>', unsafe_allow_html=True)

    selected_bot = st.selectbox(
        "Processing Mode",
        [
            "Auto Mode",
            "Structured CRS Only",
            "Drawing Comments Only"
        ]
    )

    generate_button = st.button("Generate CRS Output")

    st.markdown('</div>', unsafe_allow_html=True)

# PROCESSING

if uploaded_pdf:

    os.makedirs("backend/storage/uploads", exist_ok=True)

    pdf_path = "backend/storage/uploads/input.pdf"

    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.read())

    if uploaded_template:
        template_path = "backend/storage/uploads/custom_template.docx"
        with open(template_path, "wb") as f:
            f.write(uploaded_template.read())

    if generate_button:

        progress = st.progress(0)

        try:
            for i in range(20, 80, 20):
                progress.progress(i)
                time.sleep(0.2)

            subprocess.run(
                [sys.executable, "-m", "backend.final_bot_main"],
                capture_output=True,
                text=True,
                check=True
            )

            progress.progress(100)

            st.success("CRS generated successfully")

            output_dir = "backend/storage/outputs"
            files = os.listdir(output_dir)

            latest_file = sorted(
                [os.path.join(output_dir, f) for f in files],
                key=os.path.getmtime
            )[-1]

            with open(latest_file, "rb") as file:
                st.download_button(
                    label="Download Output File",
                    data=file,
                    file_name=os.path.basename(latest_file)
                )

        except subprocess.CalledProcessError as e:
            st.error("Processing failed")
            st.text(e.stderr)

# FOOTER

st.markdown('<div class="footer">© Avenir International Engineers & Consultant</div>', unsafe_allow_html=True)