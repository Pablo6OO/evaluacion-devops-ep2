import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from validaciones import es_email_valido, normalizar_nombre

@pytest.mark.parametrize('email, esperado', [
    ('estudiante@duoc.cl', True),
    ('correo-invalido', False),
    ('', False),
])
def test_es_email_valido(email, esperado):
    assert es_email_valido(email) is esperado

def test_normalizar_nombre_ok():
    assert normalizar_nombre('  duoc ') == 'Duoc'

def test_normalizar_nombre_vacio():
    with pytest.raises(ValueError):
        normalizar_nombre('   ')