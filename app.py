import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 1. Wczytanie danych
df = pd.read_csv('magazyn.csv', parse_dates=['Start', 'Koniec'])

# 2. Określenie zakresu czasu dla wykresu (od dziś do 3 miesięcy w przód)
start_plot = datetime.now()
end_plot = start_plot + timedelta(days=90)
dni = pd.date_range(start_plot, end_plot)

# 3. Obliczanie zajętości dla każdego dnia
zajetosc = []
for dzien in dni:
    # Sumuj powierzchnię projektów, które trwają w tym konkretnym dniu
    suma = df[(df['Start'] <= dzien) & (df['Koniec'] >= dzien)]['Powierzchnia'].sum()
    zajetosc.append(suma)

# 4. Rysowanie wykresu
plt.figure(figsize=(10, 6))
plt.plot(dni, zajetosc, marker='o', linestyle='-', color='b')
plt.fill_between(dni, zajetosc, alpha=0.2, color='b')

plt.title('Prognoza zajętości magazynu (m2)')
plt.xlabel('Data')
plt.ylabel('Suma zajętej powierzchni')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()

# 5. Zapisanie do pliku
plt.savefig('wykres_zajetosci.png')
