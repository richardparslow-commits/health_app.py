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
    
    .class-badge {{
        display: inline-block;
        padding: 15px 30px;
        border-radius: 40px;
        font-size: 24px;
        font-weight: bold;
        color: #fff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 10px;
    }}
    .eligibility-box {{
        background: #f8fafc;
        border: 2px solid {PRIMARY_RED};
        padding: 20px;
        border-radius: 12px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.title("🩺 Health Class & Eligibility Predictor")
st.info("Evaluate your Health Class & Product Eligibility based on fiduciary-grade pre-underwriting logic.")

# 3. Input Tabs (The 88-Question Integration)
tab1, tab2, tab3, tab4 = st.tabs(["👤 Identity & Physical", "🏥 Medical Profile", "🚵 Lifestyle & Background", "👨‍⚕️ Physicians"])

with tab1:
    col_id, col_phys = st.columns(2)
    with col_id:
        st.subheader("Identity")
        name = st.text_input("Full Name (Include maiden name)")
        dob = st.text_input("Date of Birth (mm/dd/yyyy)")
        sex = st.radio("Sex", ["Male", "Female", "Other"])
        citizen = st.radio("U.S. Citizen?", ["Yes", "No"])
    
    with col_phys:
        st.subheader("Physical Specs")
        col_ft, col_in = st.columns(2)
        with col_ft:
            ft = st.selectbox("Height (ft)", [4, 5, 6, 7], index=1)
        with col_in:
            inc = st.selectbox("Height (in)", list(range(12)), index=10)
        weight = st.number_input("Weight (lbs)", value=180)
        
        st.markdown("---")
        nic = st.selectbox("Nicotine Use", ["Never / >3 years clean", "1-3 years clean", "Current / Within 12 months"])
        weed = st.selectbox("Marijuana Use", ["None", "Occasional / Recreational", "Medical Prescription", "Daily Use (>5x week)"])

with tab2:
    st.subheader("Comprehensive Risk Profile")
    col_mild, col_sev, col_ko = st.columns(3)
    
    with col_mild:
        st.markdown("##### 🟡 Mild / Moderate Risk")
        m1 = st.checkbox("Controlled BP / Cholesterol")
        m2 = st.checkbox("Thyroid / Celiac / GERD")
        m3 = st.checkbox("Asthma / Sleep Apnea / Migraines")
        m4 = st.checkbox("Anxiety / Depression / PTSD")
        m5 = st.checkbox("Diabetes Type 2 (Oral Meds)")
        
    with col_sev:
        st.markdown("##### 🟠 Severe / Substandard")
        s1 = st.checkbox("Diabetes (Insulin / Complications)")
        s2 = st.checkbox("Heart Attack / Stent / Angina")
        s3 = st.checkbox("Stroke / TIA / A-Fib")
        s4 = st.checkbox("Past History of Cancer")
        s5 = st.checkbox("Bipolar / Suicide Attempt")
        
    with col_ko:
        st.markdown("##### 🔴 Knockouts / GI Only")
        k1 = st.checkbox("Organ Transplant / ICD")
        k2 = st.checkbox("ALS / Alzheimer's / Dementia")
        k3 = st.checkbox("COPD / Emphysema / Oxygen")
        k4 = st.checkbox("Kidney Failure / Dialysis")
        k5 = st.checkbox("Active/Current Cancer Treatment")

with tab3:
    st.subheader("Lifestyle & Background")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        income = st.number_input("Annual Income", value=75000)
        occ = st.text_input("Occupation")
        military = st.radio("Armed Forces / Reserves?", ["Yes", "No"])
    with col_l2:
        risk_hobbies = st.checkbox("High-Risk Hobbies (Skydiving, Racing, etc.)")
        pilot_license = st.checkbox("Pilot License / Flown in past 5 years")
        criminal = st.checkbox("Criminal Offense / Parole history")
        bankruptcy = st.checkbox("Bankruptcy / Bad Debt (Last 5 years)")

with tab4:
    st.subheader("Physician Data")
    st.text_input("Primary Physician Name")
    st.text_area("Reason last seen and results of visit")
    st.text_area("List all current Medications & Dosages")

# 4. Underwriting Logic (The "cRank" System)
total_inches = (ft * 12) + inc
bmi = (weight * 703) / (total_inches * total_inches)

hClass = "Standard"
cRank = 4 
badge_color = "#f1c40f"

if bmi <= 29:
    hClass, cRank, badge_color = "Preferred Plus", 1, "#2ecc71"
elif bmi <= 30:
    hClass, cRank, badge_color = "Preferred", 2, "#2ecc71"
elif bmi <= 32:
    hClass, cRank, badge_color = "Standard Plus", 3, "#2ecc71"
elif bmi <= 36:
    hClass, cRank, badge_color = "Standard", 4, "#f1c40f"
elif bmi <= 42:
    hClass, cRank, badge_color = "Table Rated", 5, "#e67e22"
else:
    hClass, cRank, badge_color = "Decline (GI Only)", 6, "#e74c3c"

if nic == "Current / Within 12 months" and cRank < 4:
    hClass, cRank, badge_color = "Standard Smoker", 4, "#f1c40f"
if weed in ["Medical Prescription", "Daily Use (>5x week)"] and cRank < 4:
    hClass, cRank, badge_color = "Standard", 4, "#f1c40f"

if any([m1, m2, m3, m4, m5]) and cRank < 4:
    hClass, cRank, badge_color = "Standard", 4, "#f1c40f"
if any([s1, s2, s3, s4, s5]) and cRank < 5:
    hClass, cRank, badge_color = "Table Rated (Substandard)", 5, "#e67e22"
if any([k1, k2, k3, k4, k5]) or criminal:
    hClass, cRank, badge_color = "Decline (GI Only)", 6, "#e74c3c"

# 5. Results & Eligibility Dashboard
st.divider()
col_res1, col_res2 = st.columns([1, 1.5])

with col_res1:
    st.markdown(f"### Results")
    st.write(f"**Estimated BMI:** {bmi:.1f}")
    st.markdown(f'<div>Estimated Health Class:</div><div class="class-badge" style="background: {badge_color};">{hClass}</div>', unsafe_allow_html=True)

with col_res2:
    st.markdown("### ✈️ Market Navigator: Eligibility")
    with st.container():
        st.markdown('<div class="eligibility-box">', unsafe_allow_html=True)
        if cRank <= 4:
            st.write("✅ **Standard & Top Tier Products Available**")
            st.write("* Term Life / IUL / Whole Life")
        elif cRank == 5:
            st.write("⚠️ **Substandard Markets Required**")
            st.write("* Substandard Term/IUL (Higher Premium)")
            st.write("* Graded / Modified Final Expense")
        else:
            st.write("🚫 **Restricted Access**")
            st.write("* Guaranteed Issue (GI) Whole Life **ONLY**")
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.link_button("Submit Data for Fiduciary Review", "https://lifepolicypilot.blog/contact-2/")
st.caption("Disclaimer: This tool provides general estimates based on universal field underwriting guidelines. Final risk classification is subject to formal carrier review.")
