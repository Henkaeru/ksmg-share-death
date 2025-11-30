import json
import uuid
import socket
from pathlib import Path

CFG_FILE = "shared_death_config.json"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def load_config():
    cfg = json.loads(Path(CFG_FILE).read_text())

    # Ensure UUID
    if "uuid" not in cfg["network"] or not cfg["network"]["uuid"]:
        cfg["network"]["uuid"] = str(uuid.uuid4())
        Path(CFG_FILE).write_text(json.dumps(cfg, indent=2))
        print("Added uuid to config:", cfg["network"]["uuid"])

    # Detect local IP
    cfg["network"]["local_ip"] = get_local_ip()

    return cfg
