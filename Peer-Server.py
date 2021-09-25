from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import sys
import threading
import urllib.parse
import requests


class Handler(BaseHTTPRequestHandler):

    #data_base = {'datos.txt' : '54.57.44.21'}

    def _set_response(self, data):
        global data_base
        value = ""
        if data in data_base:
            value = data_base.get(data)
        else :
            value = "There is not a peer with that dataThere is not a peer with that data"
        print(value)
        self.send_response(200)
        self.end_headers()
        response = value.encode('ascii')
        self.wfile.write(response)

    def _add_Information(self, data):
        print(data)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        help = "Hola del servidor - enviandote informacion"
        message = help.encode('ascii')
        self.wfile.write(message)
        return

    def do_POST(self):
        #r = requests.post("http://ec2-54-165-183-13.compute-1.amazonaws.com:3000")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = post_data.decode("utf_8")
        print(data)
        info = urllib.parse.unquote_plus(data).split('=')[0]
        url = urllib.parse.unquote_plus(data).split('=')[1]
        print(info)
        if info == 'upload':
            self._add_Information(url)
        print("-----------------------------//-----------")
        print(url)
        self._set_response(url)
        self.wfile.write("\n POST request for {}".format(self.path).encode('utf-8'))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

data_base = {'datos.txt' : 'url'}

def main():
    global data_base
    PORT = 3000
    server = ThreadedHTTPServer(('',PORT), Handler)
    print('Server running on port ', PORT)
    server.serve_forever()

if __name__ == "__main__":
    main()
