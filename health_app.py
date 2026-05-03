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
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ height: 45px; background-color: {SILVER_GRAY}; border-radius: 4px; padding: 10px; font-weight: bold; }}
    .stTabs [aria-selected="true"] {{ background-color: {PRIMARY_RED}; color: white; }}
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.title("🩺 Health Class Predictor")
st.info("Providing these details empowers our team to conduct a precise pre-underwriting analysis, ensuring we match you with the right carrier.") [cite: 76]

# 3. Form Organization (Tabs)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👤 Identity", "⚖️ Physical & Habits", "🏥 Medical History", 
    "🚵 Lifestyle & Risk", "🛡️ Policy Needs", "👨‍⚕️ Physicians"
])

# --- TAB 1: IDENTITY & CONTACT ---
with tab1:
    st.subheader("Personal Information")
    name = st.text_input("Full Name (Include maiden name in parentheses)") [cite: 80]
    col_bio1, col_bio2 = st.columns(2)
    with col_bio1:
        sex = st.radio("Sex", ["Male", "Female", "Other"]) [cite: 87]
        dob = st.text_input("Date of Birth (mm/dd/yyyy)") [cite: 92]
    with col_bio2:
        marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed", "Separated"]) [cite: 335]
        citizen = st.radio("U.S. Citizen?", ["Yes", "No"]) [cite: 333]
    
    st.markdown("---")
    email = st.text_input("Email Address") [cite: 95]
    phone = st.text_input("Phone Numbers (home, mobile, work)") [cite: 98, 99]
    address = st.text_area("Home Address & Duration") [cite: 313, 315]

# --- TAB 2: PHYSICAL & HABITS ---
with tab2:
    st.subheader("Physical Specs")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        height = st.number_input("Height (inches)", value=70) [cite: 318]
    with col_p2:
        weight = st.number_input("Weight (pounds)", value=180) [cite: 321]
    
    st.markdown("---")
    st.subheader("Habits & Substances")
    tobacco = st.radio("Have you ever used tobacco or nicotine products in any form?", ["Yes", "No"]) [cite: 325]
    alcohol = st.radio("Consumed alcoholic beverages?", ["Yes", "No"]) [cite: 197]
    if alcohol == "Yes":
        st.checkbox("Been advised to limit/cease alcohol or sought treatment?") [cite: 202, 206, 212]
    
    marijuana = st.radio("Used marijuana in the past 5 years?", ["Yes", "No"]) [cite: 239]
    if marijuana == "Yes":
        st.text_area("Purpose, delivery method, and frequency") [cite: 246]
        
    controlled = st.radio("Ever used controlled substances or illegal drugs (cocaine, heroin, etc.)?", ["Yes", "No"]) [cite: 106, 248]

# --- TAB 3: MEDICAL HISTORY ---
with tab3:
    st.subheader("Diagnostic History")
    st.checkbox("Had an electrocardiogram, x-ray, blood test, or other diagnostic test?") [cite: 133]
    st.checkbox("Been advised to have surgery, biopsy, or testing not yet completed?") [cite: 184]
    st.checkbox("Tested positive for HIV, ARC, or AIDS?") [cite: 220]
    
    st.markdown("---")
    st.subheader("Condition Screening")
    st.write("Have you ever been treated for or diagnosed with disorders of the following:")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.checkbox("Respiratory System (Asthma, COPD, Sleep Apnea)") [cite: 101]
        st.checkbox("Cancer, Tumor, or Melanoma") [cite: 111]
        st.checkbox("Kidney or Bladder") [cite: 114]
        st.checkbox("Mental/Emotional (Depression, Anxiety, Bipolar)") [cite: 125]
        st.checkbox("Digestive System (Hepatitis, GERD, Ulcers)") [cite: 137]
        st.checkbox("Blood or Immune System") [cite: 143]
        st.checkbox("Diabetes or Thyroid") [cite: 147]
    with col_m2:
        st.checkbox("Reproductive System (Prostate, Uterus, Breasts)") [cite: 151, 155]
        st.checkbox("Pregnancy/Infertility") [cite: 158]
        st.checkbox("Nervous System (Stroke, MS, Seizures)") [cite: 166]
        st.checkbox("Bones, Skin, or Muscles (Arthritis)") [cite: 169]
        st.checkbox("Eyes, Ears, Nose, or Throat") [cite: 175]
        st.checkbox("Heart or Blood Vessels (BP, Cholesterol)") [cite: 283, 426]
    
    st.markdown("---")
    st.text_area("Current Medications, Supplements, or Remedies (Name, dosage, condition)") [cite: 229, 307]

# --- TAB 4: LIFESTYLE & RISK ---
with tab4:
    st.subheader("Activities & Employment")
    occ = st.text_input("Occupation") [cite: 104]
    income = st.number_input("Annual Income", value=0) [cite: 235]
    st.checkbox("Currently a member of the armed forces or reserves?") [cite: 272]
    
    st.markdown("---")
    st.subheader("Hazardous Activities")
    st.checkbox("Engage in high-risk hobbies (Sky diving, racing, mountain climbing, etc.)?") [cite: 371]
    st.checkbox("Hold a current pilot license or flown in the past 5 years?") [cite: 375]
    st.checkbox("Intend to travel outside the U.S. or Canada in next 12 months?") [cite: 344]
    
    st.markdown("---")
    st.subheader("Background")
    st.checkbox("Convicted of a criminal offense or currently on parole?") [cite: 278]
    st.checkbox("Filed for bankruptcy or had charge off of bad debts in last 5 years?") [cite: 381]
    st.text_area("Exercise Routine (Type, frequency, time)") [cite: 304]

# --- TAB 5: POLICY NEEDS & FAMILY ---
with tab5:
    st.subheader("Insurance Strategy")
    coverage_type = st.multiselect("Preferred Coverage Type", ["Term Life", "Whole Life", "Universal Life", "Variable Life", "Guaranteed Issue"]) [cite: 354]
    purpose = st.text_area("Primary purpose for this insurance (Income replacement, estate, etc.)") [cite: 364]
    amount = st.number_input("Desired Coverage Amount", value=500000) [cite: 367]
    st.text_area("How was the need for this face amount determined?") [cite: 369]
    
    st.markdown("---")
    st.subheader("Family Medical History")
    st.checkbox("Family members diagnosed with heart disease, stroke, diabetes, or cancer prior to age 60?") [cite: 299]
    st.text_area("Current status of parents and siblings (Ages, cause of death)") [cite: 310, 311]

# --- TAB 6: PHYSICIANS ---
with tab6:
    st.subheader("Medical Support Team")
    st.markdown("#### Primary Physician")
    st.text_input("Primary Physician Name") [cite: 389]
    st.text_input("Telephone & Address") [cite: 394, 397]
    st.text_area("Reason last seen and results of visit") [cite: 392]
    
    st.markdown("---")
    st.markdown("#### Last Consulted Physician")
    st.text_input("Specialty & Address") [cite: 385, 387]
    st.text_input("Date last seen") [cite: 405]
    st.text_area("Reason last seen and results (Last Consulted)") [cite: 408]

st.divider()
st.button("Submit Analysis Request") [cite: 435]
st.caption("Note: This response is secure and confidential. Final underwriting results depend on carrier-specific review.") [cite: 432]
