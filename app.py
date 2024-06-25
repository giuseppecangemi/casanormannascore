import pandas as pd
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Ottieni la porta dal valore di PORT nell'ambiente o usa 10000 di default se non definito
port = int(os.environ.get('PORT', 10000))

class CalcolaPosizione:
    def __init__(self, lista_gruppi=None, parametri=None, updates=None):
        self.lista_gruppi = lista_gruppi if lista_gruppi is not None else [
            "Contrada della Corte", "Artena", "Torri Metelliane", "Pozzo Seravezza", "Piazzarola", "Borgo Veneto",
            "Borgo Don Bosco", "Tempesta Noale", "Arquatesi", "Terre Sabaude", "Rione Cento", "Borgo San Pietro",
            "Porta Tufilla", "Rione Santa Caterina", "ASTA", "Citta Regia", "Rocca di Monselice",
            "Torre Dei Germani", "Contesa Estense", "Rione San Paolo"
        ]

        self.parametri = parametri if parametri is not None else {
            "Singolo": 1, "Coppia": 1.2, "Piccola": 1.4, "Grande": 1.6, "Musici": 1.6
        }

        self.updates = updates

        self.df = pd.DataFrame(columns=[
            "Posizione", "Gruppo", "Singolo", "Coppia", "Piccola", "Grande", "Musici", "Combinata"
        ])

    def popola_dataframe(self):
        for i, gruppo in enumerate(self.lista_gruppi):
            self.df.loc[i] = [None] * len(self.df.columns)
            self.df.at[i, 'Gruppo'] = gruppo
            self.df.at[i, 'Singolo'] = 0
            self.df.at[i, 'Coppia'] = 0
            self.df.at[i, 'Piccola'] = 0
            self.df.at[i, 'Grande'] = 0
            self.df.at[i, 'Musici'] = 0

    def applica_updates(self):
        if self.updates:
            for index, row in self.df.iterrows():
                self.df.at[index, 'Singolo'] = int(self.updates.get(f'singolo_{index}', row['Singolo']))
                self.df.at[index, 'Coppia'] = int(self.updates.get(f'coppia_{index}', row['Coppia']))
                self.df.at[index, 'Piccola'] = int(self.updates.get(f'piccola_{index}', row['Piccola']))
                self.df.at[index, 'Grande'] = int(self.updates.get(f'grande_{index}', row['Grande']))
                self.df.at[index, 'Musici'] = int(self.updates.get(f'musici_{index}', row['Musici']))

    def calcola_combinata(self):
        for h, k in self.df.iterrows():
            self.df.at[h, 'Combinata'] = ((k.Singolo * self.parametri["Singolo"])
                                         + (k.Coppia * self.parametri["Coppia"])
                                         + (k.Piccola * self.parametri["Piccola"])
                                         + (k.Grande * self.parametri["Grande"])
                                         + (k.Musici * self.parametri["Musici"]))
        self.df["Combinata"] = self.df["Combinata"].astype(float).round(3)
        self.df = self.df.sort_values(by='Combinata', ascending=True)
        self.df['Posizione'] = range(1, len(self.df) + 1)

    def calcola_posizione(self):
        self.popola_dataframe()
        self.applica_updates()
        self.calcola_combinata()
        return self.df


@app.route('/')
def index():
    calcolatore = CalcolaPosizione()
    df_posizione = calcolatore.calcola_posizione()
    return render_template('index.html', dataframe=df_posizione)

@app.route('/update', methods=['POST'])
def update():
    updates = {}
    for key, value in request.form.items():
        updates[key] = value
    calcolatore = CalcolaPosizione(updates=updates)
    df_posizione = calcolatore.calcola_posizione()
    return render_template('index.html', dataframe=df_posizione)


if __name__ == '__main__':
    # Avvia l'applicazione Flask
    app.run(host='0.0.0.0', port=port, debug=True)