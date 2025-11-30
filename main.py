from config import load_config
from dolphin import Dolphin
from image_detector import ImageDetector
from server_client import ServerClient
import sys

SERVER_URL = "http://ksmg.lannionauth.com:5000"

cfg = load_config()
dolphin = Dolphin(cfg["memory"])

if not dolphin.hook():
    print("[Main] Failed to hook Dolphin. Exiting...")
    sys.exit(1)

client_name = cfg["network"]["uuid"]
server_client = ServerClient(dolphin, SERVER_URL, client_name)

# --- Image detection ---
TEMPLATES = {"0-hp": "0-hp.png"}

def on_detected(template_name):
    print(f"[FOUND {template_name}] reporting death")
    server_client.report_death()

detector = ImageDetector(TEMPLATES, callback=on_detected, fps=10, match_threshold=100)
detector.start()

# --- Main CLI ---
print("Shared death LAN tool running. Commands: 'd' = send death, 'q' = quit")
try:
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "d":
            server_client.report_death()
        elif cmd == "q":
            break
except KeyboardInterrupt:
    print("\n[Main] Exiting...")
finally:
    detector.running = False
    server_client.running = False
