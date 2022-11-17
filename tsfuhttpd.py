import ssl
import socket
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver
import argparse
import platform
import os

hostname = str(socket.gethostname())
#hostname = 'localhost'
PORT = 38443
HOST = hostname

parser = argparse.ArgumentParser(description="fuHTTPd",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('file', default=None, nargs='?', type=argparse.FileType('r'), help="Root directory, if omitted - use current")
args = parser.parse_args()
config = vars(args)
print(config)

if os.path.isdir(args.file.name):
    directory = args.file.name
else:
    print("NO DIRECTORY")
    exit

Handler = SimpleHTTPRequestHandler
with http.server.ThreadingHTTPServer(('0.0.0.0',PORT), Handler) as httpd:
    print(HOST, str(PORT))
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslcontext.load_cert_chain(keyfile="key.pem", certfile="cert.pem")
    httpd.socket = sslcontext.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
