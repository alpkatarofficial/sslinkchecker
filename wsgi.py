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

# Rest of your original app.py code stays exactly the same
def get_ssl_dates(hostname):
    # ... (your existing code)

class CustomHandler(SimpleHTTPRequestHandler):
    # ... (your existing code)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f'Running server on port {port}...')
    httpd.serve_forever()
