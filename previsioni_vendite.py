import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Genera dataset di esempio se non esiste (struttura: Data, Prodotto, Vendite, Prezzo)
if not os.path.exists('vendite.csv'):
    print("Generando dataset esempio...")
    np.random.seed(42)
    n_days = 365
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_days)]
    prodotti = ['Biscotti', 'Pizza', 'Pane', 'Latte', 'Acqua']
    data = {
        'Data': np.random.choice(dates, 1000),
        'Prodotto': np.random.choice(prodotti, 1000),
        'Vendite': np.random.randint(10, 100, 1000),
        'Prezzo': np.random.uniform(1, 10, 1000)
    }
    df_raw = pd.DataFrame(data)
    df_raw.to_csv('vendite.csv', index=False)
    print("Dataset salvato in vendite.csv")
else:
    df_raw = pd.read_csv('vendite.csv')
    print("Dataset caricato da vendite.csv")

# Parte 1: Caricamento e esplorazione
print("\nParte 1 - Caricamento e esplorazione dati")
print("Prime 5 righe:")
print(df_raw.head())
print("\nInfo dataset:")
print(df_raw.info())
print("\nStatistiche descrittive:")
print(df_raw.describe())

# Parte 2: Pulizia
print("\nParte 2 - Pulizia dati")
df = df_raw.copy()
# Simula e gestisce NaN
df.loc[np.random.choice(df.index, 20), 'Vendite'] = np.nan
media_vendite = df['Vendite'].mean()
df['Vendite'] = df['Vendite'].fillna(media_vendite)  # Fix chained assignment
print(f"Valori mancanti in 'Vendite' riempiti con media: {media_vendite:.2f}")

# Rimuovi duplicati
duplicati_pre = len(df)
df.drop_duplicates(inplace=True)
duplicati_post = len(df)
print(f"Duplicati rimossi: {duplicati_pre - duplicati_post}")

# Correggi tipi dati
df['Data'] = pd.to_datetime(df['Data'])
df['Vendite'] = pd.to_numeric(df['Vendite'], errors='coerce')
df['Prezzo'] = pd.to_numeric(df['Prezzo'], errors='coerce')
print("Tipi dati corretti: Data -> datetime, Vendite/Prezzo -> numeric")

# Parte 3: Analisi esplorativa
print("\nParte 3 - Analisi esplorativa")
vendite_totali = df.groupby('Prodotto')['Vendite'].sum().round(2)
print("\nVendite totali per prodotto:")
print(vendite_totali)

piu_venduto = vendite_totali.idxmax()
meno_venduto = vendite_totali.idxmin()
print(f"\nProdotto più venduto: {piu_venduto} ({vendite_totali.max():.2f})")
print(f"Prodotto meno venduto: {meno_venduto} ({vendite_totali.min():.2f})")

df.set_index('Data', inplace=True)
medie_giornaliere = df.groupby('Data')['Vendite'].mean().round(2)
print("\nPrime 5 vendite medie giornaliere:")
print(medie_giornaliere.head())

# Salva pulito
df.reset_index(inplace=True)
df.to_csv('vendite_pulite.csv', index=False)
print("\nDataset pulito salvato in 'vendite_pulite.csv'")
print("\nProgetto completato! ZIP: previsioni_vendite.py + vendite.csv + vendite_pulite.csv")
