import streamlit as st
import pandas as pd
import numpy as np

# -------------------- CONFIGURATION --------------------
st.set_page_config(page_title="🎯 Prédiction des Ventes", layout="wide")
st.title("📊 Application de Prédiction des Ventes et Quantités")

# -------------------- DONNÉES DE BASE --------------------
category_options = ['Furniture', 'Office Supplies', 'Technology']
subcategory_options = [
    'Bookcases', 'Chairs', 'Tables', 'Appliances', 'Binders', 'Paper', 'Phones',
    'Storage', 'Art', 'Accessories', 'Copiers', 'Machines', 'Envelopes',
    'Fasteners', 'Labels', 'Furnishings', 'Supplies'
]
region_options = ['East', 'West', 'Central', 'South']

# -------------------- PARTIE 1 : CHOIX TEMPOREL --------------------
st.markdown("### 🧠 Partie 1 : Choix du type de prédiction temporelle")
temp_choice = st.selectbox("Niveau de granularité temporelle :", ["Année", "Année + Mois", "Jour complet"])

order_year = order_month = order_week = order_day = None

if temp_choice == "Année":
    order_year = st.selectbox("Année", list(range(2018, 2027)))
elif temp_choice == "Année + Mois":
    col1, col2 = st.columns(2)
    with col1:
        order_year = st.selectbox("Année", list(range(2018, 2027)))
    with col2:
        order_month = st.slider("Mois", 1, 12, 6)
elif temp_choice == "Jour complet":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        order_year = st.selectbox("Année", list(range(2018, 2027)))
    with col2:
        order_month = st.slider("Mois", 1, 12, 6)
    with col3:
        order_week = st.slider("Semaine", 1, 52, 26)
    with col4:
        order_day = st.slider("Jour de semaine", 0, 6, 0)

# -------------------- PARTIE 2 : TYPE DE PRODUIT --------------------
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

# -------------------- INFORMATIONS COMPLÉMENTAIRES --------------------
st.markdown("### 📌 Informations complémentaires")
col1, col2, col3 = st.columns(3)

with col1:
    is_holiday = st.selectbox("Jour férié ?", ["Non", "Oui"]) == "Oui"
with col2:
    is_holiday_season = st.selectbox("Saison des fêtes ?", ["Non", "Oui"]) == "Oui"
with col3:
    delivery_duration = st.number_input("Durée de livraison (jours)", min_value=0, step=1)

# -------------------- SIMULATION LOGIQUE --------------------
def simulate_sales_quantity(category, subcategory, temp_choice, product_choice):
    expensive_subcategories = ['Copiers', 'Phones', 'Machines']
    
    if subcategory:
        if subcategory in expensive_subcategories:
            price = np.random.uniform(500, 2000)
            quantity = np.random.randint(1, 5)
        else:
            price = np.random.uniform(20, 200)
            quantity = np.random.randint(1, 10)
    elif category:
        if category == 'Technology':
            price = np.random.uniform(300, 1500)
            quantity = np.random.randint(1, 6)
        elif category == 'Furniture':
            price = np.random.uniform(100, 800)
            quantity = np.random.randint(1, 8)
        else:
            price = np.random.uniform(10, 200)
            quantity = np.random.randint(1, 12)
    else:
        price = np.random.uniform(10, 2000)
        quantity = np.random.randint(1, 12)

    base_sales = price * quantity

    # Ajustement temporel
    if temp_choice == "Année":
        base_sales *= np.random.uniform(30, 60)
        quantity *= np.random.randint(20, 60)
    elif temp_choice == "Année + Mois":
        base_sales *= np.random.uniform(4, 8)
        quantity *= np.random.randint(3, 8)

    # Ajustement produit
    if product_choice == "Par catégorie":
        base_sales *= 1.5
        quantity *= 1.3
    elif product_choice == "Tous les produits":
        base_sales *= 2
        quantity *= 1.5

    return round(base_sales, 2), int(quantity)

# -------------------- BOUTON PREDICTION --------------------
if st.button("📈 Prédire les Ventes et Quantités"):
    sales, quantity = simulate_sales_quantity(category, subcategory, temp_choice, product_choice)

    st.success("✅ Prédictions simulées avec succès !")

    st.markdown(f"""
    ### Résultats de la simulation :
    - **Vente estimée** 💰 : `{sales} €`
    - **Quantité estimée** 📦 : `{quantity}`
    """)
