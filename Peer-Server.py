from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import sys
import threading
import urllib.parse
import requests
import json

class Handler(BaseHTTPRequestHandler):

    #data_base = {'datos.txt' : '54.57.44.21'}

    def _set_response(self, data):
        global data_base
        value = ""
        if data in data_base:
            value = data_base.get(data)
        else :
            value = "There is not a peer with that data"
        print(value)
        self.send_response(200)
        self.end_headers()
        response = value.encode('ascii')
        self.wfile.write(response)

    def _add_Information(self, data):
        self.send_response(200)
        self.end_headers()
        #info = "The data of your files was Upload"
        #response = info.encode('ascii')
        #self.wfile.write(response)
        #print("Los datos que llegaron son : ")
        #print(data)
        if data[0] in data_base :
            if data_base[data[0]].find(data[1]) == -1:
                print("--------Adding new Peer to a file--------")
                data_base[data[0]] = data_base[data[0]]+ f",{data[1]}"
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data_base, f, ensure_ascii=False, indent=4)
            else :
                message = "\nYou already upload this file"
                response = message.encode('ascii')
                self.wfile.write(response)
        else :
            data_base[data[0]] = data[1]
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data_base, f, ensure_ascii=False, indent=4)
            info = "The file was Upload"
            response = info.encode('ascii')
            self.wfile.write(response)
        print("--------DATA BASE--------")
        print(data_base)

    def _upload_file(self, data):
        requests.post("http://ec2-54-226-205-132.compute-1.amazonaws.com:3000", {'data': data})

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
        split_data = urllib.parse.unquote_plus(data).split('&')
        #print("--------------SPLIT DATA---------------")
        #print(split_data)
        peer_ip = []
        #print("----------------Entro al for-------------")
        for i in split_data:
            print(i)
            peer_ip.append(i.split('=')[1])
        print(peer_ip)

        info = urllib.parse.unquote_plus(data).split('=')[0]
        url = urllib.parse.unquote_plus(data).split('=')[1]
        #print("SPLIT : ")
        #print(info)
        if info == 'upload':
            self._add_Information(peer_ip)
        else :
            print(url)
            #self._upload_file(data)
            self._set_response(url)
        #self.wfile.write("\n POST request for {}".format(self.path).encode('utf-8'))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

data_base = {}

def main():
    global data_base
    with open('data.json', 'r') as fp:
        data_base = json.load(fp)
    print("------------Iniciando con base de datos anterior------------")
    print(data_base)
    PORT = 3000
    server = ThreadedHTTPServer(('',PORT), Handler)
    print('Server running on port ', PORT)
    server.serve_forever()

if __name__ == "__main__":
    main()
