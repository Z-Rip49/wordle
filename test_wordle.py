import pytest
import wordle
from constantes import DB_TABLES

def test_abrir_conexion_existe():
    main_attrs = dir(wordle)
    assert 'abrir_conexion' in main_attrs

def test_consulta_generica_existe():
    main_attrs = dir(wordle)
    assert 'consulta_generica' in main_attrs