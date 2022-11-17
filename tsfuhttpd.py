import ssl
import socket
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver

hostname = str(socket.gethostname())
#hostname = 'localhost'
PORT = 38443
HOST = hostname
Handler = SimpleHTTPRequestHandler
with http.server.ThreadingHTTPServer(0.0.0.0',PORT), Handler) as httpd:
    print(HOST, str(PORT))
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslcontext.load_cert_chain(keyfile="key.pem", certfile="cert.pem")
    httpd.socket = sslcontext.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
