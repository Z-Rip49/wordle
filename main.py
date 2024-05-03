from typing import List
import mysql.connector as db
import constantes
import random
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

def cargar_usuario(conn: db.MySQLConnection, id_usuario: int, nombre_usuario: str):
    """Carga un usuario en la tabla jugadores"""
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO jugadores (id, nombre) VALUES (%s, %s)", (id_usuario, nombre_usuario))
    conn.commit()
    print("Usuario cargado exitosamente.")

def jugador_existe_por_nombre(conn: db.MySQLConnection, nombre: str) -> bool:
    """Verifica si existe un jugador en la tabla jugadores por su nombre"""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jugadores WHERE nombre = %s", (nombre,))
    count = cursor.fetchone()[0]
    return count > 0

def obtener_palabras_jugadas(nombre_jugador: str) -> List[int]:
    """Obtiene una lista de los ids de las palabras que ya ha jugado un jugador"""
    conn = abrir_conexion()
    consulta = f"SELECT palabras.id FROM palabras JOIN jugadores ON palabras.id = jugadores.id WHERE jugadores.nombre = '{nombre_jugador}'"
    resultado = consulta_generica(conn, consulta)
    return [fila[0] for fila in resultado]

def obtener_palabra_aleatoria_no_jugada(conn: db.MySQLConnection, jugador_id: int) -> str:
    """Obtiene una palabra aleatoria que no haya sido jugada por el jugador"""
    palabras_jugadas = obtener_palabras_jugadas(conn, jugador_id)
    consulta = "SELECT palabra FROM palabras WHERE id NOT IN (SELECT palabra_id FROM jugadas WHERE jugador_id = %s)"
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta, (jugador_id,))
    palabras_disponibles = [resultado[0] for resultado in cursor.fetchall() if resultado[0] not in palabras_jugadas]
    return random.choice(palabras_disponibles) if palabras_disponibles else None

def insertar_registro(conn, valores):
    cursor = conn.cursor()
    consulta = "INSERT INTO jugadores (palabra, jugador, intentos) VALUES (%s, %s, %s)"
    cursor.execute(consulta, valores)
    conn.commit()

def actualizar_registro(conn, actualizaciones, condiciones):
    cursor = conn.cursor()
    consulta = "UPDATE jugadores SET {} WHERE {}".format(actualizaciones, condiciones)
    cursor.execute(consulta)
    conn.commit()

def obtener_registros(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT palabra, jugador, intentos FROM jugadores")
    return cursor.fetchall()
