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
st.info("Evaluate your Health Class & Product Eligibility based on fiduciary-grade pre-underwriting logic.")

# 3. Input Tabs
tab1, tab2, tab3, tab4 = st.tabs(["👤 Identity & Physical", "🏥 Medical Profile", "🚵 Lifestyle & Background", "👨‍⚕️ Physicians"])

with tab1:
    col_id, col_phys = st.columns(2)
    with col_id:
        st.subheader("Identity")
        name = st.text_input("Full Name (Include maiden name)")
        dob = st.text_input("Date of Birth (mm/dd/yyyy)")
        email_addr = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        sex = st.radio("Sex", ["Male", "Female", "Other"])
        address = st.text_area("Home Address")
    
    with col_phys:
        st.subheader("Physical Specs")
        col_ft, col_in = st.columns(2)
        with col_ft:
            ft = st.selectbox("Height (ft)", [4, 5, 6, 7], index=1)
        with col_in:
            inc = st.selectbox("Height (in)", list(range(12)), index=10)
        weight = st.number_input("Weight (lbs)", value=0)
        
        st.markdown("---")
        nic = st.selectbox("Nicotine Use", ["Never / >3 years clean", "1-3 years clean", "Current / Within 12 months"])
        weed = st.selectbox("Marijuana Use", ["None", "Occasional / Recreational", "Medical Prescription", "Daily Use (>5x week)"])

with tab2:
    st.subheader("Comprehensive Risk Profile")
    col_mild, col_sev, col_ko = st.columns(3)
    with col_mild:
        st.markdown("##### 🟡 Mild Risk")
        m1 = st.checkbox("Controlled BP / Cholesterol")
        m2 = st.checkbox("Thyroid / Celiac / GERD")
        m3 = st.checkbox("Asthma / Sleep Apnea / Migraines")
    with col_sev:
        st.markdown("##### 🟠 Severe Risk")
        s1 = st.checkbox("Diabetes (Insulin)")
        s2 = st.checkbox("Heart Attack / Stent")
        s3 = st.checkbox("History of Cancer")
    with col_ko:
        st.markdown("##### 🔴 Knockouts")
        k1 = st.checkbox("Organ Transplant / ICD")
        k2 = st.checkbox("COPD / Emphysema")
        k3 = st.checkbox("Kidney Failure / Dialysis")

with tab3:
    st.subheader("Lifestyle & Background")
    occ = st.text_input("Occupation")
    income = st.number_input("Annual Income", value=0)
    criminal = st.checkbox("Criminal Offense / Parole history")
    hobbies = st.text_area("Exercise Routine & High-Risk Hobbies")

with tab4:
    st.subheader("Physician Data")
    doc_name = st.text_input("Primary Physician Name")
    doc_visit = st.text_area("Reason for last visit and results")
    meds = st.text_area("Current Medications & Dosages")

# 4. Underwriting Logic
total_inches = (ft * 12) + inc
bmi = (weight * 703) / (total_inches * total_inches) if weight > 0 else 0

hClass = "Standard"
cRank = 4 
badge_color = "#f1c40f"

if bmi > 0:
    if bmi <= 29: hClass, cRank, badge_color = "Preferred Plus", 1, "#2ecc71"
    elif bmi <= 30: hClass, cRank, badge_color = "Preferred", 2, "#2ecc71"
    elif bmi <= 32: hClass, cRank, badge_color = "Standard Plus", 3, "#2ecc71"
    elif bmi <= 36: hClass, cRank, badge_color = "Standard", 4, "#f1c40f"
    elif bmi <= 42: hClass, cRank, badge_color = "Table Rated", 5, "#e67e22"
    else: hClass, cRank, badge_color = "Decline (GI Only)", 6, "#e74c3c"

if nic == "Current / Within 12 months" and cRank < 4:
    hClass, cRank, badge_color = "Standard Smoker", 4, "#f1c40f"

if any([m1, m2, m3]) and cRank < 4:
    hClass, cRank, badge_color = "Standard", 4, "#f1c40f"
if any([s1, s2, s3]) and cRank < 5:
    hClass, cRank, badge_color = "Table Rated (Substandard)", 5, "#e67e22"
if any([k1, k2, k3]) or criminal:
    hClass, cRank, badge_color = "Decline (GI Only)", 6, "#e74c3c"

# 5. Validation Logic
# We check if required text fields are empty or numbers are zero
is_complete = all([
    name != "", dob != "", email_addr != "", phone != "", 
    address != "", weight > 0, occ != "", 
    doc_name != "", doc_visit != ""
])

st.divider()

if not is_complete:
    # This message pops up if any required question is left unanswered
    st.warning("⚠️ Please answer all questions to proceed with your fiduciary review.")
else:
    # If everything is answered, show the results and the email button
    st.success("✅ Analysis Complete. You can now send your data to Richard Parslow.")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown(f"### Results")
        st.write(f"**BMI:** {bmi:.1f}")
        st.markdown(f'<div class="class-badge" style="background: {badge_color};">{hClass}</div>', unsafe_allow_html=True)
    
    with col_res2:
        st.markdown("### Eligibility")
        if cRank <= 4: st.write("✅ Term / IUL / Whole Life Eligible")
        elif cRank == 5: st.write("⚠️ Substandard Markets Only")
        else: st.write("🚫 Guaranteed Issue (GI) ONLY")

    # Email Logic
    subject = f"Health Analysis Request: {name}"
    body = f"Name: {name}%0ADOB: {dob}%0ABMI: {bmi:.1f}%0AClass: {hClass}%0AOccupation: {occ}%0AMedications: {meds}"
    mailto_link = f"mailto:richardparslow@lifepolicypilot.blog?subject={subject}&body={body}"
    
    st.markdown(f"""
        <a href="{mailto_link}" style="text-decoration: none;">
            <div style="background-color: {PRIMARY_RED}; color: white; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold;">
                Email Results to richardparslow@lifepolicypilot.blog
            </div>
        </a>
    """, unsafe_allow_html=True)
