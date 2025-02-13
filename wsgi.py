# wsgi.py
from app import CustomHandler, HTTPServer, make_wsgi_app
import os

def create_app():
    return make_wsgi_app()

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f'Running server on port {port}...')
    httpd.serve_forever()




