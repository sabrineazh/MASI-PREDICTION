# Réexécution nécessaire suite à la réinitialisation de l'environnement

from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_masi_value():
    url = "https://fr.investing.com/indices/masi"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        masi_val = soup.find("div", {"class": "text-5xl/6 font-bold"}).text.strip().replace(",", "")
        return float(masi_val)
    except Exception as e:
        print(f"Erreur lors du scraping : {e}")
        return None

def update_csv(file_path="masi_history_ready.csv"):
    today = datetime.today().strftime("%Y-%m-%d")
    masi_value = get_masi_value()
    if masi_value is None:
        return

    try:
        df = pd.read_csv(file_path)
        if today in df["Date"].values:
            print("La valeur d'aujourd'hui est déjà enregistrée.")
            return
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Valeur"])

    new_entry = pd.DataFrame([{"Date": today, "Valeur": masi_value}])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(file_path, index=False)
    print(f"✅ Mise à jour réussie : {today} - {masi_value}")

# Confirmation pour l'utilisateur
"Le script a bien été préparé pour automatiser la mise à jour du fichier 'masi_history_ready.csv'."
