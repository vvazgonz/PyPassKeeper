import json
import os
from flask import Flask, request, render_template, redirect, url_for
from crypto import cod, decod  # Importa tus funciones de cifrado y descifrado

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    data = {
        'web': request.form['web'],
        'user': request.form['user'],
        'password': cod(request.form['password'])  # Cifra la contraseña
    }

    # Leer datos anteriores si existen y si el archivo no está vacío
    existing_data = []
    if os.path.exists('data.json') and os.path.getsize('data.json') > 0:
        with open('data.json', 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                print("Archivo JSON corrupto o vacío")

    existing_data.append(data)

    # Guardar de nuevo
    with open('data.json', 'w') as f:
        json.dump(existing_data, f, indent=4)

    return redirect(url_for('view'))  # redirige al visualizador

@app.route('/view')
def view():
    data = []
    if os.path.exists('data.json') and os.path.getsize('data.json') > 0:
        with open('data.json', 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Archivo JSON corrupto o vacío")

    # Descifra las contraseñas antes de enviarlas al template
    for entry in data:
        entry['password'] = decod(entry['password'])

    return render_template('view.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
