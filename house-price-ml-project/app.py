import streamlit as st
import pickle
import numpy as np

# load model
model = pickle.load(open("model.pkl", "rb"))

st.title("House Price Prediction")

# inputs
area = st.number_input("Area")
bedrooms = st.number_input("Bedrooms")
bathrooms = st.number_input("Bathrooms")
stories = st.number_input("Stories")
parking = st.number_input("Parking")

# binary inputs
mainroad = st.selectbox("Main Road", ["yes", "no"])
guestroom = st.selectbox("Guest Room", ["yes", "no"])
basement = st.selectbox("Basement", ["yes", "no"])
hotwaterheating = st.selectbox("Hot Water Heating", ["yes", "no"])
airconditioning = st.selectbox("Air Conditioning", ["yes", "no"])
prefarea = st.selectbox("Preferred Area", ["yes", "no"])

# furnishing
furnishing = st.selectbox(
    "Furnishing",
    ["furnished", "semi-furnished", "unfurnished"]
)

# convert yes/no → 1/0
mainroad = 1 if mainroad == "yes" else 0
guestroom = 1 if guestroom == "yes" else 0
basement = 1 if basement == "yes" else 0
hotwaterheating = 1 if hotwaterheating == "yes" else 0
airconditioning = 1 if airconditioning == "yes" else 0
prefarea = 1 if prefarea == "yes" else 0

# furnishing encoding
semi_furnished = 1 if furnishing == "semi-furnished" else 0
unfurnished = 1 if furnishing == "unfurnished" else 0

# prediction
if st.button("Predict"):
    input_data = np.array([[area, bedrooms, bathrooms, stories, parking,
                            mainroad, guestroom, basement, hotwaterheating,
                            airconditioning, prefarea,
                            semi_furnished, unfurnished]])

    prediction = model.predict(input_data)[0]

    st.write("Predicted Price:", int(prediction))