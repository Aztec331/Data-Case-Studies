import streamlit as st
import pickle
import pandas as pd

# load model
model = pickle.load(open("model.pkl", "rb"))

# Title
st.title("House Price Prediction")

#-------------------------------------------------------
# Model comparison Graph
st.subheader("Model Comparison")

# errors from your notebook
lr_error = 970043
rf_error = 1018147

chart_data = {
    "Model": ["Linear Regression", "Random Forest"],
    "Error": [lr_error, rf_error]
}

st.bar_chart(chart_data, x="Model", y="Error")
#-------------------------------------------------------

st.subheader("Enter House Details")

# inputs
area = st.number_input("Area", min_value=0)
bedrooms = st.number_input("Bedrooms", min_value=0)
bathrooms = st.number_input("Bathrooms", min_value=0)
stories = st.number_input("Stories", min_value=0)
parking = st.number_input("Parking", min_value=0)

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

#-------------------------------------------------------
# CREATE INPUT DATA (GLOBAL VARIABLE)
input_data = pd.DataFrame([{
    "area": area,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "stories": stories,
    "mainroad": mainroad,
    "guestroom": guestroom,
    "basement": basement,
    "hotwaterheating": hotwaterheating,
    "airconditioning": airconditioning,
    "parking": parking,
    "prefarea": prefarea,
    "furnishingstatus_semi-furnished": semi_furnished,
    "furnishingstatus_unfurnished": unfurnished
}])
#-------------------------------------------------------

# Prediction
if st.button("Predict"):

    prediction = model.predict(input_data)[0]

    # Approx MAE from training (used for range estimation)
    error = lr_error

    lower = prediction - error
    upper = prediction + error

    st.write("---")

    st.success(f"Predicted Price: ₹{int(prediction)}")
    st.info(f"Estimated Range: ₹{int(lower)} - ₹{int(upper)}")


#-------------------------------------------------------
# What-if Analysis
st.write("---")
st.subheader("What-if Analysis (Area Impact)")

extra_area = st.slider("Increase Area", 0, 2000, 0)

if st.button("Check Impact"):

    new_area = area + extra_area

    input_data_whatif = input_data.copy()
    input_data_whatif["area"] = new_area

    new_prediction = model.predict(input_data_whatif)[0]

    st.write(f"New Area: {new_area}")
    st.success(f"New Predicted Price: ₹{int(new_prediction)}")
#-------------------------------------------------------