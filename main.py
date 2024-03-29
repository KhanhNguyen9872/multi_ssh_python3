#!/bin/python3
import threading, socket, os, sys, time
class bcolors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
def error(host,port,arg):
	print(f"{bcolors.RED}[!]{bcolors.YELLOW} {host}{bcolors.GREEN}:{bcolors.CYAN}{port} {bcolors.ENDC}| {bcolors.RED}{arg}{bcolors.ENDC}")
def no_error(host,port,arg):
	print(f"{bcolors.YELLOW}{host}{bcolors.GREEN}:{bcolors.CYAN}{port} {bcolors.ENDC}| {bcolors.GREEN}{arg}{bcolors.ENDC}")
def execute_ssh(host,port,username,password,command):
   password=password.replace("\n","")
   check=os.popen(f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{host} -p {port} whoami 2> /dev/null").read()
   if (check.replace("\n","") == ""):
   	error(host,port,"Username or Password ERROR")
   else:
      no_error(host,port,"Running....")
      pid=os.system(f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{host} -p {port} \"{command}\"")
      no_error(host,port,"Disconnected")
def check_ip(host,port,username,password):
   global command
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((host, int(port)))
   except:
      error(host,port,"Failed")
   else:
      s.close()
      no_error(host,port,"Online")
      if ("--test" in sys.argv):
      	pass
      else:
          while is_start==0:
            time.sleep(0.25)
          threading.Thread(target=execute_ssh, args=(host,port,username,password,command)).start()
   del s
global is_start
is_start=0
if (os.name == 'nt'):
	print("Windows is not supported!\n Use WSL/Docker or Linux to run it")
	exit()
else:
    check=os.popen("which sshpass").read()
    if (check.replace("\n","") == ""):
        print("Missing sshpass\nPlease install it first!")
        exit()
del sys.argv[0]
try:
    file1 = open('ip.txt', 'r')
except FileNotFoundError as e:
	print(e)
	exit()
Lines = file1.readlines()
file1.close()
if ("--test" in sys.argv):
	pass
else:
    try:
	    sys.argv[0] != ""
	    command=" ".join(sys.argv)
    except:
        command=str(input("Input command or file: "))
    if (command == ""):
        print("Need command or bash file!")
        exit()
    if os.path.isfile(command):
        print(f"{bcolors.CYAN} - Use file: {bcolors.YELLOW}{command}{bcolors.ENDC}")
        print(f"{bcolors.CYAN} - Uploading to SSH....{bcolors.ENDC}")
        check=os.popen(f"curl --upload-file {command} https://transfer.sh 2> /dev/null").read()
        if (check == ""):
            print(f"{bcolors.RED}[!] Network ERROR!")
            exit()
        else:
	        command=f"cd \$HOME; curl {check} -o run.sh 2> /dev/null; sudo bash ./run.sh"
    else:
        print(f"{bcolors.CYAN} - Use command: {bcolors.YELLOW}{command}{bcolors.ENDC}")
for line in Lines:
   info=line.split(" ")
   if (info != ""):
       threading.Thread(target=check_ip, args=(info)).start()
print(f"{bcolors.GREEN}Process will running after 5 seconds!{bcolors.ENDC}")
time.sleep(5)
is_start=1