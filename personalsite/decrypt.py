from cryptography.fernet import Fernet

def decrypt_file(encrypted, key):
    fernet = Fernet(key)

    decrypted = fernet.decrypt(bytes(encrypted, 'utf-8'))
    decrypted = decrypted.decode('utf-8')
    
    lines = []
    idx = 0

    while decrypted.find('\n') >= 0:
        idx = decrypted.find('\n')
        lines.append(decrypted[0:idx])
        decrypted = decrypted[idx+1:-1]
            
    lines.append(decrypted)

    return lines