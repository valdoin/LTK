import subprocess
import sys

required_packages = ["requests", "beautifulsoup4"]

def install(package):
    subprocess.check_call([sys.executable, "pip", "install", package])

def check_and_install_packages(packages):
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Package {package} not found. Installing...")
            install(package)

check_and_install_packages(required_packages)