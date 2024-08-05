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
    prediction = model.predict(input_array)
    return prediction[0]

# Streamlit app
st.title("Diabetes Prediction App")
st.write("This app predicts diabetes risk based on user input.")

# Define the questionnaire for input data
Sex = st.selectbox("Sex (0=Female, 1=Male)", (0, 1))
Age = st.selectbox("Age (1 = 18-24, 2 = 25-29, 3 = 30-34, 4 = 35-39, 5 = 40-44, 6 = 45-49, 7 = 50-54, 8 = 55-59, 9 = 60-64, 10 = 65-69, 11 = 70-74, 12 = 75-79, 13 = Over 80 Years)", 
                   options=list(range(1, 14)))  
Education = st.selectbox("Education level (1 = Never attended school or only kindergarten, 2 = Elementary, 3 = Some High school, 4 = High school graduate, 5 = Some college, 6 = College graduate)", 
                         options=list(range(1, 7)))  
Income = st.selectbox("Income level (1 = Less than $10000, 2 = $10000-15000, 3 = $15000-20000, 4 = $20000-25000, 5 = $25000-35000, 6 = $35000-50000, 7 = $50000-75000, 8 = Over $75000)", 
                      options=list(range(1, 9)))  
HighBP = st.selectbox("Do you have high blood pressure?(0 = No,1 = Yes)", (0, 1))
HighChol = st.selectbox("Do you have high cholesterol?(0 = No,1 = Yes)", (0, 1))
CholCheck = st.selectbox("Have you had your cholesterol checked?(0 = No,1 = Yes)", (0, 1))
BMI = st.slider("What is your BMI?", 10, 50)
HealthScore = st.slider("What is your healthscore?", 1, 22)
Smoker = st.selectbox("Are you a smoker?(0 = No,1 = Yes)", (0, 1))
Stroke = st.selectbox("Have you had a stroke?(0 = No,1 = Yes)", (0, 1))
HeartDiseaseorAttack = st.selectbox("Have you had heart disease or attack?(0 = No,1 = Yes)", (0, 1))
HvyAlcoholConsump = st.selectbox("Do you consume heavy amounts of alcohol?(0 = No,1 = Yes)", (0, 1))
AnyHealthcare = st.selectbox("Do you have any healthcare coverage?(0 = No,1 = Yes)", (0, 1))
NoDocbcCost = st.selectbox("Have you been unable to see a doctor because of cost?(0 = No,1 = Yes)", (0, 1))
DiffWalk = st.selectbox("Do you have difficulty walking?", (0, 1))
GenHlth = st.slider("How is your general health? (1=Excellent, 5=Poor)", 1, 5)
MentHlth = st.slider("Number of days with poor mental health in the past month", 0, 30)
PhysHlth = st.slider("Number of days with poor physical health in the past month", 0, 30)

# Collect the input data
input_data = [HighBP, HighChol, CholCheck, BMI, HealthScore, Smoker, Stroke, HeartDiseaseorAttack, HvyAlcoholConsump, AnyHealthcare, NoDocbcCost, DiffWalk, GenHlth, MentHlth, PhysHlth, Sex, Age, Education, Income]

# Predict diabetes risk
if st.button("Submit Results"):
    prediction = predict_diabetes(input_data)
    st.write(f"Prediction: {'Diabetes' if prediction == 1 else 'No Diabetes'}")
