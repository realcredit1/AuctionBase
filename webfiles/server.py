from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

# server on 0.0.0.0:8000
try:
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    print 'Serving on 127.0.0.1:8000'
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
