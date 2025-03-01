import sys
import os
import json
import time
import subprocess

FAILED_ATTEMPTS_FILE = "failed_attempts.json"
BLOCK_THRESHOLD = 5  # Nombre de tentatives avant blocage
TIME_WINDOW = 3600  # Fenêtre d'analyse (1 heure)
BAN_DURATION = 600  # Durée du blocage (10 minutes)

def load_failed_attempts():
    """Charge les tentatives échouées depuis le fichier JSON."""
    if os.path.exists(FAILED_ATTEMPTS_FILE):
        with open(FAILED_ATTEMPTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_failed_attempts(failed_attempts):
    """Sauvegarde les tentatives échouées dans le fichier JSON."""
    with open(FAILED_ATTEMPTS_FILE, 'w') as f:
        json.dump(failed_attempts, f)

def record_failed_attempt(ip, failed_attempts):
    """Ajoute une nouvelle tentative échouée pour une IP."""
    current_time = time.time()
    if ip not in failed_attempts:
        failed_attempts[ip] = []
    failed_attempts[ip].append(current_time)
    save_failed_attempts(failed_attempts)
    print(f"Recorded failed attempt for IP: {ip}")  # Ajout d'une impression de débogage

def check_failed_attempts(ip, failed_attempts):
    """Vérifie si l'IP dépasse le seuil et déclenche le blocage."""
    current_time = time.time()
    if ip in failed_attempts:
        failed_attempts[ip] = [t for t in failed_attempts[ip] if current_time - t < TIME_WINDOW]
        if len(failed_attempts[ip]) >= BLOCK_THRESHOLD:
            print(f"[SECURITY] Brute force detected for {ip}. Blocking...")
            block_ip(ip)

def block_ip(ip):
    """Bloque une IP en appelant le script block_ip.sh."""
    try:
        subprocess.run(['bash', 'scripts/block_ip.sh', ip], check=True)
        print(f"Blocked IP: {ip}")  # Ajout d'une impression de débogage
    except subprocess.CalledProcessError as e:
        print(f"Error blocking IP {ip}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 detect.py <IP>")
        sys.exit(1)

    ip_address = sys.argv[1]
    print(f"Checking failed attempts for IP: {ip_address}")
    failed_attempts = load_failed_attempts()
    record_failed_attempt(ip_address, failed_attempts)
    check_failed_attempts(ip_address, failed_attempts)

