from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json
import re

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = "https://www.inversoro.es/precio-del-oro/en-tiempo-real/gramos/USD/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status() # Lanza error si la web no responde bien
            
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Buscamos el elemento por nombre
            tag_precio = soup.find("span", {"name": "current_price_field"})
            
            if tag_precio:
                precio_raw = tag_precio.get_text(strip=True)
                
                # Limpieza robusta:
                # 1. Quitamos el símbolo de dólar y espacios raros
                precio_limpio = precio_raw.replace("$", "").strip()
                # 2. Cambiamos el formato decimal (de 150,95 a 150.95)
                # OJO: Si el precio fuera "1.200,50", primero quitamos el punto de miles
                precio_limpio = precio_limpio.replace(".", "").replace(",", ".")
                
                status = "success"
            else:
                precio_limpio = "0.00"
                status = "No se encontró el selector en el HTML"

        except Exception as e:
            precio_limpio = "0.00"
            status = f"Error: {str(e)}"

        # Respuesta del servidor
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        output = {"precio": precio_limpio, "status": status}
        self.wfile.write(json.dumps(output).encode('utf-8'))