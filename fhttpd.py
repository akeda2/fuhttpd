import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import ssl

PORT = 18080

httpd = HTTPServer(("", PORT), http.server.SimpleHTTPRequestHandler)#BaseHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
	keyfile="key.pem",
	certfile="cert.pem", server_side=True)

#Handler = http.server.SimpleHTTPRequestHandler

#with socketserver.TCPServer(("", PORT), Handler) as httpd:

print("serving at port", PORT)
httpd.serve_forever()
