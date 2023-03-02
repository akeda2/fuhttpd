#!/usr/bin/python3 -u
import ssl
import socket
import http.server
from http.server import HTTPServer, SimpleHTTPRequestHandler # BaseHTTPRequestHandler
#import socketserver
import argparse
import platform
import os
from multiprocessing import Process
import yaml
import signal
import sys

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

try:
    hostname = str(socket.gethostname())
    HOST = hostname

    # Default ports:
    httpsport=38443
    httpport=38080
    PORT = httpsport

    # Default paths:
    certpath = str(os.path.realpath("/usr/local/share/ca-certificates/cert.pem"))
    keypath = str(os.path.realpath("/usr/local/share/ca-certificates/key.pem"))

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
    parser.add_argument('-S', '--https', action='store_true', default=True, help="Use HTTPS")
    parser.add_argument('-p', '--port', type=int, help="Use custom port")
    parser.add_argument('-d', '--dirlist', action='store_true', default=False, help="Allow directory listings")
    parser.add_argument('-c', '--cert', type=str, help="Use certificate")
    parser.add_argument('-k', '--key', type=str, help="Use key")
    parser.add_argument('-s', '--save', action='store_true', default=False, help="Save config to file")
    parser.add_argument('-l', '--load', nargs='?', const='.fuhttpd.yaml', help="Load config from file")
    args = parser.parse_args()
    config = vars(args)
    print(config)
    

    # Load config from yaml file:
    if args.load and not args.save:
        print(args.load)
        config_path = args.load #os.path.normpath('.fuhttpd.yaml') if args.load else os.path.normpath('.fuhttpd.yaml')

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        certpath = args.cert if args.cert else config['cert']
        print(certpath)
        print(keypath)
        keypath = args.key if args.key else  config['key']
        args.plain = args.plain if args.plain else config['plain']
        args.dirlist = args.dirlist if args.dirlist else config['dirlist']
        args.path = args.path if args.path else config['path']
        args.port = args.port if args.port else config['port']
        print(config)
    dir = args.path
    # Save config to yaml file:
    if args.save:
        """if not args.dirlist:
            args.dirlist = input("Allow directory listings? (y/N): ") == 'y'
            print(str(args.dirlist))
            if args.dirlist == True:
                args.dirlist = True"""
        new_config = {
            'path': args.path or input("Path/Webroot: " + os.getcwd()) or os.getcwd(),
            'plain': args.plain or input("Use plain HTTP? (y/N): ") == 'y',
            'port': args.port or input('Port: (' + str(PORT) + ')') or PORT if not args.plain else input('Port: (' + str(httpport) + ')') or httpport,
            'dirlist': args.dirlist or input("Allow directory listings? (y/N): ") == 'y',
            'cert': args.cert or input("Certificate: (" + certpath + ")") or certpath,
            'key': args.key or input("Key: (" + keypath + ")") or keypath,
        }
        with open('.fuhttpd.yaml', 'w') as f:
            yaml.dump(new_config, f)
        exit(0)


    # Do we want to allow directory listing? If so, use default handler settings.
    if not args.dirlist:
        class Handler(SimpleHTTPRequestHandler):
    #        def do_LIST(self):
    #            pass
            def list_directory(self, path):
                self.send_error(404, "File not found")
    else:
        Handler = SimpleHTTPRequestHandler

    # This is changed! Certs are in /usr/local/share/ca-certificates/ as default!
    # Cert and key should be in the WorkingDirectory (default: /usr/local/bin/) - NOT in webroot!
    # I may change this and add an option for custom placement, but I don't need it now...
    """if not args.plain:
        certpath = os.path.normpath(args.cert) if args.cert else str(os.path.realpath("cert.pem")) 
        keypath = os.path.normpath(args.key) if args.key else str(os.path.realpath("key.pem"))"""

    if args.plain:
        # -P Plain HTTP server with no encryption
        if args.port:
            PORT = args.port
        else:
            PORT = httpport
        # Replaced socketserver.ThreadingTCPServer
        with http.server.ThreadingHTTPServer(('0.0.0.0', PORT), Handler) as phttpd:
            print(HOST, str(PORT))
            if args.path:
                os.chdir(dir)
    #        phttpd.serve_forever()

        # Create a process for each CPU core (or SMT thread):
            for i in range(os.cpu_count()):
                p = Process(target=phttpd.serve_forever)
                p.start()
    else:
        # HTTPS using ssl.SSLContext.wrap_socket():
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

        # Create a process for each CPU core (or SMT thread):
            for i in range(os.cpu_count()):
                p = Process(target=httpd.serve_forever)
                p.start()
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    sys.exit(0)