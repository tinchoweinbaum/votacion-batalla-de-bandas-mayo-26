import os
import sqlite3

def init_db():
    # 1. Definir la ruta absoluta de la base de datos de forma compatible con Windows/Linux
    cwd = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(cwd, "db_main.db")

    print(f"Conectando a la base de datos en: {db_path}")

    # 2. Conectar (si el archivo no existe, SQLite lo crea automáticamente)
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    print(f"Conectado con la base de datos en {db_path}")

    try:
        # 3. ACTIVAR CLAVES FORÁNEAS (Crucial para SQLite, se hace por cada conexión)
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 4. Crear la tabla de Reglamento (bandas_participantes)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bandas_participantes (
                id_batalla INTEGER NOT NULL,
                id_banda TEXT NOT NULL,
                PRIMARY KEY (id_batalla, id_banda)
            );
        """
        )

        # 5. Crear la tabla Principal (votos) con su Clave Foránea
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS votos (
                id_voto INTEGER PRIMARY KEY AUTOINCREMENT,
                id_batalla INTEGER NOT NULL,
                id_banda TEXT NOT NULL,
                id_dispositivo TEXT,
                FOREIGN KEY (id_batalla, id_banda) 
                    REFERENCES bandas_participantes(id_batalla, id_banda)
            );
        """
        )

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

    except sqlite3.Error as error:
        print(f"Error al inicializar la base de datos: {error}")

    finally:
        # Cerrar la conexión siempre para liberar el archivo
        conexion.close()


if __name__ == "__main__":
    init_db()