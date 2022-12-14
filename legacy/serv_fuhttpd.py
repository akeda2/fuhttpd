#!/usr/bin/python3 -u
import ssl
import socket
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver
import argparse
import platform
import os

hostname = str(socket.gethostname())
httpsport=38443
httpport=38080
PORT = 38443
HOST = hostname
certpath=str(os.path.realpath("cert.pem"))
keypath=str(os.path.realpath("key.pem"))

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
parser.add_argument('-p', '--plain', action='store_true', default=False, help="Use plain HTTP")
args = parser.parse_args()
config = vars(args)
print(config)
dir = args.path

'''
if os.path.isdir(args.):
    dir = args.file.name
else:
    print("NO DIRECTORY")
    exit
'''


Handler = SimpleHTTPRequestHandler

if args.plain:
    PORT = httpport
    with socketserver.ThreadingTCPServer(("", PORT), Handler) as phttpd:
        print(HOST, str(PORT))
        if args.path:
            os.chdir(dir)
        phttpd.serve_forever()
else:
    PORT = httpsport
    with http.server.ThreadingHTTPServer(('0.0.0.0',PORT), Handler) as httpd:
        print(HOST, str(PORT))
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sslcontext.load_cert_chain(keyfile=keypath, certfile=certpath)
        httpd.socket = sslcontext.wrap_socket(httpd.socket, server_side=True)
        if args.path:
            os.chdir(dir)
        httpd.serve_forever()
