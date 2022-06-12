import sqlite3

def ejecutar_query_y_recuperar_respuesta(c: sqlite3.Cursor, query: str) -> list:
    """
    Está función nos permite ejecutar nuestro query y recuperar el resultado.
    """
    c.execute(query)
    respuesta = c.fetchall()
    return respuesta

def imprimir_pregunta_y_respuesta(pregunta: str, num_pregunta: int, c: sqlite3.Cursor, query: str, nota: str=None) -> None:
    """
    Está función nos permite imprimir de forma ordenada la pregunta dada y su respuesta.
    Así como una nota en su debido caso.
    """
    print('~'*80)
    print("Pregunta : ", pregunta)
    respuesta = ejecutar_query_y_recuperar_respuesta(c, query)
    if num_pregunta != 4:
        print("Respuesta : ", respuesta[0][0].upper())
    else:
        print("Respuesta : ", respuesta)
    if nota:
        print("Nota : ", nota)
    print()

def crear_tablas_e_insertar_datos(conn: sqlite3.Connection, c: sqlite3.Cursor) -> None:
    """
    Está función nos permite crear las tablas de la BD e insertar los datos dados
    en el challengue.
    """
    c.execute("""
        CREATE TABLE IF NOT EXISTS aereolineas (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            NOMBRE_AEREOLINEA VARCHAR(20) NOT NULL
        );
        """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS aereopuertos (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            NOMBRE_AEREOPUERTO VARCHAR(50) NOT NULL
        );
        """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            DESCRIPCION VARCHAR(10) NOT NULL
        );
        """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS vuelos (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            ID_AEREOLINEA INT NOT NULL,
            ID_AEREOPUERTO INT NOT NULL,
            ID_MOVIMIENTO INT NOT NULL,
            DIA DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ID_AEREOLINEA) REFERENCES aereolineas(ID) ON DELETE CASCADE,
            FOREIGN KEY (ID_AEREOPUERTO) REFERENCES aereopuertos(ID) ON DELETE CASCADE,
            FOREIGN KEY (ID_MOVIMIENTO) REFERENCES movimientos(ID) ON DELETE CASCADE
        );
        """)
    # ~~~~~~~~~~~~
    c.execute("""
            INSERT INTO aereolineas VALUES 
            (1, "Volaris"), 
            (2, "Aeromar"), 
            (3, "Interjet"), 
            (4, "Aeromexico");
            """)
    c.execute("""
            INSERT INTO aereopuertos VALUES 
            (1, "Benito Juarez"), 
            (2, "Guanajuato"), 
            (3, "La paz"), 
            (4, "Oaxaca");
            """)
    c.execute("""
            INSERT INTO movimientos VALUES 
            (1, "Salida"), 
            (2, "Llegada");
            """)
    c.execute("""
            INSERT INTO vuelos VALUES 
            (1,1,1,1,"2021-05-02"),
            (2,2,1,1,"2021-05-02"),
            (3,3,2,2,"2021-05-02"),
            (4,4,3,2,"2021-05-02"),
            (5,1,3,2,"2021-05-02"),
            (6,2,1,1,"2021-05-02"),
            (7,2,3,1,"2021-05-04"),
            (8,3,4,1,"2021-05-04"),
            (9,3,4,1,"2021-05-04");
            """)
    # conn.commit()

conn = sqlite3.connect("desafio_dos.db")
c = conn.cursor()

crear_tablas_e_insertar_datos(conn, c)

# ---
# Pregunta 1:
pregunta = "¿Cuál es el nombre aeropuerto que ha tenido mayor movimiento durante el año?"
query = """
        SELECT NOMBRE_AEREOPUERTO
            FROM (SELECT NOMBRE_AEREOPUERTO, COUNT(*) FROM vuelos JOIN aereopuertos ON vuelos.ID_AEREOPUERTO = aereopuertos.ID
                  GROUP BY vuelos.ID_AEREOPUERTO, vuelos.ID_MOVIMIENTO)
            GROUP BY NOMBRE_AEREOPUERTO ORDER BY COUNT(*) DESC
            LIMIT 1;
        """
nota = "\nOriginalmente había pensado que se trataba de dos aereopuertos (La paz y Benito Juarez)."
nota += "\nSin embargo, dado que la pregunta es en singular decidí tomar como criterio a aquel aereopuerto"
nota += "\nque tuviera tanto salidas como llegadas. Finalmente, considerar que siento que la pregunta es algo ambigua."
imprimir_pregunta_y_respuesta(pregunta, 1, c, query, nota)

# ---
# Pregunta 2:
pregunta = "¿Cuál es el nombre aerolínea que ha realizado mayor número de vuelos durante el año?"
query = """
        SELECT NOMBRE_AEREOLINEA, COUNT(*) FROM vuelos JOIN aereolineas ON vuelos.ID_AEREOLINEA = aereolineas.ID
        WHERE ID_MOVIMIENTO=1 GROUP BY NOMBRE_AEREOLINEA
        LIMIT 1;
        """
nota = "\nLa pregunta se me hace algo ambigua, dado que en lo particular originalmente creí que eran dos aereolíneas"
nota += "\n(Interjet y Aeromar). Sin embargo, dado que la pregunta estaba en singular, decidí considerar a los vuelos"
nota += "\ncomo salidas y aplicar dicho criterio como una condición más en mi query."
imprimir_pregunta_y_respuesta(pregunta, 2, c, query, nota)

# ---
# Pregunta 3:
pregunta = "¿En qué día se han tenido mayor número de vuelos?"
query = """
        SELECT DIA
            FROM (SELECT COUNT(*)*100.0/(SELECT COUNT(*) FROM vuelos WHERE DIA='2021-05-04') AS Result, DIA FROM vuelos 
                  WHERE DIA='2021-05-04' AND ID_MOVIMIENTO=1
                  UNION 
                  SELECT COUNT(*)*100.0/(SELECT COUNT(*) FROM vuelos WHERE DIA='2021-05-02') AS Result, DIA FROM vuelos 
                  WHERE DIA='2021-05-02' AND ID_MOVIMIENTO=1)
            ORDER BY Result DESC LIMIT 1;
        """
imprimir_pregunta_y_respuesta(pregunta, 3, c, query)

# ---
# Pregunta 4:
pregunta = "¿Cuáles son las aerolíneas que tienen mas de 2 vuelos por día?"
query = """
        SELECT NOMBRE_AEREOLINEA, COUNT(*) FROM vuelos JOIN aereolineas ON vuelos.ID_AEREOLINEA = aereolineas.ID 
        GROUP BY DIA, ID_AEREOLINEA
        ORDER BY COUNT(*) DESC;
        """
nota = "\nDado que ninguna aerolínea tiene MÁS DE DOS VUELOS POR DÍA (lo cual se aprecia en el resultado del query),"
nota += "\nel resultado es NINGUNA."
imprimir_pregunta_y_respuesta(pregunta, 4, c, query, nota)

conn.close()