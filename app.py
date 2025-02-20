import os
import ssl
import socket
from datetime import datetime, timezone, timedelta
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json
from wsgiref.simple_server import make_server

def get_ssl_dates(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
            return not_before, not_after

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/check_ssl'):
            query_components = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            url = query_components.get('url', [None])[0]
            if url:
                try:
                    established_date, expiry_date = get_ssl_dates(url)
                    remaining_time = expiry_date - datetime.now(timezone.utc)
                    valid = remaining_time >= timedelta(days=7)
                    months = remaining_time.days // 30
                    days = remaining_time.days % 30
                    response = {
                        'valid': valid,
                        'established_date': established_date.isoformat(),
                        'expiry_date': expiry_date.isoformat(),
                        'remaining_time': f"{months} months, {days} days",
                        'renew': remaining_time <= timedelta(days=7)
                    }
                except Exception as e:
                    response = {'valid': False, 'error': str(e)}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            super().do_GET()

def make_wsgi_app():
    def simple_app(environ, start_response):
        path = environ.get('PATH_INFO', '')
        if path.startswith('/check_ssl'):
            query_string = environ.get('QUERY_STRING', '')
            query_components = urlparse.parse_qs(query_string)
            url = query_components.get('url', [None])[0]
            if url:
                try:
                    established_date, expiry_date = get_ssl_dates(url)
                    remaining_time = expiry_date - datetime.now(timezone.utc)
                    valid = remaining_time >= timedelta(days=7)
                    months = remaining_time.days // 30
                    days = remaining_time.days % 30
                    response = {
                        'valid': valid,
                        'established_date': established_date.isoformat(),
                        'expiry_date': expiry_date.isoformat(),
                        'remaining_time': f"{months} months, {days} days",
                        'renew': remaining_time <= timedelta(days=7)
                    }
                except Exception as e:
                    response = {'valid': False, 'error': str(e)}
                status = '200 OK'
                headers = [('Content-type', 'application/json')]
                start_response(status, headers)
                return [json.dumps(response).encode()]
            else:
                status = '400 Bad Request'
                headers = [('Content-type', 'text/plain')]
                start_response(status, headers)
                return [b'Bad Request']
        else:
            status = '404 Not Found'
            headers = [('Content-type', 'text/plain')]
            start_response(status, headers)
            return [b'Not Found']

    return simple_app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f'Running server on port {port}...')
    httpd.serve_forever()
