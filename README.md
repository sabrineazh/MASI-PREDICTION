# 📈 MASI Prediction App

Application Streamlit de prédiction de l'indice **MASI** (Moroccan All Shares Index) basée sur un modèle **LSTM** entraîné avec des données historiques de la Bourse de Casablanca.

---

## 🎯 Objectif

Fournir une **interface interactive** permettant de :
- Visualiser l’évolution historique de l’indice MASI
- Prédire la prochaine valeur de l’indice à partir des 60 derniers jours
- Mettre à jour manuellement la base de données avec les nouvelles valeurs quotidiennes

---

## 🧠 Modèle utilisé

- **Architecture** : LSTM (Long Short-Term Memory)
- **Fenêtre temporelle** : séquences de 60 jours
- **Prétraitement** : normalisation via `MinMaxScaler`
- **Entraînement** : TensorFlow, scikit-learn

Le modèle est sauvegardé au format `.keras` pour une meilleure compatibilité au déploiement.

---

## 📂 Contenu du dépôt

| Fichier | Description |
|--------|-------------|
| `prediction_masi.py` | Script principal de l’application Streamlit |
| `update_masi_script.py` | Script de mise à jour manuelle des données |
| `modele_masi.keras` | Modèle LSTM sauvegardé |
| `scaler_masi.pkl` | Scaler pour la normalisation des données |
| `masi_history_ready.csv` | Historique complet de l’indice MASI |
| `requirements.txt` | Dépendances nécessaires au déploiement |
| `PREDICTION MASI - SA.ipynb` | Notebook de développement du modèle |

---

## 🌐 Déploiement

L’application est conçue pour être déployée sur [Streamlit Cloud](https://streamlit.io/cloud).
https://masi-prediction.streamlit.app/
