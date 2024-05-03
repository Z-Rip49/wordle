import pytest
import main

from constantes import DB_TABLES

def test_abrir_conexion_existe():
    main_attrs = dir(main)
    assert 'abrir_conexion' in main_attrs

def test_consulta_generica_existe():
    main_attrs = dir(main)
    assert 'consulta_generica' in main_attrs

def cargar_usuario(conn, nombre):
    conn.execute(f"INSERT INTO jugadores (nombre) VALUES ('{nombre}')")

@pytest.fixture
def db_setup():
    conn = None  
    yield conn      
    if conn is not None:
        conn.close()

def test_cargar_usuario(db_setup):
    conn = db_setup
    
    cargar_usuario(conn, 'NuevoJugador')
    result = conn.execute("SELECT * FROM jugadores WHERE nombre = 'NuevoJugador'").fetchone()
    assert result is not None
    assert result['nombre'] == 'NuevoJugador'

    
    with pytest.raises(Exception):
        cargar_usuario(conn, 'NuevoJugador')

def test_verificar_jugador_existente(db_setup):
    conn = db_setup
    
    main.cargar_usuario(conn, 'Blade')
    assert main.consulta_generica(f"SELECT * FROM {DB_TABLES['jugadores']} WHERE nombre = 'Blade'") is not None
    assert main.consulta_generica(f"SELECT * FROM {DB_TABLES['jugadores']} WHERE nombre = 'Satoru Gojo'") is None

def test_obtener_palabras_jugadas(conn):
    
    main.obtener_palabras_jugadas = conn(return_value=[1, 2, 3])
    palabras_jugadas = main.obtener_palabras_jugadas('Jugador1')
    assert palabras_jugadas == [1, 2, 3]
    main.obtener_palabras_jugadas.assert_called_once_with('Jugador1')

def test_obtener_palabra_al_azar(conn):
   
    main.obtener_palabras_jugadas = conn(return_value=[1, 2, 3])
    main.jugador_existe_por_nombre = conn(return_value=True)
    main.random.choice = conn(return_value="PalabraAlAzar")
    palabra = main.obtener_palabra_al_azar([1, 2, 3], "Jugador1")

   
    assert palabra == "PalabraAlAzar"

   
    main.obtener_palabras_jugadas.assert_called_once_with("Jugador1")
    main.jugador_existe_por_nombre.assert_called_once_with("Jugador1")
    main.random.choice.assert_called_once_with(["Palabra1", "Palabra2", "Palabra3"])
    
def test_insertar_registro(conn):
    # Insertar un registro y luego verificar si se puede recuperar correctamente
    valores = ("piedra", "usuario1", 3)
    main.insertar_registro(conn, valores)
    registros = main.obtener_registros(conn)
    assert valores in registros

def test_actualizar_registro(conn):
    # Insertar un registro, actualizarlo y luego verificar si se actualiza correctamente
    valores_iniciales = ("piedra", "usuario1", 3)
    valores_actualizados = ("papel", "usuario1", 5)
    main.insertar_registro(conn, valores_iniciales)
    main.actualizar_registro(conn, "palabra = %s, intentos = %s", "palabra = %s AND jugador = %s", valores_actualizados)
    registros = main.obtener_registros(conn)
    assert valores_iniciales not in registros
    assert valores_actualizados in registros

def test_obtener_registros(conn):
    # Insertar algunos registros y verificar si se recuperan correctamente
    registros_esperados = [("piedra", "usuario1", 3), ("papel", "usuario2", 5)]
    for valores in registros_esperados:
        main.insertar_registro(conn, valores)
    registros_obtenidos = main.obtener_registros(conn)
    for registro in registros_esperados:
        assert registro in registros_obtenidos