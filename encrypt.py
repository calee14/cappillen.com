from cryptography.fernet import Fernet

def gen_key():
    key = Fernet.generate_key()

    with open('secretkey.key', 'wb') as filekey:
        filekey.write(key)

def encrypt_file(file):
    with open('secretkey.key', 'rb') as filekey:
        key = filekey.read()
    
    fernet = Fernet(key)

    with open(file, 'rb') as file:
        original = file.read()
    
    encrypted = fernet.encrypt(original)

    with open(file, 'wb') as encyrpted_file:
        encyrpted_file.write(encrypted)
