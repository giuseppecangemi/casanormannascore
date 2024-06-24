from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__, template_folder='templates')

def calcola_posizione(lista_gruppi=None, parametri=None, updates=None):
    if lista_gruppi is None:
        lista_gruppi = ["Contrada della Corte", "Artena", "Torri Metelliane", "Pozzo Seravezza", "Piazzarola", "Borgo Veneto",
                        "Borgo Don Bosco", "Tempesta Noale", "Arquatesi", "Terre Sabaude", "Rione Cento", "Borgo San Pietro",
                        "Porta Tufilla", "Rione Santa Caterina", "ASTA", "Citta Regia", "Rocca di Monselice",
                        "Torre Dei Germani", "Contesa Estense", "Rione San Paolo"]

    if parametri is None:
        parametri = {"Singolo": 1, "Coppia": 1.2, "Piccola": 1.4, "Grande": 1.6, "Musici": 1.6}

    df = pd.DataFrame(columns=["Posizione", "Gruppo", "Singolo", "Coppia", "Piccola", "Grande", "Musici", "Combinata"])

    for i, gruppo in enumerate(lista_gruppi):
        df.loc[i] = [np.nan] * len(df.columns)
        df.at[i, 'Gruppo'] = gruppo

    punteggi_singolo = [1, 3, 8, 5, 6, 9, 2, 12, 11, 10, 7, 5, 13, 19, 14, 18, 16, 15, 17, 20]
    punteggi_coppia = [1, 4, 2, 6, 7, 5, 11, 3, 9, 10, 13, 16, 12, 8, 14, 15, 17, 19, 18, 20]

    valori_punteggi_grande = {
        "Contrada della Corte": 2,
        "Artena": 13,
        "Torri Metelliane": 9,
        "Pozzo Seravezza": 4,
        "Piazzarola": 6,
        "Borgo Veneto": 1,
        "Borgo Don Bosco": 15,
        "Tempesta Noale": 19,
        "Arquatesi": 12,
        "Terre Sabaude": 16,
        "Rione Cento": 17,
        "Borgo San Pietro": 7,
        "Porta Tufilla": 3,
        "Rione Santa Caterina": 8,
        "ASTA": 5,
        "Citta Regia": 10,
        "Rocca di Monselice": 20,
        "Torre Dei Germani": 18,
        "Contesa Estense": 14,
        "Rione San Paolo": 11
    }

    punteggi_grande = [valori_punteggi_grande.get(gruppo, 0) for gruppo in lista_gruppi]

    valori_punteggi_musici = {
        "Contrada della Corte": 8,
        "Artena": 19,
        "Torri Metelliane": 5,
        "Pozzo Seravezza": 1,
        "Piazzarola": 4,
        "Borgo Veneto": 11,
        "Borgo Don Bosco": 16,
        "Tempesta Noale": 13,
        "Arquatesi": 2,
        "Terre Sabaude": 15,
        "Rione Cento": 17,
        "Borgo San Pietro": 9,
        "Porta Tufilla": 6,
        "Rione Santa Caterina": 3,
        "ASTA": 18,
        "Citta Regia": 14,
        "Rocca di Monselice": 20,
        "Torre Dei Germani": 10,
        "Contesa Estense": 7,
        "Rione San Paolo": 12
    }

    punteggi_musici = [valori_punteggi_musici.get(gruppo, 0) for gruppo in lista_gruppi]

    valori_punteggi_piccola = {
        "Contrada della Corte": 1,
        "Artena": 10,
        "Torri Metelliane": 7,
        "Pozzo Seravezza": 2,
        "Piazzarola": 13,
        "Borgo Veneto": 3,
        "Borgo Don Bosco": 12,
        "Tempesta Noale": 15,
        "Arquatesi": 5,
        "Terre Sabaude": 6,
        "Rione Cento": 16,
        "Borgo San Pietro": 8,
        "Porta Tufilla": 17,
        "Rione Santa Caterina": 9,
        "ASTA": 4,
        "Citta Regia": 11,
        "Rocca di Monselice": 20,
        "Torre Dei Germani": 19,
        "Contesa Estense": 14,
        "Rione San Paolo": 18
    }

    punteggi_piccola = [valori_punteggi_piccola.get(gruppo, 0) for gruppo in lista_gruppi]

    for i, j in df.iterrows():
        df.at[i, 'Singolo'] = punteggi_singolo[i]
        df.at[i, 'Coppia'] = punteggi_coppia[i]
        df.at[i, 'Piccola'] = punteggi_piccola[i]
        df.at[i, 'Grande'] = punteggi_grande[i]
        df.at[i, 'Musici'] = punteggi_musici[i]

    df = df.where(pd.notna(df), 0)

    if updates:
        for index, row in df.iterrows():
            df.at[index, 'Singolo'] = int(updates.get(f'singolo_{index}', row['Singolo']))
            df.at[index, 'Coppia'] = int(updates.get(f'coppia_{index}', row['Coppia']))
            df.at[index, 'Piccola'] = int(updates.get(f'piccola_{index}', row['Piccola']))
            df.at[index, 'Grande'] = int(updates.get(f'grande_{index}', row['Grande']))
            df.at[index, 'Musici'] = int(updates.get(f'musici_{index}', row['Musici']))

    for h, k in df.iterrows():
        df.at[h, 'Combinata'] = ((k.Singolo * parametri["Singolo"])
                                 + (k.Coppia * parametri["Coppia"])
                                 + (k.Piccola * parametri["Piccola"])
                                 + (k.Grande * parametri["Grande"])
                                 + (k.Musici * parametri["Musici"]))
    df["Combinata"] = round(df.Combinata, 3)
    df = df.sort_values(by='Combinata', ascending=True)
    df['Posizione'] = range(1, len(df) + 1)

    return df

@app.route('/')
def show_dataframe():
    df = calcola_posizione()
    df.set_index('Posizione', inplace=True)
    first_row_gold = df.index[0] == 1
    return render_template('index.html', dataframe=df, first_row_gold=first_row_gold)

@app.route('/update', methods=['POST'])
def update_scores():
    updates = request.form.to_dict()
    df = calcola_posizione(updates=updates)
    df.set_index('Posizione', inplace=True)
    first_row_gold = df.index[0] == 1
    return render_template('index.html', dataframe=df, first_row_gold=first_row_gold)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

