from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet, InvalidToken
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# metoda generująca klucz
def generate_key(password):

    # Convert to type bytes
    password = password.encode()

    salt1 = 'salt'.encode()

    # parametry klasy pbkdf2 do uzyskania klucza kryptograficznego
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=salt1,
        iterations=100000,
        backend=default_backend()
    )

    # generacja klucza z hasła i zamiana na znaki
    key = base64.urlsafe_b64encode(kdf.derive(password))
    file = open('key.key', 'wb')
    file.write(key)  # The key is type bytes still
    file.close()
    print("generated key!!")
    return key


# metoda szyfrująca przyjmująca plik tekstowy oraz haslo
def encrypt_file(input_file, password):

    # Stworzenie klucza na podstawie hasła
    key = generate_key(password)

    output_file = "test.encrypted"

    with open(input_file, 'rb') as f:
        data = f.read()
    print(len(data))

    # Tworzenie obiektu kryptograficznego na podstawie klucza
    fernet = Fernet(key)
    # Szyfrowanie tekstu z pliku
    encrypted = fernet.encrypt(data)
    print(len(encrypted))

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    print("file is encrypted!")
    return encrypted.decode('utf8')


#file decryption

def decrypt_file(message, password):

    # Tworzenie tego samego klucza do odkodowywania
    key = generate_key(password)

    output_file = '../data/hidden_message/secret.decrypted'

    # Tworzenie obiektu szyfrującego
    fernet = Fernet(key)

    # Odszyfrowywanie wraz ze sprawdzeniem czy hasło jest prawidłowe
    try:
        decrypted = fernet.decrypt(message.encode('utf8'))
    except (InvalidSignature, InvalidToken):
        return "Niewlasciwe haslo lub algorytm albo plik!\nSprawdz jeszcze raz!\nZamykam program"
    except:
        return "Nieoczekiwany blad"

    with open(output_file, 'wb') as f:
        f.write(decrypted)

    return "Odzyskana wiadomosc: " + output_file.split("/")[-1]
