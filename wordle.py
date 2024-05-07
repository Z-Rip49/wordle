from typing import List
import mysql.connector as db
import constantes
from constantes import DB_HOSTNAME,DB_DATABASE,DB_PASSWORD,DB_USERNAME

def abrir_conexion() -> db.pooling.PooledMySQLConnection | db.MySQLConnection:
    """Abre una conexión con la base de datos

        Deben especificarse los datos en el módulo de constantes para poder
        conectar a la base de datos local correspondiente.

    Returns:
        PooledMySQLConnection | MySQLConnection: conexión a la base de datos
    """
    return db.connect(host=DB_HOSTNAME,
                      user=DB_USERNAME,
                      password=DB_PASSWORD,
                      database=DB_DATABASE)

def consulta_generica(conn : db.MySQLConnection, consulta : str) -> List[db.connection.RowType]:
    """Hace una consulta la base de datos

    Args:
        conn (MySQLConnection): Conexión a la base de datos obtenida por abrir_conexion()
        consulta (str): Consulta en SQL para hacer en la BD

    Returns:
        List[RowType]: Una lista de tuplas donde cada tupla es un registro y 
                        cada elemento de la tupla es un campo del registro.
    """
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta)
    return cursor.fetchall()

def verificar_letra(conn, letra, palabra):
    return [pos for pos, char in enumerate(palabra) if char == letra]

def comparar_palabras(palabra_secreta, intento):
    resultado = ['_'] * len(palabra_secreta)
    for i, letra in enumerate(intento):
        if letra in palabra_secreta:
            resultado[i] = letra if palabra_secreta[i] == letra else '?'
    return ''.join(resultado)

def registrar_intentos(nombre_jugador: str, id_palabra: int, cantidad_intentos: int):
    conn = abrir_conexion()
    cursor = conn.cursor()
    
    consulta = f"""
    INSERT INTO intentos (nombre_jugador, id_palabra, cantidad_intentos)
    VALUES ('{nombre_jugador}', {id_palabra}, {cantidad_intentos})
    ON DUPLICATE KEY UPDATE cantidad_intentos = VALUES(cantidad_intentos);
    """
    
    cursor.execute(consulta)
    conn.commit()
    cursor.close()
    conn.close()
    
def obtener_top_jugadores() -> List[db.connection.RowType]:
    conn = abrir_conexion()
    cursor = conn.cursor()
    
    
    consulta = """
    SELECT nombre_jugador, AVG(cantidad_intentos) AS promedio_intentos, COUNT(DISTINCT id_palabra) AS palabras_adivinadas, COUNT(*) AS jugadas
    FROM jugadas
    GROUP BY nombre_jugador
    ORDER BY promedio_intentos ASC, palabras_adivinadas DESC
    LIMIT 10;
    """  
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return resultado