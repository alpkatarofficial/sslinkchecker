import os
import ssl
import socket
import logging
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

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
    app.logger.info(f"Received request to check SSL for URL: {url}")
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
            app.logger.info(f"SSL check successful for URL: {url}")
        except Exception as e:
            app.logger.error(f"Error checking SSL for URL: {url} - {str(e)}")
            response = {'valid': False, 'error': str(e)}
        return jsonify(response)
    else:
        app.logger.error("No URL provided")
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
