import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def generate():
    try:
        # Wczytujemy dane - ważne, aby nazwy kolumn w CSV były identyczne
        df = pd.read_csv('magazyn.csv', parse_dates=['start_p', 'koniec_p'])
    except Exception as e:
        print(f"Błąd wczytywania CSV: {e}")
        return

    # Ustawiamy zakres wykresu od dzisiaj do najdalszej daty w pliku
    start_plot = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if not df.empty:
        end_plot = max(df['koniec_p'].max(), start_plot + timedelta(days=30))
    else:
        end_plot = start_plot + timedelta(days=30)

    dni = pd.date_range(start_plot, end_plot)

    # Obliczamy sumę powierzchni dla każdego dnia
    zajetosc = []
    for dzien in dni:
        mask = (df['start_p'] <= dzien) & (df['koniec_p'] >= dzien)
        suma = df.loc[mask, 'powierzchnia'].sum()
        zajetosc.append(suma)

    # Tworzenie wykresu
    plt.figure(figsize=(10, 5))
    plt.plot(dni, zajetosc, color='#1f77b4', linewidth=2, label='Zajęte m2')
    plt.fill_between(dni, zajetosc, alpha=0.2, color='#1f77b4')
    
    plt.title('Prognoza zajętości magazynu', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Zapisujemy jako obraz .png
    plt.savefig('wykres_zajetosci.png')

if __name__ == "__main__":
    generate()
