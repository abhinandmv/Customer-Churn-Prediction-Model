import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Churn Predictor", page_icon="📡", layout="wide")

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace !important;
    background-color: #080c14 !important;
    color: #e2e8f0 !important;
}

.stApp {
    background: #080c14;
    background-image:
        linear-gradient(rgba(0,212,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.025) 1px, transparent 1px);
    background-size: 48px 48px;
}

/* ── Hide Streamlit default chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
    animation: fadeDown 0.7s ease both;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 999px;
    padding: 5px 18px;
    font-size: 11px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #00d4ff;
    margin-bottom: 18px;
}
.hero-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00d4ff;
    box-shadow: 0 0 8px #00d4ff;
    animation: pulse 2s infinite;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2rem, 4vw, 3rem) !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
}
.hero p {
    color: #64748b;
    font-size: 14px;
    letter-spacing: 0.02em;
}

/* ── Section cards ── */
.section-card {
    background: #0e1520;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 24px 24px 8px;
    margin-bottom: 20px;
    transition: border-color 0.3s;
    animation: fadeUp 0.6s ease both;
}
.section-card:hover { border-color: rgba(0,212,255,0.15); }

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #00d4ff;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(0,212,255,0.3), transparent);
}

/* ── Labels ── */
.stSelectbox label, .stNumberInput label, .stTextInput label {
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #64748b !important;
    font-weight: 500 !important;
    margin-bottom: 4px !important;
}

/* ── Inputs & Selects ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #141d2e !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.12) !important;
}
.stSelectbox svg { color: #64748b !important; }

/* ── Predict button ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #080c14 !important;
    background: linear-gradient(135deg, #00d4ff 0%, #0098c7 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 0 !important;
    width: 100% !important;
    cursor: pointer !important;
    box-shadow: 0 0 28px rgba(0,212,255,0.3) !important;
    transition: all 0.2s !important;
    margin-top: 8px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 44px rgba(0,212,255,0.5) !important;
}

/* ── Result cards ── */
.result-churn {
    background: linear-gradient(135deg, rgba(248,113,113,0.07) 0%, #0e1520 100%);
    border: 1px solid rgba(248,113,113,0.35);
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    animation: fadeUp 0.5s ease both;
    margin-top: 24px;
}
.result-safe {
    background: linear-gradient(135deg, rgba(52,211,153,0.07) 0%, #0e1520 100%);
    border: 1px solid rgba(52,211,153,0.35);
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    animation: fadeUp 0.5s ease both;
    margin-top: 24px;
}
.result-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #64748b;
    margin-bottom: 10px;
}
.result-verdict-churn {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    color: #f87171;
    letter-spacing: -0.02em;
}
.result-verdict-safe {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    color: #34d399;
    letter-spacing: -0.02em;
}
.result-sub {
    font-size: 13px;
    color: #64748b;
    margin-top: 6px;
}
.prob-label {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 20px;
    margin-bottom: 6px;
}
.prob-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
}
.prob-number-churn { color: #f87171; }
.prob-number-safe  { color: #34d399; }

/* ── Progress bar ── */
.stProgress > div > div > div {
    border-radius: 999px !important;
    height: 8px !important;
}
.stProgress > div > div {
    background: #141d2e !important;
    border-radius: 999px !important;
    height: 8px !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── Animations ── */
@keyframes fadeDown {
    from { opacity:0; transform:translateY(-20px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes pulse {
    0%,100% { opacity:1; }
    50%      { opacity:0.3; }
}
</style>
""", unsafe_allow_html=True)


# ── Load models ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    with open("best_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("encoder.pkl", "rb") as f:
        encoders = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, encoders, scaler

model, encoders, scaler = load_models()


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge"><span class="dot"></span> ML Prediction Engine</div>
  <h1>Customer Churn Predictor</h1>
  <p>Fill in customer details below to generate a real-time churn prediction.</p>
</div>
""", unsafe_allow_html=True)


# ── Section 1: Demographics ────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">01 — Demographics</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
gender    = c1.selectbox("Gender",          ["Male", "Female"])
senior    = c2.selectbox("Senior Citizen",  [0, 1], format_func=lambda x: "Yes" if x else "No")
partner   = c3.selectbox("Partner",         ["Yes", "No"])
dependents= c4.selectbox("Dependents",      ["Yes", "No"])
tenure    = c5.number_input("Tenure (months)", min_value=0, step=1)
st.markdown('</div>', unsafe_allow_html=True)


# ── Section 2: Phone & Internet ────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">02 — Phone & Internet Services</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
phone       = c1.selectbox("Phone Service",   ["Yes", "No"])
multi_lines = c2.selectbox("Multiple Lines",  ["Yes", "No", "No phone service"])
internet    = c3.selectbox("Internet Service",["DSL", "Fiber optic", "No"])
st.markdown('</div>', unsafe_allow_html=True)


# ── Section 3: Add-ons ─────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">03 — Add-on Services</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
security = c1.selectbox("Online Security",    ["Yes", "No", "No internet service"])
backup   = c2.selectbox("Online Backup",      ["Yes", "No", "No internet service"])
device   = c3.selectbox("Device Protection",  ["Yes", "No", "No internet service"])
tech     = c4.selectbox("Tech Support",       ["Yes", "No", "No internet service"])
tv       = c5.selectbox("Streaming TV",       ["Yes", "No", "No internet service"])
movies   = c6.selectbox("Streaming Movies",   ["Yes", "No", "No internet service"])
st.markdown('</div>', unsafe_allow_html=True)


# ── Section 4: Billing ─────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">04 — Billing & Contract</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
contract   = c1.selectbox("Contract",          ["Month-to-month", "One year", "Two year"])
paperless  = c2.selectbox("Paperless Billing", ["Yes", "No"])
payment    = c3.selectbox("Payment Method",    ["Electronic check", "Mailed check",
                                                "Bank transfer (automatic)", "Credit card (automatic)"])
monthly    = c4.number_input("Monthly Charges ($)", min_value=0.0, step=0.01, format="%.2f")
total      = c5.number_input("Total Charges ($)",   min_value=0.0, step=0.01, format="%.2f")
st.markdown('</div>', unsafe_allow_html=True)


# ── Predict button ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict_clicked = st.button("🔍  Run Prediction", use_container_width=True)

if predict_clicked:
    input_data = {
        "gender": gender, "SeniorCitizen": senior, "Partner": partner,
        "Dependents": dependents, "tenure": tenure, "PhoneService": phone,
        "MultipleLines": multi_lines, "InternetService": internet,
        "OnlineSecurity": security, "OnlineBackup": backup,
        "DeviceProtection": device, "TechSupport": tech,
        "StreamingTV": tv, "StreamingMovies": movies,
        "Contract": contract, "PaperlessBilling": paperless,
        "PaymentMethod": payment, "MonthlyCharges": monthly,
        "TotalCharges": total
    }

    with st.spinner("Running model inference..."):
        df = pd.DataFrame([input_data])
        for col, enc in encoders.items():
            df[col] = enc.transform(df[col])
        df[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.transform(
            df[['tenure', 'MonthlyCharges', 'TotalCharges']]
        )
        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0, 1]

    # ── Result ─────────────────────────────────────────────────────────────────
    if pred == 1:
        st.markdown(f"""
        <div class="result-churn">
            <div class="result-label">Prediction Result</div>
            <div class="result-verdict-churn">⚠ Churn</div>
            <div class="result-sub">This customer is likely to leave</div>
            <div class="prob-label">Churn Probability</div>
            <div class="prob-number prob-number-churn">{prob*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(float(prob))
    else:
        st.markdown(f"""
        <div class="result-safe">
            <div class="result-label">Prediction Result</div>
            <div class="result-verdict-safe">✓ No Churn</div>
            <div class="result-sub">This customer is likely to stay</div>
            <div class="prob-label">Churn Probability</div>
            <div class="prob-number prob-number-safe">{prob*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(float(prob))