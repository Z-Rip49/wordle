import pytest
import wordle
from constantes import DB_TABLES

# Prueba si la función 'abrir_conexion' existe en el módulo 'wordle'
def test_abrir_conexion_existe():
    main_attrs = dir(wordle)
    assert 'abrir_conexion' in main_attrs

# Prueba si la función 'consulta_generica' existe en el módulo 'wordle'
def test_consulta_generica_existe():
    main_attrs = dir(wordle)
    assert 'consulta_generica' in main_attrs

# Prueba la función 'verificar_letra' con un caso básico
def test_verificar_letra():
    palabra = "hello"
    letra = "l"
    assert wordle.verificar_letra(None, letra, palabra) == [2, 3]

# Prueba la función 'comparar_palabras' con palabras iguales
def test_comparar_palabras_iguales():
    palabra_secreta = "python"
    intento = "python"
    assert wordle.comparar_palabras(palabra_secreta, intento) == "python"

# Prueba la función 'comparar_palabras' con una coincidencia parcial
def test_comparar_palabras_coincidencia_parcial():
    palabra_secreta = "python"
    intento = "p------"
    assert wordle.comparar_palabras(palabra_secreta, intento) == "python"

# Prueba la función 'registrar_intentos' con datos válidos
def test_registrar_intentos():
    nombre_jugador = "TestPlayer"
    id_palabra = 1
    cantidad_intentos = 5
    with pytest.raises(Exception):
        wordle.registrar_intentos(nombre_jugador, id_palabra, cantidad_intentos)

# Prueba la función 'obtener_top_jugadores'
def test_obtener_top_jugadores():
    assert isinstance(wordle.obtener_top_jugadores(), list)

# Se pueden agregar más pruebas según sea necesario
