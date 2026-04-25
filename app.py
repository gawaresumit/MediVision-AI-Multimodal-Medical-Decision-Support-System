import streamlit as st
from PIL import Image
from model import predict_xray
from text_model import analyze_symptoms
from utils import save_record, get_history, clear_history

# 1. Page Configuration
st.set_page_config(page_title="MediVision AI", layout="wide")

# 2. Custom CSS for professional look
st.markdown("""
    <style>
    [data-testid="stImage"] img {
        max-height: 400px;
        width: auto;
        border-radius: 15px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    .stButton>button {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 MediVision AI: Multimodal Medical Decision Support System")
st.write("Professional Multimodal Analysis: Combining Computer Vision with Symptom Correlation.")

# 3. Layout: Input and Preview
col1, col2, col3 = st.columns([1, 1, 0.5])

with col1:
    st.subheader("📋 Patient Details")
    name = st.text_input("Patient Full Name")
    symptoms = st.selectbox("Reported Symptoms", [
        "Routine checkup (no symptoms)",
        "Chest pain and breathing issue",
        "Severe bone pain after injury",
        "Persistent cough and fever",
        "Swelling and inability to move limb"
    ])
    file = st.file_uploader("Upload X-ray Scan", type=["jpg", "jpeg", "png"])

with col2:
    st.subheader("🖼️ Scan Preview")
    if file:
        image = Image.open(file)
        st.image(image, caption="Uploaded X-ray", use_container_width=True)
    else:
        st.info("Awaiting X-ray upload...")

# 4. Diagnosis Logic
if st.button("🚀 Run Full Diagnosis", use_container_width=True):
    if not name or not file:
        st.error("Missing Data: Please ensure name and image are provided.")
    else:
        with st.spinner("Analyzing scan and symptoms..."):
            img_label, img_conf, domain = predict_xray(image)
            text_label, text_conf = analyze_symptoms(symptoms)

        st.divider()

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("Image Analysis", img_label.upper(), f"{img_conf}% Confidence")
            st.info(f"System identified this as a **{domain}** scan.")

        with res_col2:
            st.metric("Symptom Check", text_label.upper())

        if img_label == text_label:
            st.success(f"✅ **Validated**: The scan results align with the patient's symptoms.")
        elif img_label == "uncertain":
            st.warning("⚠️ **Uncertain Scan**: Clinical symptoms take priority.")
        else:
            st.error("⚠️ **Clinical Mismatch**: Manual review required.")

        save_record(name, symptoms, img_label, domain)

# 5. History Section with Delete Functionality
st.divider()
# Use columns to put the button on the same line as the header
head_col, btn_col = st.columns([5, 1])

with head_col:
    st.subheader("📜 Diagnostic History")

with btn_col:
    if st.button("🗑️ Clear History", type="secondary"):
        clear_history()
        st.rerun()  # Forces the UI to refresh and show an empty table

history = get_history()

if history:
    st.table(history[::-1])  # Display latest records at the top
else:
    st.info("No diagnostic history available.")