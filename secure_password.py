from cryptography.fernet import Fernet


def encrypt_pwd(password, fernet):
    enc_password = fernet.encrypt(password.encode())
    return enc_password


def decrypt_pwd(password, fernet):
    dec_password = fernet.decrypt(password).decode()
    return dec_password


if __name__ == '__main__':
    key = Fernet.generate_key()
    fernet = Fernet(key)
    pwd = encrypt_pwd("1234", fernet)
    print(pwd)
    print(decrypt_pwd(pwd, fernet))
