import streamlit as st  # type: ignore[import]
import pandas as pd  # type: ignore[import]
import pickle
import os

# Load model and columns
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "model.pkl")
columns_path = os.path.join(base_dir, "model_columns.pkl")

with open(model_path, "rb") as model_file:
    model = pickle.load(model_file)
with open(columns_path, "rb") as columns_file:
    model_columns = pickle.load(columns_file)

st.title("Luxury Watch Price Estimator")
st.write("Enter watch details below to get a predicted market value.")

# Input fields
brand = st.selectbox("Brand", ["Rolex", "Omega", "Tag Heuer", "Breitling", "Cartier", 
                                "Audemars Piguet", "Patek Philippe", "IWC", "Hublot", "Panerai"])

model_name = st.selectbox("Model", ["Submariner", "Seamaster", "Carrera", "Navitimer", 
                                     "Tank Solo", "Royal Oak", "Nautilus", "Portugieser", 
                                     "Big Bang", "Luminor"])

case_material = st.selectbox("Case Material", ["Stainless Steel", "Gold", "Titanium", "Ceramic", "Platinum"])

strap_material = st.selectbox("Strap Material", ["Leather", "Rubber", "Stainless Steel", "Titanium"])

movement_type = st.selectbox("Movement Type", ["Automatic", "Manual", "Quartz"])

dial_color = st.selectbox("Dial Color", ["Black", "White", "Blue", "Silver", "Green"])

crystal_material = st.selectbox("Crystal Material", ["Sapphire", "Mineral", "Acrylic"])

complications = st.selectbox("Complications", ["None", "Date", "Chronograph", "GMT", "Moonphase"])

water_resistance = st.slider("Water Resistance (meters)", 30, 600, 100)
case_diameter = st.slider("Case Diameter (mm)", 28, 48, 40)
case_thickness = st.slider("Case Thickness (mm)", 5, 20, 12)
band_width = st.slider("Band Width (mm)", 16, 24, 20)
power_reserve = st.slider("Power Reserve (hours)", 38, 120, 48)

if st.button("Estimate Price"):
    # Build input row
    input_data = {
        "Water Resistance": water_resistance,
        "Case Diameter (mm)": case_diameter,
        "Case Thickness (mm)": case_thickness,
        "Band Width (mm)": band_width,
        "Power Reserve": power_reserve,
    }

    # Add all dummy columns as False
    for col in model_columns:
        if col not in input_data:
            input_data[col] = False

    # Set selected categories to True
    input_data[f"Brand_{brand}"] = True
    input_data[f"Model_{model_name}"] = True
    input_data[f"Case Material_{case_material}"] = True
    input_data[f"Strap Material_{strap_material}"] = True
    input_data[f"Movement Type_{movement_type}"] = True
    input_data[f"Dial Color_{dial_color}"] = True
    input_data[f"Crystal Material_{crystal_material}"] = True
    input_data[f"Complications_{complications}"] = True

    input_df = pd.DataFrame([input_data])[model_columns]
    prediction = model.predict(input_df)[0]

    st.success(f"Estimated Market Value: ${prediction:,.0f}")