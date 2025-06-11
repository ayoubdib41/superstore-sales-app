import streamlit as st
import pandas as pd
import joblib

st.title("📊 Application de prédiction des ventes - Superstore")

model = joblib.load("xgboost_model.pkl")
columns = joblib.load("columns_reference.pkl")

st.subheader("Entrez les informations pour prédire la vente :")
year = st.number_input("Année de commande", min_value=2014, max_value=2020, step=1)
month = st.selectbox("Mois de commande", list(range(1, 13)))
quantity = st.slider("Quantité commandée", 1, 100)
discount = st.slider("Remise (%)", 0, 100) / 100
profit = st.number_input("Profit estimé")

category = st.selectbox("Catégorie", ["Furniture", "Office Supplies", "Technology"])
sub_category = st.selectbox("Sous-catégorie", ["Chairs", "Tables", "Bookcases", "Phones", "Binders", "Accessories", "Copiers", "Appliances", "Storage", "Art", "Envelopes", "Paper", "Fasteners", "Supplies", "Labels", "Furnishings"])
region = st.selectbox("Région", ["East", "West", "Central", "South"])
segment = st.selectbox("Segment", ["Consumer", "Corporate", "Home Office"])
ship_mode = st.selectbox("Mode de livraison", ["Second Class", "Standard Class", "First Class", "Same Day"])

input_df = pd.DataFrame([{
    "Order_Year": year,
    "Order_Month": month,
    "Quantity": quantity,
    "Discount": discount,
    "Profit": profit,
    "Category": category,
    "Sub-Category": sub_category,
    "Region": region,
    "Segment": segment,
    "Ship Mode": ship_mode
}])

if st.button("🔮 Prédire les ventes"):
    prediction = model.predict(input_df)
    st.success(f"🛒 Vente prévue : {prediction[0]:.2f} $")
