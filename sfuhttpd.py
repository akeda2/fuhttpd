import ssl
import socket
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver

hostname = 'localhost'
PORT = 18443
HOST = hostname
Handler = http.server.SimpleHTTPRequestHandler
with http.server.HTTPServer((HOST,PORT), Handler) as httpd:
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslcontext.load_cert_chain(keyfile="key.pem", certfile="cert.pem")
    httpd.socket = sslcontext.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
