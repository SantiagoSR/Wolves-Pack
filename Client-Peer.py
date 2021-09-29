import requests
import urllib.request
import cmd
import os
import sys
import argparse

 

def FILE(data):
    r = requests.post('http://'+ SERVER +':3000', data = {'url': data})
    print(f"The following peers have that file: {r.text}")
    external_ip =str(urllib.request.urlopen('https://ident.me').read().decode('utf8'))
    ip_list = r.text.split(',')

 

    for ip in ip_list:
        try:
            with requests.post('http://'+ ip +':3000', data = {'file': data, 'peerIp': external_ip}) as r:
                r.raise_for_status()
                with open(data, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        #if chunk: 
                        f.write(chunk)
                        #print(f"{file_request.text}")
            print( f"Peer {ip} could transfer the file")
            break
            UPLOAD(data)
        except:
            e = sys.exc_info()[0]
            print( f"Peer {ip} currently unavailable - Error: {e} - Trying another peer")

 

def UPLOAD(data):
    if not(os.path.isfile(data)) :
        print("This file dont exist in your data folder")
    else :
        external_ip =str(urllib.request.urlopen('https://ident.me').read().decode('utf8'))
        file_name = data #os.listdir()
        print(file_name)
        print(external_ip)
        #data = 'datos.txt'
        r = requests.post('http://'+ SERVER +':3000', data = {'upload': file_name, 'ip' : external_ip})
        print(f"{r.text}")

 

        #with open(file_name, 'rb') as f:
            #r = requests.post('http://'+ URL +':3000', data = {file_name: f})

 

class ShortyShell(cmd.Cmd):
    intro = "Welcome to shorty, the URL shortner. \n Type help COMMAND_NAME to see further information about the command. \n Type bye to leave."
    prompt = "ShortyShell -> "
    file = None
    def do_FILE(self, arg):
        'Generates FILE based on URL: FILE <URL> '
        FILE(str(arg))
    def do_UPLOAD(self, args):
        'UPLOAD DATA FROM FOLDER'
        UPLOAD(str(args))
    def do_bye(self, arg):
        'Stop recording, close the turtle window, and exit:  BYE'
        print('Bye bye!')
        self.close()
        return True

 

def main():

 

    global SERVER

 

    if os.path.isdir("./data"):
        print("Directory alredy created")
    else :
        # Directory
        directory = "data"
        # Parent Directory path
        parent_dir = os.getcwd()
        # Path
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        print("Directory '% s' created" % directory)
    os.chdir(os.getcwd()+'/data')
    shell = ShortyShell()

 

 

    try:
        shell.cmdloop()
    except Exception as e:
        print(f"Sorry, we were not expecting that. {e}")

 

 

 

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Create a peer")
    parser.add_argument("--server", type=str, metavar="SERVER", default = '35.168.166.112', help="Central server IP or URL")

 

    args = parser.parse_args()

 

    SERVER = args.server

 

    main()
