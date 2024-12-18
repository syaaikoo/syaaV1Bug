import random
import string
import socket
import importlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def get_crypto_library():
    try:
        return importlib.import_module('cryptography')
    except ImportError:
        try:
            return importlib.import_module('Crypto')
        except ImportError:
            raise ImportError("Tidak dapat mengimpor modul kriptografi. Pastikan 'cryptography' atau 'pycryptodome' terinstal.")

crypto = get_crypto_library()

class CryptoUtils:
    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_aes(data: str, key: bytes) -> str:
        iv = os.urandom(16)
        cipher = crypto.hazmat.primitives.ciphers.Cipher(crypto.hazmat.primitives.ciphers.algorithms.AES(key), crypto.hazmat.primitives.ciphers.modes.CBC(iv), backend=crypto.hazmat.backends.default_backend())
        encryptor = cipher.encryptor()
        padder = crypto.hazmat.primitives.padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return (iv + ciphertext).hex()

    @staticmethod
    def decrypt_aes(encrypted_data: str, key: bytes) -> str:
        data = bytes.fromhex(encrypted_data)
        iv = data[:16]
        ciphertext = data[16:]
        cipher = crypto.hazmat.primitives.ciphers.Cipher(crypto.hazmat.primitives.ciphers.algorithms.AES(key), crypto.hazmat.primitives.ciphers.modes.CBC(iv), backend=crypto.hazmat.backends.default_backend())
        decryptor = cipher.decryptor()
        unpadder = crypto.hazmat.primitives.padding.PKCS7(128).unpadder()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data.decode()

    @staticmethod
    def validate_token(token: str) -> bool:
        return len(token) == 32 and all(c in string.hexdigits for c in token)

class NetworkScanner:
    @staticmethod
    def scan_ports(target: str, port_range: range) -> list:
        open_ports = []
        for port in port_range:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        return open_ports

    @staticmethod
    def generate_random_ip() -> str:
        return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

    @staticmethod
    def generate_mac_address() -> str:
        return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])

class DataGenerator:
    @staticmethod
    def generate_random_string(length: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_phone_number() -> str:
        return f"+{random.randint(1, 999):03d}{random.randint(100000000, 999999999):09d}"

    @staticmethod
    def generate_email() -> str:
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        username = DataGenerator.generate_random_string(random.randint(5, 10))
        domain = random.choice(domains)
        return f"{username}@{domain}"

class SystemUtils:
    @staticmethod
    def get_system_info() -> dict:
        return {
            "os": "Arch-Linux",
            "version": "5.10.0-generic",
            "architecture": "x86_64",
            "hostname": "phantom-exploit-server",
            "cpu_cores": 8,
            "ram": "16GB",
            "disk_space": "500GB"
        }

    @staticmethod
    def generate_process_list() -> list:
        processes = [
            ("systemd", 1),
            ("kthreadd", 2),
            ("apache2", 1234),
            ("mysql", 5678),
            ("sshd", 9012),
            ("phantom_exploit", 3456)
        ]
        return [(name, pid + random.randint(-100, 100)) for name, pid in processes]

