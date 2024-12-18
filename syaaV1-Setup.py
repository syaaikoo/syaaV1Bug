import sys
import subprocess
import pkg_resources
import importlib

required_packages = {
    'colorama': ['colorama', 'termcolor'],
    'tqdm': ['tqdm', 'progress'],
    'cryptography': ['cryptography', 'pycryptodome'],
    'requests': ['requests', 'urllib3']
}

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def install_packages(packages):
    for package, alternatives in packages.items():
        installed = False
        for alt in alternatives:
            try:
                pkg_resources.get_distribution(alt)
                print(f"{alt} sudah terinstal.")
                installed = True
                break
            except pkg_resources.DistributionNotFound:
                print(f"Mencoba menginstal {alt}...")
                if install_package(alt):
                    print(f"{alt} berhasil diinstal.")
                    installed = True
                    break
                else:
                    print(f"Gagal menginstal {alt}. Mencoba alternatif lain...")
        
        if not installed:
            print(f"PERINGATAN: gak bisa install paket {package} atau alternatifnya. beberapa fitur mungkin gak berfungsi.")

def install_instagram_module():
    instagram_modules = ['instaloader', 'instagram-scraper', 'instagram-python-scraper']
    for module in instagram_modules:
        try:
            importlib.import_module(module)
            print(f"{module} berhasil diinstal.")
            return module
        except ImportError:
            print(f"Mencoba menginstal {module}...")
            if install_package(module):
                print(f"{module} berhasil diinstal.")
                return module
    print("PERINGATAN: Tidak dapat menginstal modul Instagram. Fitur terkait mungkin tidak berfungsi.")
    return None

def setup():
    print("Memeriksa dan menginstal library yang dibutuhkan...")
    install_packages(required_packages)
    instagram_module = install_instagram_module()
    print("Selesai memeriksa dan menginstal library.")
    return instagram_module

if __name__ == "__main__":
    setup()
from simulasi_keren import ExploitSimulator

