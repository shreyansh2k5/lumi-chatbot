from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler

def keep_alive():
    server = HTTPServer(("0.0.0.0", 8080), SimpleHTTPRequestHandler)
    server.serve_forever()

def start():
    Thread(target=keep_alive).start()
