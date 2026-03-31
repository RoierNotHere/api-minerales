from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # La web de donde sacaremos el dato (puedes cambiarla luego)
        url = "https://www.inversoro.es/precio-del-oro/en-tiempo-real/onzas/USD/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            # Selector específico para el precio en esa web
            precio_raw = soup.find("span", {"name": "current_price_field"}).text
            precio_limpio = precio_raw.replace(".", "").replace(",", ".")
            status = "success"
        except Exception as e:
            precio_limpio = "0.00"
            status = str(e)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # Vital para que PHP lo lea
        self.end_headers()
        
        output = {"precio": precio_limpio, "status": status}
        self.wfile.write(json.dumps(output).encode())
        return