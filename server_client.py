import requests
import time
import threading

class ServerClient:
    def __init__(self, dolphin, server_url, client_name, poll_interval=0.3, cooldown=3.0):
        self.dolphin = dolphin
        self.server_url = server_url
        self.client_name = client_name
        self.poll_interval = poll_interval
        self.cooldown = cooldown

        self.last_sent_time = 0
        self.last_polled_time = 0
        self.last_server_timestamp = 0

        self.running = True
        threading.Thread(target=self._poll_loop, daemon=True).start()

    def report_death(self):
        now = time.time()
        if now - self.last_sent_time < self.cooldown:
            return
        try:
            requests.post(f"{self.server_url}/report_death", json={"source": self.client_name}, headers={"Connection": "close"}, timeout=2.0)
            self.last_sent_time = now
            print("[Client] Death reported to server")
        except Exception as e:
            print("Failed to report death:", e)

    def _poll_loop(self):
        while self.running:
            now = time.time()
            if now - self.last_sent_time < self.cooldown:
                time.sleep(self.poll_interval)
                continue
            try:
                resp = requests.get(f"{self.server_url}/check_death", params={"since": self.last_server_timestamp}, headers={"Connection": "close"}, timeout=2.0)
                data = resp.json()
                for ev in data.get("death_events", []):
                    ts = ev["timestamp"]
                    source = ev["source"]
                    if source != self.client_name:
                        self.dolphin.trigger_action()
                        self.last_sent_time = time.time()  # prevent immediate resend
                        print(f"[Client] Triggered action due to death by {source}")
                    self.last_server_timestamp = max(self.last_server_timestamp, ts)
            except Exception as e:
                print("Failed to poll server:", e)
            time.sleep(self.poll_interval)
