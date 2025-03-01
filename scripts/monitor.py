import re
import subprocess
import time

LOG_FILE = "/var/log/auth.log"  # Chemin du fichier de logs

FAILURE_PATTERN = re.compile(r"Failed password for .* from (\d+\.\d+\.\d+\.\d+|::1|[a-fA-F0-9:]+:+[a-fA-F0-9]*)") # Regex pour extraire l'IP
def parse_log_line(line):
    """Extrait l'adresse IP d'une tentative de connexion échouée."""
    match = FAILURE_PATTERN.search(line)
    return match.group(1) if match else None

def process_log_line(line):
    """Analyse la ligne du log et déclenche la détection si nécessaire."""
    ip = parse_log_line(line)
    if ip:
        print(f"[ALERT] Failed login attempt from {ip}")
        subprocess.run(["python3", "scripts/detect.py", ip])  
def monitor_log():
    """Surveille en continu le fichier de logs pour détecter les échecs de connexion."""
    with open(LOG_FILE, "r") as log_file:
        log_file.seek(0, 2)  # Se positionner à la fin du fichier pour lire en temps réel
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(0.1)
                continue
            process_log_line(line)

def start_monitoring():
    """Démarre la surveillance des logs."""
    print(f"Monitoring {LOG_FILE} for failed login attempts...")
    try:
        monitor_log()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Error:{e}")
if __name__ == "__main__":
    start_monitoring()

