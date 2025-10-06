#!/usr/bin/env python3
# ip_server.py
# Dipendenze: solo la stdlib + 'requests' (opzionale). Se non hai requests, il fallback usa urllib.

import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    import requests
except Exception:
    requests = None
    import urllib.request

HOST = "0.0.0.0"   # ascolta su tutte le interfacce
PORT = 8080        # porta pubblica (configurabile)

def get_public_ip():
    """Prova a ottenere l'IP pubblico via api.ipify.org; fallback a IP locale."""
    urls = [
        "https://api.ipify.org?format=json",
        "https://ifconfig.me/all.json"
    ]
    for url in urls:
        try:
            if requests:
                r = requests.get(url, timeout=3)
                r.raise_for_status()
                # api.ipify returns {"ip":"x.x.x.x"}
                data = r.json()
                ip = data.get("ip") or data.get("ip_addr")
                if ip:
                    return ip
            else:
                with urllib.request.urlopen(url, timeout=3) as resp:
                    body = resp.read().decode()
                    data = json.loads(body)
                    ip = data.get("ip") or data.get("ip_addr")
                    if ip:
                        return ip
        except Exception:
            continue
    # fallback: IP locale (non sempre pubblico, ma utile)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "unknown"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/ip"):
            ip = get_public_ip()
            payload = {"ip": ip, "port": PORT}
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # disabilita log troppo verbosi su stdout se vuoi
        print("%s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), format%args))

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Server in ascolto su {HOST}:{PORT} — endpoint /ip")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Arresto server...")
        server.server_close()
