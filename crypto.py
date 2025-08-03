from cryptography.fernet import Fernet

def generate():
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as archivo_clave:
        archivo_clave.write(clave)

def get():
    with open("clave.key", "rb") as archivo_clave:
        return archivo_clave.read()

def cod(password):
    clave = get()
    f = Fernet(clave)
    return f.encrypt(password.encode()).decode()

def decod(cifrada):
    clave = get()
    f = Fernet(clave)
    return f.decrypt(cifrada.encode()).decode()