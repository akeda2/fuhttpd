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

def isdir(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
def getdir(string):
    return os.getcwd()

parser = argparse.ArgumentParser(description="fuHTTPd",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('path', type=isdir, nargs='?', help="Root directory if omitted - use current")
args = parser.parse_args()
config = vars(args)
print(config)
dir = args.path
os.chdir(dir)
'''
if os.path.isdir(args.):
    dir = args.file.name
else:
    print("NO DIRECTORY")
    exit
'''

Handler = SimpleHTTPRequestHandler
with http.server.ThreadingHTTPServer(('0.0.0.0',PORT), Handler) as httpd:
    print(HOST, str(PORT))
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslcontext.load_cert_chain(keyfile="key.pem", certfile="cert.pem")
    httpd.socket = sslcontext.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
