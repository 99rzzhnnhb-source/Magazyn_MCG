import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def generate():
    # 1. Wczytanie danych z Twojego pliku CSV
    # Używamy nazw kolumn: projekt, start_p, koniec_p, powierzchnia, sure
    try:
        df = pd.read_csv('magazyn.csv', parse_dates=['start_p', 'koniec_p'])
    except Exception as e:
        print(f"Błąd podczas wczytywania pliku CSV: {e}")
        return

    # 2. Określenie zakresu czasu dla wykresu
    # Zaczynamy od dzisiaj, kończymy na ostatniej dacie z pliku (lub 30 dni od dziś, jeśli plik jest pusty)
    start_plot = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if not df.empty:
        end_plot = df['koniec_p'].max()
        # Jeśli ostatni projekt kończy się wcześniej niż za 30 dni, rozciągnij wykres
        if end_plot < start_plot + timedelta(days=30):
            end_plot = start_plot + timedelta(days=30)
    else:
        end_plot = start_plot + timedelta(days=30)

    dni = pd.date_range(start_plot, end_plot)

    # 3. Obliczanie zajętości dla każdego dnia
    zajetosc = []
    for dzien in dni:
        # Sumujemy powierzchnię projektów, które trwają w tym konkretnym dniu
        mask = (df['start_p'] <= dzien) & (df['koniec_p'] >= dzien)
        suma = df.loc[mask, 'powierzchnia'].sum()
        zajetosc.append(suma)

    # 4. Rysowanie wykresu
    plt.figure(figsize=(12, 6))
    plt.plot(dni, zajetosc, marker='', linestyle='-', color='#1f77b4', linewidth=2.5, label='Zajęta powierzchnia')
    plt.fill_between(dni, zajetosc, alpha=0.2, color='#1f77b4')

    # Stylizacja wykresu
    plt.title('Prognoza zajętości magazynu (m2)', fontsize=16, pad=20)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Suma m2', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.legend()
    
    # Dodanie czerwonej linii limitu (opcjonalnie - np. 500m2)
    # plt.axhline(y=500, color='r', linestyle='--', label='Limit magazynu')

    plt.tight_layout()

    # 5. Zapisanie do pliku (ten plik będzie wyświetlany w README)
    plt.savefig('wykres_zajetosci.png', dpi=100)
    print("Wykres został wygenerowany pomyślnie jako 'wykres_zajetosci.png'")

if __name__ == "__main__":
    generate()
