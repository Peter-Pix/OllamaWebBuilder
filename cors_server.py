import http.server
import socketserver
import urllib.request
import json

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/proxy/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Přeposlání požadavku na Ollama
                ollama_url = 'http://127.0.0.1:11434/api/generate'
                req = urllib.request.Request(ollama_url, data=post_data, headers={
                    'Content-Type': 'application/json'
                })
                
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(response_data)
                    
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = json.dumps({'error': str(e)})
                self.wfile.write(error_response.encode())
        else:
            super().do_POST()

PORT = 8000
with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    print(f"Server běží na http://localhost:{PORT}")
    print("Tento server řeší CORS problémy")
    httpd.serve_forever()