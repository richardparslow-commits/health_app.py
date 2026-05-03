import streamlit as st

# 1. Branding & Configuration
st.set_page_config(page_title="Life Policy Pilot | Health Class Predictor", page_icon="🩺", layout="wide")
PRIMARY_RED = "#CC0700" 
SILVER_GRAY = "#E2E8F0"

st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(180deg, {SILVER_GRAY} 0%, #FFFFFF 100%); }}
    .block-container {{ background-color: white; padding: 30px !important; border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.05); margin-top: 20px; }}
    h1, h2, h3 {{ color: {PRIMARY_RED} !important; }}
    .class-badge {{ display: inline-block; padding: 15px 30px; border-radius: 40px; font-size: 24px; font-weight: bold; color: #fff; text-align: center; margin-top: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.title("🩺 Health Class & Eligibility Predictor")
st.info("Complete all fields to finalize your Pre-Flight Health Audit.")

# 3. Input Tabs (Gathering variables for validation) 
tab1, tab2, tab3, tab4 = st.tabs(["👤 Identity", "🏥 Medical", "🚵 Lifestyle", "👨‍⚕️ Physicians"])

with tab1:
    name = st.text_input("Full Name (Include maiden name)")
    dob = st.text_input("Date of Birth (mm/dd/yyyy)")
    sex = st.radio("Sex", ["Male", "Female", "Other"])
    email_addr = st.text_input("Email Address") [cite: 56]
    phone = st.text_input("Phone Number")
    address = st.text_area("Home Address")
    col_ft, col_in = st.columns(2)
    with col_ft: ft = st.selectbox("Height (ft)", [4, 5, 6, 7], index=1)
    with col_in: inc = st.selectbox("Height (in)", list(range(12)), index=10)
    weight = st.number_input("Weight (lbs)", value=0)

with tab2:
    st.subheader("Medical Risk Factors") [cite: 53]
    m_check = st.checkbox("Controlled BP / Cholesterol")
    s_check = st.checkbox("History of Heart Attack / Stroke / Cancer")
    k_check = st.checkbox("Organ Transplant / ALS / COPD")
    meds = st.text_area("List all current Medications & Dosages")

with tab3:
    st.subheader("Lifestyle & Background") [cite: 53]
    income = st.number_input("Annual Income", value=0)
    occ = st.text_input("Occupation")
    nic = st.selectbox("Nicotine Use", ["None", "Current User"])
    criminal = st.checkbox("History of criminal offenses?")

with tab4:
    st.subheader("Physician Contact Info") [cite: 53]
    doc_name = st.text_input("Primary Physician Name")
    doc_visit = st.text_area("Reason for last visit & results")

# 4. Underwriting Logic
total_inches = (ft * 12) + inc
bmi = (weight * 703) / (total_inches * total_inches) if weight > 0 else 0

# 5. Validation Logic (THE GATEKEEPER)
# Define required fields
required_fields = [name, dob, email_addr, phone, address, weight, occ, doc_name, doc_visit]

# Check if all required fields have content
# Strings shouldn't be empty, numbers shouldn't be 0
is_form_complete = all([
    name != "", dob != "", email_addr != "", phone != "", 
    address != "", weight > 0, occ != "", 
    doc_name != "", doc_visit != ""
])

st.divider()

if not is_form_complete:
    # Warning message if anything is missing
    st.warning("⚠️ Please answer all questions to proceed with your fiduciary review.")
else:
    # If complete, show the results and the email submission button
    st.success("✅ Flight Data Complete. You may now submit for review.")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.write(f"**Estimated BMI:** {bmi:.1f}")
        st.markdown(f'<div class="class-badge" style="background: {PRIMARY_RED};">Analysis Ready</div>', unsafe_allow_html=True)
    
    # 6. Email Submission Button
    # This creates a mailto link that pre-fills the subject and body with the user's data
    subject = f"Health Analysis Request: {name}"
    body = f"Client Name: {name}%0D%0ADOB: {dob}%0D%0ABMI: {bmi:.1f}%0D%0AOccupation: {occ}%0D%0AMedications: {meds}"
    
    mailto_link = f"mailto:richardparslow@lifepolicypilot.blog?subject={subject}&body={body}"
    
    st.markdown(f"""
        <a href="{mailto_link}" style="text-decoration: none;">
            <div style="background-color: {PRIMARY_RED}; color: white; padding: 15px 25px; border-radius: 8px; text-align: center; font-weight: bold;">
                Email Results to Richard Parslow
            </div>
        </a>
    """, unsafe_allow_html=True)

st.caption("Disclaimer: This tool provides objective simulations. Final results are subject to full fiduciary review and carrier guidelines.")
