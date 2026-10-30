import re

def es_email_valido(email: str) -> bool:
    if not email:
        return False
    patron = r"^[\w.-]+@[\w.-]+\.\w+$"
    return re.match(patron, email) is not None

def normalizar_nombre(nombre: str) -> str:
    if nombre is None or nombre.strip() == '':
        raise ValueError('El nombre no puede estar vacio')
    return nombre.strip().capitalize()