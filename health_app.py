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
    .status-box {{ background-color: {SILVER_GRAY}; padding: 20px; border-radius: 12px; border-left: 8px solid {PRIMARY_RED}; }}
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.title("🩺 Health Class Predictor")
st.subheader("Step 2: Assessing Visibility")
st.info("This tool provides an objective simulation of potential underwriting classes based on standard carrier guidelines. It is not a final offer or a guarantee of coverage.")

# 3. Inputs
col_in, col_out = st.columns([1, 1.2], gap="large")

with col_in:
    st.markdown("### 🧬 Health Indicators")
    tobacco = st.radio("Tobacco or Nicotine Use (Last 12 Months)", ["None", "Occasional/Social", "Current User"])
    
    col_h, col_w = st.columns(2)
    with col_h:
        height = st.number_input("Height (Inches)", value=70)
    with col_w:
        weight = st.number_input("Weight (lbs)", value=180)
    
    st.markdown("---")
    st.markdown("### 💓 Vitals")
    systolic = st.slider("Systolic Blood Pressure (Top Number)", 100, 160, 120)
    history = st.checkbox("History of chronic conditions (e.g., Diabetes, Heart Disease)")

# 4. Logic (Simplified Carrier Simulation)
bmi = (weight / (height ** 2)) * 703

if tobacco == "Current User" or history or bmi > 32 or systolic > 140:
    predicted_class = "Standard"
    color = "#FFA500" # Orange for caution
elif tobacco == "Occasional/Social" or bmi > 28 or systolic > 130:
    predicted_class = "Preferred"
    color = PRIMARY_RED
else:
    predicted_class = "Preferred Plus"
    color = "#228B22" # Forest Green for clear skies

# 5. Results Dashboard
with col_out:
    st.markdown("### 📊 Estimated Flight Category")
    st.markdown(f"""
        <div class="status-box">
            <h2 style="color: {color} !important; margin-bottom: 5px;">{predicted_class}</h2>
            <p><strong>Calculated BMI:</strong> {bmi:.1f}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("#### What this means for your Flight Plan:")
    if predicted_class == "Preferred Plus":
        st.write("You likely qualify for the most aggressive carrier pricing available in the current market.")
    elif predicted_class == "Preferred":
        st.write("Your profile is strong, though minor factors place you in a standard-competitive tier.")
    else:
        st.write("Current indicators suggest a standard rating class. Professional advocacy is required to match you with a carrier that favors your specific profile.")

    st.divider()
    st.link_button("Request Full Pre-Flight Consultation", "https://lifepolicypilot.blog/contact-2/")

# 6. Disclaimer
st.caption("Note: This simulation is based on anonymized data and the D.I.M.E. logic of objective analysis. Final rating classes are determined exclusively by carrier underwriters following a full medical review.")
