import requests
import urllib.request
import cmd
import os


def FILE(data):
    URL = "52.91.144.8"
    r = requests.post('http://'+ URL +':3000', data = {'url': data})
    print(f"{r.text}")
def UPLOAD(data):
    if not(os.path.isfile(data)) :
        print("This file dont exist in your data folder")
    else :
        URL = "52.91.144.8"
        external_ip =str(urllib.request.urlopen('https://ident.me').read().decode('utf8'))
        file_name = data #os.listdir()
        print(file_name)
        print(external_ip)
        #data = 'datos.txt'
        r = requests.post('http://'+ URL +':3000', data = {'upload': file_name, 'ip' : external_ip})
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
    main()
