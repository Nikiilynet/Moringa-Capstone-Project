import pickle
import streamlit as st
import numpy as np
import gdown
import os

# URL of your .pkl file in Google Drive
url = 'https://drive.google.com/uc?export=download&id=1TpTUM2yz_yvinPm1RNlhO5S3mW8mqJqI'

# Path to save the downloaded file
model_filename = 'diabetes_prediction_model.pkl'

# Function to download the model file
def download_model(url, model_filename):
    if not os.path.exists(model_filename):
        gdown.download(url, model_filename, quiet=False)

# Download the model file
download_model(url, model_filename)

# Load the pre-trained model
try:
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    st.error(f"Error loading model: {e}")

# Define a function to make predictions
def predict_diabetes(inputs):
    input_array = np.array(inputs).reshape(1, -1)
    probabilities = model.predict_proba(input_array)
    return probabilities[0]

# Streamlit app
st.title("Diabetes Prediction App")
st.write("This app predicts diabetes risk based on user input.")

# Define the questionnaire for input data
Sex = st.selectbox("Sex", ("Female", "Male"))
Age = st.selectbox("Age", [
    "18-24", "25-29", "30-34", "35-39", "40-44", 
    "45-49", "50-54", "55-59", "60-64", "65-69", 
    "70-74", "75-79", "Over 80 Years"
])
Education = st.selectbox("Education level", [
    "Never attended school or only kindergarten", "Elementary", 
    "Some High school", "High school graduate", 
    "Some college", "College graduate"
])
Income = st.selectbox("Income level", [
    "Less than $10000", "$10000-15000", "$15000-20000", "$20000-25000", 
    "$25000-35000", "$35000-50000", "$50000-75000", "Over $75000"
])
HighBP = st.selectbox("Do you have high blood pressure?", ("No", "Yes"))
HighChol = st.selectbox("Do you have high cholesterol?", ("No", "Yes"))
CholCheck = st.selectbox("Have you had your cholesterol checked?", ("No", "Yes"))
BMI = st.slider("What is your BMI?", 10, 50)
HealthScore = st.slider("What is your health score?", 1, 22)
Smoker = st.selectbox("Are you a smoker?", ("No", "Yes"))
Stroke = st.selectbox("Have you had a stroke?", ("No", "Yes"))
HeartDiseaseorAttack = st.selectbox("Have you had heart disease or attack?", ("No", "Yes"))
HvyAlcoholConsump = st.selectbox("Do you consume heavy amounts of alcohol?", ("No", "Yes"))
AnyHealthcare = st.selectbox("Do you have any healthcare coverage?", ("No", "Yes"))
NoDocbcCost = st.selectbox("Have you been unable to see a doctor because of cost?", ("No", "Yes"))
DiffWalk = st.selectbox("Do you have difficulty walking?", ("No", "Yes"))
GenHlth = st.slider("How is your general health?", 1, 5, format="%d (1=Excellent, 5=Poor)")
MentHlth = st.slider("Number of days with poor mental health in the past month", 0, 30)
PhysHlth = st.slider("Number of days with poor physical health in the past month", 0, 30)

# Mapping the descriptive text to binary values
Sex_binary = 0 if Sex == "Female" else 1
HighBP_binary = 0 if HighBP == "No" else 1
HighChol_binary = 0 if HighChol == "No" else 1
CholCheck_binary = 0 if CholCheck == "No" else 1
Smoker_binary = 0 if Smoker == "No" else 1
Stroke_binary = 0 if Stroke == "No" else 1
HeartDiseaseorAttack_binary = 0 if HeartDiseaseorAttack == "No" else 1
HvyAlcoholConsump_binary = 0 if HvyAlcoholConsump == "No" else 1
AnyHealthcare_binary = 0 if AnyHealthcare == "No" else 1
NoDocbcCost_binary = 0 if NoDocbcCost == "No" else 1
DiffWalk_binary = 0 if DiffWalk == "No" else 1

# Convert Age, Education, and Income to numerical values
Age_mapping = {
    "18-24": 1, "25-29": 2, "30-34": 3, "35-39": 4, "40-44": 5, 
    "45-49": 6, "50-54": 7, "55-59": 8, "60-64": 9, "65-69": 10, 
    "70-74": 11, "75-79": 12, "Over 80 Years": 13
}
Education_mapping = {
    "Never attended school or only kindergarten": 1, "Elementary": 2, 
    "Some High school": 3, "High school graduate": 4, 
    "Some college": 5, "College graduate": 6
}
Income_mapping = {
    "Less than $10000": 1, "$10000-15000": 2, "$15000-20000": 3, "$20000-25000": 4, 
    "$25000-35000": 5, "$35000-50000": 6, "$50000-75000": 7, "Over $75000": 8
}

Age_binary = Age_mapping[Age]
Education_binary = Education_mapping[Education]
Income_binary = Income_mapping[Income]

# Collect the input data
input_data = [
    Sex_binary, Age_binary, Education_binary, Income_binary, HighBP_binary, HighChol_binary, CholCheck_binary, 
    BMI, HealthScore, Smoker_binary, Stroke_binary, HeartDiseaseorAttack_binary, HvyAlcoholConsump_binary, 
    AnyHealthcare_binary, NoDocbcCost_binary, DiffWalk_binary, GenHlth, MentHlth, PhysHlth
]

# Predict diabetes risk
if st.button("Submit Results"):
    probabilities = predict_diabetes(input_data)
    classes = ["No Diabetes", "Prediabetes", "Diabetes"]
    st.write("Prediction Probabilities:")
    for i, class_name in enumerate(classes):
        st.write(f"{class_name}: {probabilities[i] * 100:.2f}%")
