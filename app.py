import streamlit as st
import pandas as pd
import joblib

# Titre principal
st.title("📊 Application de prédiction des ventes - Superstore")

# Charger les modèles
model = joblib.load("xgboost_model.pkl")
scaler = joblib.load("scaler.pkl")

# Formulaire
st.subheader("🧾 Entrer les données :")

year = st.number_input("Année de commande", min_value=2015, max_value=2025, value=2018)
month = st.selectbox("Mois de commande", list(range(1, 13)))
quantity = st.slider("Quantité", 1, 100, 1)
discount = st.slider("Remise", 0.0, 1.0, 0.1)
profit = st.number_input("Profit estimé", value=100.0)

# Prédiction
if st.button("🔮 Prédire les ventes"):
    X = pd.DataFrame([[year, month, quantity, discount, profit]],
                     columns=["Order_Year", "Order_Month", "Quantity", "Discount", "Profit"])
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)
    st.success(f"🛒 Vente prévue : {prediction[0]:.2f} $")
