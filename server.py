#!/usr/bin/env python3
"""
Simple HTTP server to serve generated documentation
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve markdown and diagrams"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.environ.get('SERVE_DIR', '/output'), **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_GET(self):
        # Redirect root to index.md
        if self.path == '/':
            self.path = '/index.md'
        
        super().do_GET()


def main():
    port = int(os.environ.get('PORT', 8080))
    serve_dir = os.environ.get('SERVE_DIR', '/output')
    
    print(f"Serving directory: {serve_dir}")
    print(f"Server starting on port {port}...")
    print(f"Access at: http://localhost:{port}")
    
    with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()


if __name__ == '__main__':
    main()
