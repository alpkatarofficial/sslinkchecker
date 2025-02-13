# wsgi.py
from app import CustomHandler, HTTPServer
import os

def create_app():
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    return httpd

app = create_app()

if __name__ == '__main__':
    print(f'Running server on port {port}...')
    app.serve_forever()
    
