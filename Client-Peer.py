import requests
import urllib.request
import cmd
import os


def FILE(data):
    #global STATUS_ADDR
    #STATUS_ADDR = "http://ec2-3-85-36-56.compute-1.amazonaws.com:3000"
    #r = requests.post('http://ec2-3-85-36-56.compute-1.amazonaws.com:3000', data = {'url': url})
    #print(f"{r}")
    r = requests.post('http://ec2-52-91-144-8.compute-1.amazonaws.com:3000', data = {'url': data})
    print(f"{r.text}")
def UPLOAD(data):
    if os.getcwd()[-4] != 'data': 
        os.chdir(os.getcwd()+'/data')
    external_ip =str(urllib.request.urlopen('https://ident.me').read().decode('utf8'))
    dataxd = data #os.listdir()
    print(dataxd)
    print(external_ip)
    #data = 'datos.txt'
    r = requests.post('http://ec2-52-91-144-8.compute-1.amazonaws.com:3000', data = {'upload': dataxd, 'ip' : external_ip})
    print(f"{r.text}")

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

def main():
    shell = ShortyShell()
    try:
        shell.cmdloop()
    except Exception as e:
        print(f"Sorry, we were not expecting that. {e}")

 

if __name__ == "__main__":
    main()
