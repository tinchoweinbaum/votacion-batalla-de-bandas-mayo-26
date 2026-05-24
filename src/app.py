from flask import Flask, request, render_template, jsonify
from db_manager import Database
from waitress import serve

app = Flask(__name__)
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/votar', methods=['POST'])
def votar():
    id_banda = request.form.get('id_banda')
    id_dispositivo = request.form.get('id_dispositivo')
    
    # Validaciones en el backend por si las dudas
    if not id_banda or not id_dispositivo:
        return jsonify({"status": "error", "message": "Faltan datos."}), 400
        
    # Intentamos votar
    if db.votar_banda(id_banda, id_dispositivo):
        return jsonify({"status": "success", "message": "Voto registrado."}), 200
    else:
        # Si devuelve False, es porque la DB bloqueó el voto (ya votó en esta batalla)
        return jsonify({"status": "error", "message": "Ya votaste en esta batalla."}), 403

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)