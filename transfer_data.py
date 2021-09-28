from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import sys
import threading
import urllib.parse
import requests


class Handler(BaseHTTPRequestHandler):

    #data_base = {'datos.txt' : '54.57.44.21'}

    def _set_response(self, data):
        print("Por si las")

    def _upload_file(self, file_name,peerIp):
        self.send_response(200)
        self.end_headers()
        with open(file_name, 'rb') as file:
            self.wfile.write(file.read()) # Read the file and send the contents
        print("Aqui enviaremos el post o put para que me reciba el dato")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        help = "Hola del servidor - enviandiote informacion"
        #with open('/filepath/file.pdf', 'rb') as file:
         #   self.wfile.write(file.read()) # Read the file and send the contents
        return

    def do_POST(self):
        #r = requests.post("http://ec2-54-165-183-13.compute-1.amazonaws.com:3000")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = post_data.decode("utf_8")
        print(data)
        split_data = urllib.parse.unquote_plus(data).split('&')
        peerIp = urllib.parse.unquote_plus(split_data[1]).split('=')[1]
        print(peerIp)
        file_name = urllib.parse.unquote_plus(split_data[0]).split('=')[1]
        print(file_name)
        self._upload_file(file_name, peerIp)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    global data_base
    PORT = 3000
    server = ThreadedHTTPServer(('',PORT), Handler)
    print('Server running on port ', PORT)
    server.serve_forever()

if __name__ == "__main__":
    main()
