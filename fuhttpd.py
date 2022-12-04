#!/usr/bin/python3 -u
import ssl
import socket
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver
import argparse
import platform
import os
from multiprocessing import Process

hostname = str(socket.gethostname())
HOST = hostname

# Default ports:
httpsport=38443
httpport=38080
PORT = httpsport

def isdir(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
def getdir(string):
    return os.getcwd()

parser = argparse.ArgumentParser(description="fuHTTPd",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('path', type=isdir, nargs='?', help="Root directory. If omitted - use current")
parser.add_argument('-P', '--plain', action='store_true', default=False, help="Use plain HTTP")
parser.add_argument('-p', '--port', type=int, help="Use custom port")
parser.add_argument('-d', '--dirlist', action='store_true', default=False, help="Allow directory listings")
args = parser.parse_args()
config = vars(args)
print(config)
dir = args.path

# Do we want to allow directory listing? If so, use default handler settings.
if args.dirlist:
    Handler = SimpleHTTPRequestHandler
else:
# If not, override with 404 on '/'-requests
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            # If the request is for a directory, return a 404 "Not Found" response
            if self.path.endswith("/"):
                self.send_error(404, "Not Found")
                return
        
            # Otherwise, use the default behavior for handling requests for files
            super().do_GET()

# Cert and key should be in the WorkingDirectory - NOT in webroot!
if not args.plain:
    certpath=str(os.path.realpath("cert.pem"))
    keypath=str(os.path.realpath("key.pem"))

if args.plain:
    # -P Plain HTTP server with no encryption
    if args.port:
        PORT = args.port
    else:
        PORT = httpport
    with socketserver.ThreadingTCPServer(('0.0.0.0', PORT), Handler) as phttpd:
        print(HOST, str(PORT))
        if args.path:
            os.chdir(dir)
        phttpd.serve_forever()
else:
    # HTTPS using ssl.SSLContext.wrap_socket()
    if args.port:
        PORT = args.port
    else:
        PORT = httpsport
    with http.server.ThreadingHTTPServer(('0.0.0.0',PORT), Handler) as httpd:
        print(HOST, str(PORT))
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sslcontext.load_cert_chain(keyfile=keypath, certfile=certpath)
        httpd.socket = sslcontext.wrap_socket(httpd.socket, server_side=True)
        if args.path:
            os.chdir(dir)
#        httpd.serve_forever()

    # Create a process for each CPU core
        for i in range(os.cpu_count()):
            p = Process(target=httpd.serve_forever)
            p.start()