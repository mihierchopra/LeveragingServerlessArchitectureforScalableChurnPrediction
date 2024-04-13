import streamlit as st
import pandas as pd
import numpy as np
import pickle
import keras
import json
import os


def make_prediction(input_data):
    try:
        train_data = None
        with open('train.bin', 'rb') as file:
            train_data = pickle.load(file)

  
        json_model = train_data['ann']
        le = train_data['le']
        ct =  train_data['ct']
        sc =  train_data['sc']

        ann = keras.models.model_from_json(json_model)
        ann.load_weights("model.weights.h5")
        dataset=pd.json_normalize(input_data)
        X = dataset.values

        user_input = X[0]
        X_input = user_input.copy()

        X_input[2] = le.transform([X_input[2]])[0]
        X_input = ct.transform(X_input.reshape(1, -1))
        X_input = sc.transform(X_input)
        
        y_pred = ann.predict(X_input)


        return {
            'data': str(y_pred[0][0])
        }
    except Exception as e:
        st.error(f"Error occurred: {e}")
    

df = pd.read_csv("Churn_Modelling.csv")

unique_values = df['Geography'].unique()

st.title('Customer Churn Analysis')
col1, col2 = st.columns(2)

# Column 1
with col1:
    Geography = st.selectbox("Country", unique_values)
    Credit = st.number_input("Credit Score of the customer", value=None, placeholder="Type a number...")
    Gender = st.selectbox("Gender", ['Male', 'Female'])
    Age = st.number_input("Age of the customer", value=None, placeholder="Type a number...")
    Tenure = st.number_input("Tenure of the customer", value=None, placeholder="Type a number...")

# Column 2
with col2:
    Balance = st.number_input("Balance of the customer", value=None, placeholder="Type a number...")
    Products = st.number_input("Products of the customer", value=None, placeholder="Type a number...")
    Credits = st.selectbox("Does this Customer has the Credit Card?", ['Yes', 'No'])
    Active = st.selectbox("Is this customer an Active Member?", ['Yes', 'No'])
    Salary = st.number_input("Estimated Salary of the customer", value=None, placeholder="Type a number...")


card= 1 if Credits == 'Yes' else 0
ac= 1 if Active == 'Yes' else 0
#input = np.array([Credit,Geography,Gender,Age,Tenure,Balance,Products,card,ac,Salary])
input_data = {"Credit":Credit, "Geography": Geography,"Gender": Gender,"Age": Age,"Tenure": Tenure,"Balance":Balance,"Products":Products,"Credits":card,"Active":ac,"Salary":Salary}
if st.button('Predict Churn'):
        with st.spinner('Predicting...'):
                prediction = make_prediction(input_data)
        st.subheader("Prediction Result")
        
        churn=float(prediction['data'])

        if churn >0.5 :
                result=churn*100
                st.success(f"There is {result}% chance that the customer will leave the bank")
        else:
                result=(1-churn)*100
                st.success(f"There is {result}% chance  that customer will stay in the bank")
