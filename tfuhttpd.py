import http.server
import socketserver

PORT = 38080

Handler = http.server.SimpleHTTPRequestHandler

with http.server.ThreadingHTTPServer(('0.0.0.0', PORT), Handler) as httpd:

	print("serving at port", PORT)
	httpd.serve_forever()
