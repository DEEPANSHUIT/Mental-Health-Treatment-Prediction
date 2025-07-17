import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("mental_health_model_streamlit.pkl")

# Inject CSS
st.markdown("""
    <style>
    /* Set page background color */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Make all titles navy */
    .stApp h1, .stApp h2, .stApp h3 {
        color: #2c3e50;
        font-weight: 700;
    }

    /* Style buttons */
    div.stButton > button:first-child {
        background-color: #2c3e50;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
    }

    div.stButton > button:hover {
        background-color: #1a252f;
        color: white;
    }

    /* Style result boxes */
    .stAlert {
        border-radius: 0.5rem;
        padding: 1rem;
    }

    /* Style footer text */
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)


# App title
st.title("🧠 Mental Health Treatment Prediction")

st.markdown("Predict whether a person is likely to seek mental health treatment based on their responses.")

# User Inputs
age = st.slider("Age", 18, 100, 30)
gender = st.selectbox("Gender", ['Male', 'Female', 'Other'])
family_history = st.selectbox("Family history of mental illness?", ['Yes', 'No'])
self_employed = st.selectbox("Are you self-employed?", ['Yes', 'No'])
remote_work = st.selectbox("Do you work remotely?", ['Yes', 'No'])
tech_company = st.selectbox("Do you work in a tech company?", ['Yes', 'No'])
benefits = st.selectbox("Does your employer provide mental health benefits?", ['Yes', 'No', "Don't know"])
care_options = st.selectbox("Are you aware of care options at your workplace?", ['Yes', 'No', "Not sure"])
wellness_program = st.selectbox("Does your employer have a wellness program?", ['Yes', 'No', "Don't know"])
seek_help = st.selectbox("Does your company encourage seeking help?", ['Yes', 'No', "Don't know"])
anonymity = st.selectbox("Is anonymity protected when seeking help?", ['Yes', 'No', "Don't know"])
leave = st.selectbox("How easy is it to take mental health leave?", ['Very easy', 'Somewhat easy', 'Somewhat difficult', 'Very difficult', "Don't know"])
work_interfere = st.selectbox("Does your mental health interfere with work?", ['Never', 'Rarely', 'Sometimes', 'Often', "Don't know"])

# Encode Inputs
input_dict = {
    'Age': age,
    'Gender': {'Male': 1, 'Female': 0, 'Other': 2}[gender],
    'family_history': {'Yes': 1, 'No': 0}[family_history],
    'self_employed': {'Yes': 1, 'No': 0}[self_employed],
    'remote_work': {'Yes': 1, 'No': 0}[remote_work],
    'tech_company': {'Yes': 1, 'No': 0}[tech_company],
    'benefits': {'Yes': 1, 'No': 0, "Don't know": 2}[benefits],
    'care_options': {'Yes': 1, 'No': 0, "Not sure": 2}[care_options],
    'wellness_program': {'Yes': 1, 'No': 0, "Don't know": 2}[wellness_program],
    'seek_help': {'Yes': 1, 'No': 0, "Don't know": 2}[seek_help],
    'anonymity': {'Yes': 1, 'No': 0, "Don't know": 2}[anonymity],
    'leave': {'Very easy': 0, 'Somewhat easy': 1, 'Somewhat difficult': 2, 'Very difficult': 3, "Don't know": 4}[leave],
    'work_interfere': {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, "Don't know": 4}[work_interfere]
}

input_df = pd.DataFrame([input_dict])

# Predict
if st.button("Predict"):
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][prediction]

    if prediction == 1:
        st.success(f"✅ Likely to seek mental health treatment (Confidence: {prob*100:.1f}%)")
    else:
        st.info(f"🧠 Not likely to seek mental health treatment (Confidence: {prob*100:.1f}%)")

# Show visuals
st.markdown("---")
st.subheader("📊 Dataset Insights")

st.image("gender_distribution.png", caption="Gender Distribution in Dataset", use_container_width=True)
st.image("prediction_confidence.png", caption="Model Confidence (Probability of Treatment = 1)", use_container_width=True)
st.image("important_features.png", caption="Important features", use_container_width=True)

# Footer
st.markdown("""
<hr style='margin-top: 2rem; margin-bottom: 1rem;'>
<p style='text-align: center; color: grey;'>
Made with ❤️ for Mental Health Awareness · <a href="https://github.com/yourusername" target="_blank">GitHub</a>
</p>
""", unsafe_allow_html=True)
