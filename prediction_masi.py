import streamlit as st
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go

# ------------------------
# Fonction de scraping
# ------------------------
def get_latest_masi():
    try:
        url = "https://fr.investing.com/indices/masi"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers)

        if resp.status_code != 200:
            st.error("❌ Échec de la connexion à Investing.com")
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')
        masi_div = soup.find('div', {'data-test': 'instrument-price-last'})

        if masi_div and masi_div.text:
            raw_value = masi_div.text.strip()
            clean_value = raw_value.replace('.', '').replace(',', '.')
            return float(clean_value)

        st.error("❌ Valeur MASI introuvable sur la page.")
    except Exception as e:
        st.error(f"Erreur de récupération : {e}")
    return None

# ------------------------
# Mise à jour manuelle
# ------------------------
def update_history_manually(csv_path="masi_history_ready.csv"):
    masi = get_latest_masi()
    if masi is None:
        st.error("❌ Impossible de récupérer la valeur MASI.")
        return

    today = datetime.today().strftime('%Y-%m-%d')

    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Seance', 'MASI'])

    if 'Seance' not in df.columns or 'MASI' not in df.columns:
        st.error("❌ Le fichier CSV doit contenir 'Seance' et 'MASI'.")
        return

    if today in df['Seance'].astype(str).values:
        st.info("✅ La valeur du jour est déjà enregistrée.")
    else:
        new_row = pd.DataFrame([[today, masi]], columns=['Seance', 'MASI'])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success(f"✅ Valeur ajoutée : {today} → {masi:.2f}")

# ------------------------
# Chargement modèle + scaler
# ------------------------
try:
    model = load_model("modele_masi.keras")
    scaler = joblib.load("scaler.save")
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle ou du scaler : {e}")
    st.stop()

# ------------------------
# Interface utilisateur
# ------------------------
st.title("📈 Prédiction de l’indice MASI")
st.subheader("Bourse de Casablanca 📊")

with st.expander("ℹ️ À propos de l'application", expanded=True):
    st.markdown("""
    Cette application permet de prédire l'indice **MASI** (Moroccan All Shares Index) à l'aide d’un modèle LSTM basé sur les 60 derniers jours de données.

    Elle exécute automatiquement :
    - 📡 Le scraping de la valeur actuelle depuis Investing.com
    - 🗂️ La mise à jour de l'historique (`masi_history_ready.csv`)
    - 📈 La prédiction via le modèle LSTM
    - 🧭 L'affichage interactif du résultat

    ⚠️ *Ce modèle est à but démonstratif et ne constitue pas un conseil financier.*
    """)

# Mise à jour manuelle
if st.button("🔄 Mettre à jour la valeur MASI d’aujourd’hui"):
    update_history_manually()

today = datetime.today()

# Si week-end : pas de prédiction
if today.weekday() >= 5:
    st.info("📅 La Bourse est fermée aujourd’hui (week-end). Pas de prédiction.")
else:
    try:
        df = pd.read_csv("masi_history_ready.csv", parse_dates=["Seance"])
        df['MASI'] = pd.to_numeric(df['MASI'], errors='coerce')

        if len(df) < 60:
            st.warning("⛔ Pas assez de données (60 minimum) pour faire une prédiction.")
        else:
            # 📆 Choix de la date
            selected_date = st.date_input(
                "📅 Choisissez une date pour la prédiction",
                value=today + pd.Timedelta(days=1),
                min_value=today + pd.Timedelta(days=1),
                help="Date indicative uniquement"
            )

            # Préparation des données pour LSTM
            last_60 = df['MASI'].values[-60:].reshape(-1, 1)
            last_60_scaled = scaler.transform(last_60)
            X_input = last_60_scaled.reshape(1, 60, 1)

            pred_scaled = model.predict(X_input)
            pred = scaler.inverse_transform(pred_scaled)[0][0]

            # Affichage du résultat
            st.success(f"📊 Prédiction MASI pour le {selected_date.strftime('%Y-%m-%d')} : **{pred:.2f}**")

            # Graphique interactif Plotly
            recent_data = df.tail(60)
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=recent_data['Seance'],
                y=recent_data['MASI'],
                mode='lines+markers',
                name='MASI'
            ))

            fig.update_layout(
                title="Évolution de l'indice MASI (60 derniers jours)",
                xaxis_title="Date",
                yaxis_title="Valeur MASI",
                yaxis=dict(range=[14000, recent_data['MASI'].max() + 200]),
                template="plotly_white",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    except FileNotFoundError:
        st.error("❌ Le fichier `masi_history_ready.csv` est introuvable.")
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
