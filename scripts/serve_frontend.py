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
import http.server
import socketserver

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
        super().end_headers()

    def log_message(self, format, *args):
        # Concise logging for visibility
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]} {args[1]} -> {args[2]}\n")

def main():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), NoCacheHTTPRequestHandler) as httpd:
        print(f"=== StayMart No-Cache Frontend Server running on http://localhost:{PORT} ===", flush=True)
        print(f"Serving files from: {DIRECTORY}", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    main()

