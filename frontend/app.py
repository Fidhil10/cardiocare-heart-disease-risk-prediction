import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Constants
API_URL = "http://localhost:8001"

st.set_page_config(
    page_title="CardioCare ML",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for premium aesthetic
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stApp {
        background-color: #0f172a;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.4);
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #38bdf8;
    }
    .metric-card {
        background: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("❤️ CardioCare Intelligence Dashboard")
st.markdown("Advanced Machine Learning Platform for Early Cardiovascular Risk Detection")

tab1, tab2 = st.tabs(["🩺 New Prediction", "📊 Patient History & Analytics"])

with tab1:
    st.markdown("### Patient Vitals & Demographics")
    
    with st.form("predict_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            patient_name = st.text_input("Patient Name", placeholder="e.g., Jane Doe")
            age = st.number_input("Age (Years)", min_value=1, max_value=120, value=50)
            sex = st.selectbox("Sex", options=["M", "F"], help="Male (M), Female (F)")
            chest_pain = st.selectbox("Chest Pain Type", options=["TA", "ATA", "NAP", "ASY"], 
                                      help="TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal, ASY: Asymptomatic")

        with col2:
            resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, value=120)
            cholesterol = st.number_input("Serum Cholesterol (mg/dl)", min_value=0, max_value=600, value=200)
            fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1], help="1: Yes, 0: No")
            resting_ecg = st.selectbox("Resting ECG", options=["Normal", "ST", "LVH"])
            
        with col3:
            max_hr = st.number_input("Maximum Heart Rate", min_value=60, max_value=202, value=150)
            exercise_angina = st.selectbox("Exercise-Induced Angina", options=["Y", "N"])
            oldpeak = st.number_input("Oldpeak (ST Depression)", min_value=-5.0, max_value=10.0, value=0.0, step=0.1)
            st_slope = st.selectbox("ST Slope", options=["Up", "Flat", "Down"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Analyze Risk Profile")
        
    if submitted:
        if not patient_name:
            st.error("Please enter a patient name.")
        else:
            payload = {
                "patient_name": patient_name,
                "Age": age,
                "Sex": sex,
                "ChestPainType": chest_pain,
                "RestingBP": resting_bp,
                "Cholesterol": cholesterol,
                "FastingBS": fasting_bs,
                "RestingECG": resting_ecg,
                "MaxHR": max_hr,
                "ExerciseAngina": exercise_angina,
                "Oldpeak": oldpeak,
                "ST_Slope": st_slope
            }
            
            with st.spinner("Processing deep learning diagnostics..."):
                try:
                    response = requests.post(f"{API_URL}/predict", json=payload)
                    if response.status_code == 200:
                        result = response.json()["prediction"]
                        st.markdown("---")
                        if result == 1:
                            st.error("⚠️ HIGH RISK DETECTED: The model indicates a high probability of cardiovascular disease.")
                        else:
                            st.success("✅ LOW RISK: The model indicates a normal profile with no immediate signs of cardiovascular disease.")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Backend connection failed. Is the API running? {e}")

with tab2:
    st.markdown("### 📈 Patient Intelligence Analytics")
    try:
        res = requests.get(f"{API_URL}/history")
        if res.status_code == 200:
            history_data = res.json()
            if history_data:
                df = pd.DataFrame(history_data)
                df['Disease Status'] = df['PredictionResult'].map({1: 'Heart Disease', 0: 'Normal'})
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Assessments", len(df))
                col2.metric("High Risk Patients", len(df[df['PredictionResult'] == 1]))
                col3.metric("Normal Patients", len(df[df['PredictionResult'] == 0]))
                
                st.markdown("---")
                # Visualizations
                st.subheader("Population Demographics")
                viz_col1, viz_col2 = st.columns(2)
                with viz_col1:
                    fig_age = px.histogram(df, x="Age", color="Disease Status",
                                           title="Age Distribution vs Risk Profile",
                                           color_discrete_sequence=["#ef4444", "#22c55e"],
                                           template="plotly_dark")
                    fig_age.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_age, use_container_width=True)
                
                with viz_col2:
                    fig_chol = px.scatter(df, x="Age", y="Cholesterol", color="Disease Status",
                                          size="MaxHR", title="Cholesterol & Heart Rate Patterns",
                                          color_discrete_sequence=["#ef4444", "#22c55e"],
                                          template="plotly_dark")
                    fig_chol.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_chol, use_container_width=True)

                st.subheader("Comprehensive Registry")
                st.dataframe(df.drop(columns=['PredictionResult']), use_container_width=True)
            else:
                st.info("No patient history found. Please process a prediction first.")
        else:
            st.error("Could not fetch history data from backend.")
    except Exception as e:
        st.warning("Backend API is not reachable for fetching history.")
