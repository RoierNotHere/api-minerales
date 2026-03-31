from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json
import re # Importante para limpiar el texto

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = "https://www.inversoro.es/precio-del-oro/en-tiempo-real/onzas/USD/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            precio_element = soup.find("span", {"name": "current_price_field"})
            
            if precio_element:
                # 1. Obtenemos el texto sucio: "\n 4 674.53 € \n"
                texto_sucio = precio_element.text
                
                # 2. LIMPIEZA TOTAL: Solo dejamos números y el punto decimal
                # Quitamos espacios, símbolos de moneda y saltos de línea
                precio_limpio = re.sub(r'[^0-9.]', '', texto_sucio.replace(',', '.'))
                
                status = "success"
            else:
                precio_limpio = "2450.00"
                status = "No se encontro el elemento, usando respaldo"

        except Exception as e:
            precio_limpio = "0.00"
            status = str(e)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Ahora el JSON enviará: {"precio": "4674.53", "status": "success"}
        self.wfile.write(json.dumps({
            "precio": precio_limpio,
            "status": status
        }).encode())
        return
