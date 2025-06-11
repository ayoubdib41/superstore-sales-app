import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# Charger le pipeline
with open("quantity_pipeline.pkl", "rb") as file:
    model = pickle.load(file)

st.set_page_config(page_title="Prédiction des quantités de vente", layout="centered", page_icon="📈")
st.title("📦 Prédiction des quantités de vente")

# Partie 1 : Choix temporel
st.header("1️⃣ Choix du type de prédiction temporelle")
time_option = st.selectbox("Choisir la granularité temporelle", ["Année", "Mois dans une année"])

if time_option == "Année":
    year = st.selectbox("Année", [2017, 2018, 2019, 2020])
elif time_option == "Mois dans une année":
    year = st.selectbox("Année", [2017, 2018, 2019, 2020])
    month = st.selectbox("Mois", list(range(1, 13)))

# Partie 2 : Type de produit
st.header("2️⃣ Type de produit")
product_filter = st.radio("Filtrer par :", ["Tous les produits", "Catégorie", "Sous-catégorie"])

# Valeurs par défaut pour l'encodage
categories = ['Furniture', 'Office Supplies', 'Technology']
sub_categories = ['Chairs', 'Phones', 'Binders', 'Paper', 'Accessories']

if product_filter == "Catégorie":
    category = st.selectbox("Choisir une catégorie", categories)
elif product_filter == "Sous-catégorie":
    sub_category = st.selectbox("Choisir une sous-catégorie", sub_categories)

# Bouton prédiction
if st.button("Prédire la quantité vendue"):
    # Construction du DataFrame
    data = {
        'Year': [year],
        'Category': [category if product_filter == "Catégorie" else 'Unknown'],
        'Sub-Category': [sub_category if product_filter == "Sous-catégorie" else 'Unknown'],
        'Month': [month if time_option == "Mois dans une année" else 0]
    }
    input_df = pd.DataFrame(data)

    # Prédiction
    prediction = model.predict(input_df)[0]
    st.success(f"✅ Quantité prédite : {int(prediction)} unités")