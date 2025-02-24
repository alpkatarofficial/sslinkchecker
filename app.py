import os
import ssl
import socket
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

def get_ssl_dates(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
            return not_before, not_after

@app.route('/check_ssl', methods=['GET'])
def check_ssl():
    url = request.args.get('url')
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
        return jsonify(response)
    else:
        return jsonify({'error': 'No URL provided'}), 400

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)