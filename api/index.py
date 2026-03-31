from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Intentamos con una web muy estable
        url = "https://www.inversoro.es/precio-del-oro/en-tiempo-real/onzas/USD/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Buscamos el precio. Si falla el nombre, intentamos otro selector.
            precio_element = soup.find("span", {"name": "current_price_field"})
            
            if precio_element:
                precio_final = precio_element.text.replace(".", "").replace(",", ".")
                status = "success"
            else:
                # PLAN B: Si no lo encuentra, manda un valor fijo para que tu web no muera
                precio_final = "2550.75" 
                status = "Web cambio el diseño, usando respaldo"

        except Exception as e:
            precio_final = "0.00"
            status = str(e)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps({
            "precio": precio_final,
            "status": status
        }).encode())
        return
