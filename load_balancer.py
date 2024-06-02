import http.server
import socketserver
import urllib.request

# List of backend servers
backend_servers = [
    'http://localhost:8000',
    'http://localhost:8001',
    'http://localhost:8002'
]

# Round-robin index
index = 0

class LoadBalancerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global index
        # Forward the request to the next backend server
        backend_url = backend_servers[index]
        index = (index + 1) % len(backend_servers)
        
        # Make a request to the backend server
        with urllib.request.urlopen(backend_url + self.path) as response:
            self.send_response(response.status)
            self.send_header('Content-type', response.getheader('Content-type'))
            self.end_headers()
            self.wfile.write(response.read())

def run(server_class=http.server.HTTPServer, handler_class=LoadBalancerHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting load balancer on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=8080)  # Port for the load balancer
