"""
Módulo gestor de la base de datos que main.py va a importar para poder manejar la base de datos.
"""
from contextlib import contextmanager

import os
import sqlite3

class Database:
    def __init__(self):
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.cwd, "db_main.db")

        self.init_db()

    @contextmanager
    def _connect(self):
        """
        Método decorado que se encarga de abrir y cerrar la conexión cuando corresponda en el método que se lo invoca. Se usa con with ___ as ___:
        """
        conexion = sqlite3.connect(self.db_path)
        try:
            conexion.execute("PRAGMA foreign_keys = ON;")
            yield conexion  # yield es un return a medias. Devuelve el objeto conexión. Una vez returneó quien llamó a esta función, se continúa la ejecución.
            conexion.commit()  # Si todo sale bien, guarda los cambios
        except sqlite3.Error as error:
            conexion.rollback()  # Si algo falla, cancela la transacción
            print(f"[DB ERROR] Error en la transacción: {error}")
            raise error
        finally:
            conexion.close()  # Se cierra SIEMPRE, liberando el archivo para otros hilos

    def init_db(self):

        # Conectar (si el archivo no existe, SQLite lo crea automáticamente)
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()

        try:
            # ACTIVAR CLAVES FORÁNEAS (Crucial para SQLite, se hace por cada conexión)
            cursor.execute("PRAGMA foreign_keys = ON;")

            # Crear la tabla de Reglamento (bandas_participantes)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS bandas_participantes (
                    id_batalla INTEGER NOT NULL,
                    id_banda TEXT NOT NULL,
                    PRIMARY KEY (id_batalla, id_banda)
                );
            """
            )

            # Crear la tabla Principal (votos) con su Clave Foránea
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS votos (
                    id_voto INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_batalla INTEGER NOT NULL,
                    id_banda TEXT NOT NULL,
                    id_dispositivo TEXT,
                    FOREIGN KEY (id_batalla, id_banda) 
                        REFERENCES bandas_participantes(id_batalla, id_banda),
                    UNIQUE(id_batalla, id_dispositivo) -- <--- ESTA REGLA BLINDA EL SISTEMA
                );
            """)

            # Guardar los cambios en el archivo
            conexion.commit()

            # Si la tabla de bandas estaba vacía la inicializa.
            cursor.execute("SELECT COUNT(*) FROM bandas_participantes;")
            if cursor.fetchone()[0] == 0:
                print("Cargando fixture de prueba inicial...")
                # Fixture totalmente sujeto a cambios. No tengo idea como voy a estructurar más adelante todo el manejo de la db ni que clases voy a definir.
                fixture = [
                    (1, "marchi"),
                    (1, "cartas"),
                    (2, "ficc"),
                    (2, "ntme"),
                    (3, "gilda"),
                    (3, "dinorah"),
                ]
                cursor.executemany(
                    "INSERT INTO bandas_participantes (id_batalla, id_banda) VALUES (?, ?);",
                    fixture,
                )
                conexion.commit()
                print("Fixture inicializado.")

            print("Conexión inicial/inicialización exitosa")

        except sqlite3.Error as error:
            print(f"Error al inicializar la base de datos: {error}")

        finally:
            # Cerrar la conexión siempre para liberar el archivo
            conexion.close()

    def votar_banda(self, id_banda, id_dispositivo):
            """
            Registra un voto en la base de datos. Utiliza la tabla auxiliar para saber a que batalla corresponde cada banda.
            Recibe id_banda de la banda a votar y id_dispositivo para evitar votos duplicados.
            """
            with self._connect() as conn:
                cursor = conn.cursor()
                
                query = """
                    INSERT INTO votos (id_batalla, id_banda, id_dispositivo)
                    SELECT id_batalla, id_banda, ? 
                    FROM bandas_participantes 
                    WHERE id_banda = ?;
                """
                
                try:
                    cursor.execute(query, (id_dispositivo, id_banda))
                    
                    if cursor.rowcount > 0:
                        print(f"[VOTO] Exitoso para '{id_banda}' desde {id_dispositivo}")
                        return True
                    else:
                        print(f"[VOTO RECHAZADO] La banda '{id_banda}' no existe en el reglamento.")
                        return False
                        
                except sqlite3.IntegrityError:
                    # El UNIQUE saltó en el búnker y bloqueó el registro
                    print(f"[VOTO BLOQUEADO] El dispositivo {id_dispositivo} ya votó en esta batalla.")
                    return False

if __name__ == "__main__":
    pass