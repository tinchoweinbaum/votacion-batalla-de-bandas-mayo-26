from flask import Flask, request, render_template
from db_manager import Database
from waitress import serve

app = Flask(__name__)
db = Database() # Instancia la database, lo que la crea e inicializa si no existe.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/votar', methods=['POST'])
def votar():
    id_banda = request.form.get('id_banda') # Levanto el id de la banda votada junto con el id del dispositivo que votó
    id_fijo = "test_device_001"
    
    if not id_banda:
        return "<h1>ERROR: No mandaste ninguna banda.</h1>", 400
        
    voto_valido = db.votar_banda(id_banda, id_fijo)

    if voto_valido:
        return f"<h1>ÉXITO: '{id_banda}' escrito en la DB.</h1><br><a href='/'>Volver</a>"
    else:
        return "<h1>FALLO: La banda no existe o ya votaste (test_device_001 ya tiene voto).</h1><br><a href='/'>Volver</a>"
    
if __name__ == "__main__":
    print("Iniciando servidor de producción con Waitress en el puerto 5000...")
    serve(app, host='0.0.0.0', port=5000)
    