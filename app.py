import os
from flask import Flask, request, render_template, send_file
import pandas as pd

arbitros_tutoria = [
    'ARENAS',
    'BAZTAN',
    'BERROJO',
    'CERRATO',
    'EOIN',
    'FORTEA',
    'HUGO',
    'IRIS',
    'ITURMENDI',
    'JANKE',
    'JARANDILLA',
    'MATIAS',
    'MIALDEA',
    'OCHAGAVIA',
    'PESGA',
    'QUINTO',
    'VENZALA',
    'ANDORRA',
    'ARICO',
    'ARIDANE',
    'ARQUILLOS',
    'BONET',
    'CANDELARIA',
    'CHEN',
    'CONIL',
    'CORCES',
    'ENGELS',
    'FRANVAZ',
    'LILLO',
    'LUCENA',
    'MARIO',
    'OLVAN',
    'ROQUETAS',
    'SABADELL',
    'SARRIA',
    'SIDONIA'
]

app = Flask(__name__)

# Carpetas para almacenar archivos temporalmente
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No se envió ningún archivo", 400

    file = request.files["file"]
    if file.filename == "":
        return "El archivo no tiene nombre", 400

    if file and file.filename.endswith(".xlsx"):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Procesar el archivo con pandas
        processed_file_path = process_excel(file_path)

        return send_file(processed_file_path, as_attachment=True)

    return "Por favor sube un archivo .xlsx", 400

def process_excel(file_path):
    # Cargar el archivo Excel con pandas
    df = pd.read_excel(file_path)

    #Modificación
    df = df[df['PRINCIPAL'].isin(arbitros_tutoria)]

    # Guardar el nuevo archivo
    processed_file_path = os.path.join(PROCESSED_FOLDER, "tutoria_" + os.path.basename(file_path))
    df.to_excel(processed_file_path, index=False)
    return processed_file_path

if __name__ == "__main__":
    app.run(debug=True)
