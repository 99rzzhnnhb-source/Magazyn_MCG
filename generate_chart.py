import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def generate():
    try:
        df = pd.read_csv('magazyn.csv', parse_dates=['start_p', 'koniec_p'])
        df = df.dropna(subset=['start_p', 'koniec_p'])
    except Exception as e:
        print(f"Błąd danych: {e}")
        return

    # Przygotowanie osi czasu (od dzisiaj + 90 dni)
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=90)
    dni = pd.date_range(start_date, end_date)

    # Tworzymy listę rekordów dla każdego dnia i każdego projektu
    plot_data = []
    for dzien in dni:
        # Sprawdzamy każdy projekt z osobna dla danego dnia
        mask = (df['start_p'] <= dzien) & (df['koniec_p'] >= dzien)
        active_projects = df[mask]
        
        if active_projects.empty:
            plot_data.append({'Data': dzien, 'Powierzchnia': 0, 'Projekt': 'Pusty Magazyn'})
        else:
            for _, row in active_projects.iterrows():
                plot_data.append({
                    'Data': dzien, 
                    'Powierzchnia': row['powierzchnia'], 
                    'Projekt': row['projekt']
                })

    df_plot = pd.DataFrame(plot_data)

    # Tworzenie nowoczesnego wykresu skumulowanego
    fig = px.area(df_plot, x="Data", y="Powierzchnia", color="Projekt",
                  title="Interaktywna Prognoza Zajętości Magazynu",
                  color_discrete_sequence=px.colors.qualitative.Pastel,
                  template="plotly_white")

    # Dodanie interakcji i poprawa wyglądu
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Data",
        yaxis_title="Suma m2",
        legend_title="Kliknij, aby ukryć projekt:",
        font=dict(family="Arial", size=12)
    )

    # Zapisanie jako plik HTML
    fig.write_html("index.html")
    print("Sukces: Wygenerowano interaktywny wykres index.html")

if __name__ == "__main__":
    generate()
