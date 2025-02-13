# wsgi.py
from app import make_wsgi_app
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

def create_app():
    return make_wsgi_app()

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Running server on port {port}...')
    httpd.serve_forever()


