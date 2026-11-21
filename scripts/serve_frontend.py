#!/usr/bin/env python3
"""
scripts/serve_frontend.py
=============================================================================
StayMart High-Performance Live Development Server with Cache-Control Guards
=============================================================================
Serves frontend/ on port 5500 with:
- Cache-Control: no-store, no-cache, must-revalidate, max-age=0
- Pragma: no-cache
- Expires: 0
- Access-Control-Allow-Origin: *
Ensures browsers always receive the latest styles, scripts, and markup.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import http.server
import socketserver
import threading

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5500
DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With, Cache-Control")
        super().end_headers()

    def do_OPTIONS(self):
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()
        else:
            super().do_OPTIONS()

    def proxy_api(self):
        backend_url = f"http://127.0.0.1:8080{self.path}"
        # Filter out hop-by-hop headers, external origin, and host
        hop_by_hop = {
            'host', 'content-length', 'transfer-encoding', 'connection',
            'keep-alive', 'origin', 'referer', 'sec-fetch-site', 'sec-fetch-mode', 'sec-fetch-dest'
        }
        req_headers = {k: v for k, v in self.headers.items() if k.lower() not in hop_by_hop}
        # Provide local loopback origin so backend Spring Boot CORS always accepts the reverse-proxied request
        req_headers['Origin'] = 'http://127.0.0.1:5500'
        
        body = None
        if 'content-length' in self.headers:
            try:
                length = int(self.headers['content-length'])
                body = self.rfile.read(length)
            except Exception:
                body = None

        req = urllib.request.Request(backend_url, data=body, headers=req_headers, method=self.command)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                self.send_response(response.status)
                for header, val in response.getheaders():
                    if header.lower() not in ('transfer-encoding', 'content-encoding', 'connection', 'content-length'):
                        self.send_header(header, val)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
        except urllib.error.HTTPError as e:
            err_content = e.read()
            self.send_response(e.code)
            for header, val in e.headers.items():
                if header.lower() not in ('transfer-encoding', 'content-encoding', 'connection', 'content-length'):
                    self.send_header(header, val)
            self.send_header("Content-Length", str(len(err_content)))
            self.end_headers()
            self.wfile.write(err_content)
        except Exception as ex:
            err_json = json.dumps({"success": False, "message": f"API Gateway Proxy Error: {str(ex)}"}).encode('utf-8')
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(err_json)))
            self.end_headers()
            self.wfile.write(err_json)

    def do_GET(self):
        # Friendly route rewrites
        clean_p = self.path.split('?')[0].rstrip('/')
        qs = '?' + self.path.split('?')[1] if '?' in self.path else ''
        
        if clean_p in ('/properties', '/properties.html'):
            self.send_response(301)
            self.send_header('Location', f'/search-properties.html{qs}')
            self.end_headers()
            return
        elif clean_p in ('/products', '/products.html'):
            self.send_response(301)
            self.send_header('Location', f'/search-products.html{qs}')
            self.end_headers()
            return
        elif clean_p == '/login':
            self.send_response(301)
            self.send_header('Location', f'/login.html{qs}')
            self.end_headers()
            return
        elif clean_p == '/register':
            self.send_response(301)
            self.send_header('Location', f'/register.html{qs}')
            self.end_headers()
            return

        if self.path.startswith('/api/'):
            self.proxy_api()
        else:
            super().do_GET()

    def do_HEAD(self):
        if self.path.startswith('/api/'):
            self.proxy_api()
        else:
            super().do_HEAD()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self.proxy_api()
        else:
            self.send_error(405, "Method not allowed")

    def do_PUT(self):
        if self.path.startswith('/api/'):
            self.proxy_api()
        else:
            self.send_error(405, "Method not allowed")

    def do_PATCH(self):
        if self.path.startswith('/api/'):
            self.proxy_api()
        else:
            self.send_error(405, "Method not allowed")

    def do_DELETE(self):
        if self.path.startswith('/api/'):
            self.proxy_api()
        else:
            self.send_error(405, "Method not allowed")

    def log_message(self, format, *args):
        # Concise logging for visibility
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]} {args[1]} -> {args[2]}\n")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True
    request_queue_size = 512

def main():
    with ThreadedTCPServer(("0.0.0.0", PORT), NoCacheHTTPRequestHandler) as httpd:
        print(f"=== StayMart Multi-Threaded Frontend & API Proxy Server running on port {PORT} ===", flush=True)
        print(f"Serving files from: {DIRECTORY}", flush=True)
        print("Concurrent requests capacity: 512+ queued connections with dynamic worker threads", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    main()

