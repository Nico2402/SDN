import http.server
import socketserver

class VulnerableServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Ejemplo de vulnerabilidad: manejo inseguro de rutas
        if self.path == "/admin":
            self.send_response(200)
            self.end_headers()
            response = "<h1>Panel de administración</h1>".encode('utf-8')
            self.wfile.write(response)
        else:
            # Respuesta estándar para otras rutas
            super().do_GET()

    def do_POST(self):
        # Ejemplo de vulnerabilidad: falta de validación en POST
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = f"<h1>Datos recibidos:</h1><p>{post_data.decode('utf-8')}</p>".encode('utf-8')
        self.wfile.write(response)

# Configurar el servidor
port = 8000  # Puerto donde se ejecutará el servidor (puedes cambiarlo si es necesario)

# Ejecutar el servidor
with socketserver.TCPServer(("", port), VulnerableServer) as httpd:
    print(f"Servidor vulnerable ejecutándose en el puerto {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
