"""
Módulo gestor de la base de datos que app.py va a importar para poder manejar la base de datos.
"""
from contextlib import contextmanager
from datetime import datetime
import os
import sqlite3

class Database:
    def __init__(self):
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.cwd, "db_main.db")
        self.init_db()

    @contextmanager
    def _connect(self):
        conexion = sqlite3.connect(self.db_path)
        try:
            conexion.execute("PRAGMA foreign_keys = ON;")
            yield conexion 
            conexion.commit() 
        except sqlite3.Error as error:
            conexion.rollback() 
            print(f"[DB ERROR] Error en la transacción: {error}")
            raise error
        finally:
            conexion.close() 

    def init_db(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys = ON;")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bandas_participantes (
                    id_batalla INTEGER NOT NULL,
                    id_banda TEXT NOT NULL,
                    PRIMARY KEY (id_batalla, id_banda)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS votos (
                    id_voto INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_batalla INTEGER NOT NULL,
                    id_banda TEXT NOT NULL,
                    id_dispositivo TEXT NOT NULL,
                    FOREIGN KEY (id_batalla, id_banda) 
                        REFERENCES bandas_participantes(id_batalla, id_banda),
                    UNIQUE(id_batalla, id_dispositivo)
                );
            """)
            conexion.commit()

            cursor.execute("SELECT COUNT(*) FROM bandas_participantes;")
            if cursor.fetchone()[0] == 0:
                print("Cargando fixture de prueba inicial...")
                fixture = [
                    (1, "gilda"), (1, "dinorah"),
                    (2, "ficc"), (2, "ntme"),
                    (3, "marchi"), (3, "cartas"),
                ]
                cursor.executemany("INSERT INTO bandas_participantes (id_batalla, id_banda) VALUES (?, ?);", fixture)
                conexion.commit()
                print("Fixture inicializado.")

            print("Conexión inicial/inicialización exitosa")
        except sqlite3.Error as error:
            print(f"Error al inicializar la base de datos: {error}")
        finally:
            conexion.close()

    def votar_banda(self, id_banda, id_dispositivo):
        with self._connect() as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO votos (id_batalla, id_banda, id_dispositivo)
                SELECT id_batalla, id_banda, ? 
                FROM bandas_participantes 
                WHERE id_banda = ?;
            """
            try:
                ahora = datetime.now().strftime("%H:%M:%S")
                cursor.execute(query, (id_dispositivo, id_banda))
                
                if cursor.rowcount > 0:
                    print(f"{ahora} - [VOTO] Voto efectuado para '{id_banda}' desde {id_dispositivo}")
                    return True
                else:
                    print(f"{ahora} - [VOTO RECHAZADO] La banda '{id_banda}' no existe.")
                    return False
                    
            except sqlite3.IntegrityError:
                print(f"[VOTO BLOQUEADO] El dispositivo {id_dispositivo} ya votó en esta batalla.")
                return False

    def obtener_votos_dispositivo(self, id_dispositivo):
        """Devuelve una lista con los IDs de las batallas donde este dispositivo ya votó."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_batalla FROM votos WHERE id_dispositivo = ?;", (id_dispositivo,))
            # Esto devuelve algo como [1, 3] si votó en las batallas 1 y 3
            return [row[0] for row in cursor.fetchall()]
        
    def obtener_resultados(self):
        """Devuelve un diccionario con los votos totales por banda agrupados por batalla."""
        with self._connect() as conn:
            cursor = conn.cursor()
            # Esta consulta trae la cantidad de votos por cada banda en cada batalla
            query = """
                SELECT b.id_batalla, b.id_banda, COUNT(v.id_voto) as total
                FROM bandas_participantes b
                LEFT JOIN votos v ON b.id_batalla = v.id_batalla AND b.id_banda = v.id_banda
                GROUP BY b.id_batalla, b.id_banda;
            """
            cursor.execute(query)
            resultados = {}
            for bat, ban, tot in cursor.fetchall():
                if bat not in resultados: resultados[bat] = []
                resultados[bat].append({'banda': ban, 'votos': tot})
            return resultados

if __name__ == "__main__":
    pass