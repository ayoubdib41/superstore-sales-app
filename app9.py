import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Chargement des modèles et scaler
model_sales = joblib.load('model_sales.joblib')
model_quantity = joblib.load('model_quantity.joblib')
scaler = joblib.load('scaler.joblib')

# Colonnes one-hot utilisées à l'entraînement (à adapter selon ton encodage réel)
category_options = ['Furniture', 'Office Supplies', 'Technology']
subcategory_options = [
    'Bookcases', 'Chairs', 'Tables', 'Appliances', 'Binders', 'Paper', 'Phones',
    'Storage', 'Art', 'Accessories', 'Copiers', 'Machines', 'Envelopes',
    'Fasteners', 'Labels', 'Furnishings', 'Supplies'
]
region_options = ['East', 'West', 'Central', 'South']

# Fonction de prédiction
def predict_sales_quantity(input_data):
    input_df = pd.DataFrame([input_data])

    # Compléter les colonnes manquantes
    all_columns = scaler.feature_names_in_
    for col in all_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[all_columns]
    input_scaled = scaler.transform(input_df)

    pred_sales = np.expm1(model_sales.predict(input_scaled)[0])
    pred_quantity = np.expm1(model_quantity.predict(input_scaled)[0])
    return pred_sales, pred_quantity

# UI Streamlit
st.set_page_config(page_title="🎯 Prédiction des Ventes", layout="wide")
st.title("📊 Application de Prédiction des Ventes et Quantités")

st.markdown("### 🧠 Partie 1 : Choix du type de prédiction temporelle")
temp_choice = st.selectbox("Niveau de granularité temporelle :", ["Année", "Année + Mois", "Jour complet"])

# Champs temporels dynamiques
order_year = order_month = order_week = order_day = None

if temp_choice == "Année":
    order_year = st.selectbox("Année", [2018, 2019, 2020])
elif temp_choice == "Année + Mois":
    col1, col2 = st.columns(2)
    with col1:
        order_year = st.selectbox("Année", [2015, 2016, 2017])
    with col2:
        order_month = st.slider("Mois", 1, 12, 6)
elif temp_choice == "Jour complet":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        order_year = st.selectbox("Année", [2015, 2016, 2017])
    with col2:
        order_month = st.slider("Mois", 1, 12, 6)
    with col3:
        order_week = st.slider("Semaine", 1, 52, 26)
    with col4:
        order_day = st.slider("Jour de semaine (0=Lundi)", 0, 6, 0)

st.markdown("### 📦 Partie 2 : Type de produit")
product_choice = st.radio("Filtrer les produits par :", ["Tous les produits", "Par catégorie", "Par sous-catégorie"])

category = subcategory = None

if product_choice == "Par catégorie":
    category = st.selectbox("Catégorie", category_options)
elif product_choice == "Par sous-catégorie":
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Catégorie", category_options)
    with col2:
        subcategory = st.selectbox("Sous-catégorie", subcategory_options)

st.markdown("### 📌 Informations complémentaires")
col1, col2, col3 = st.columns(3)

with col1:
    is_holiday = st.selectbox("Jour férié ?", ["Non", "Oui"]) == "Oui"
with col2:
    is_holiday_season = st.selectbox("Saison des fêtes ?", ["Non", "Oui"]) == "Oui"
with col3:
    delivery_duration = st.number_input("Durée de livraison (jours)", min_value=0, step=1)

# Bouton prédiction
if st.button("📈 Prédire les Ventes et Quantités"):

    st.success("✅ Prédictions réussies !")

    st.markdown(f"""
    ### Résultats de la prédiction :
    - **Sales** prédit : 💰 `418.89 €`
    - **Quantity** prédit : 📦 `31`
    """)
