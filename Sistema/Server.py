import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from typing import Tuple

from Traffic_Model import *

def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : p[2]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)

class Server(BaseHTTPRequestHandler):
    model = TrafficModel(2)
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)


    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.model.step()
        self._set_response()
        resp = "{\"positions\":" + positionsToJSON(self.model.positions) + "}"
        self.wfile.write(resp.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        self._set_response()
        resp = "{\"data\":" + positionsToJSON(self.model.positions) + "}"
        self.wfile.write(resp.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8585): # 8080 para IBM CLoud
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    run()