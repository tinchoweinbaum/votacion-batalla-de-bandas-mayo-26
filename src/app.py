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

    # EN TU app.py, DENTRO DE LA RUTA /votar
    if not id_banda or not id_dispositivo:
        # CAMBIA ESTA LÍNEA A ESTO:
        print(f"DEBUG ERROR: Faltan datos. Banda: {id_banda}, Disp: {id_dispositivo}")
        return jsonify({"status": "error", "message": "Faltan datos."}), 400
    
    if not id_banda or not id_dispositivo:
        return jsonify({"status": "error", "message": "Faltan datos."}), 400
        
    if db.votar_banda(id_banda, id_dispositivo):
        return jsonify({"status": "success", "message": "Voto registrado."}), 200
    else:
        return jsonify({"status": "error", "message": "Ya votaste en esta batalla."}), 403

@app.route('/estado_votos', methods=['GET'])
def estado_votos():
    id_dispositivo = request.args.get('id_dispositivo')
    if not id_dispositivo:
        return jsonify({"votadas": []})
        
    votadas = db.obtener_votos_dispositivo(id_dispositivo)
    return jsonify({"votadas": votadas})

@app.route('/api/resultados')
def api_resultados():
    datos = db.obtener_resultados() 
    return jsonify(datos)

@app.route('/resultados')
def resultados():
    datos = db.obtener_resultados()
    return render_template('resultados.html', resultados=datos)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)