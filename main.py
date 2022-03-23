ver="v1.1.1"
import os
import time
import sys



reset="\x1b[0m"
bright="\x1b[1m"
dim="\x1b[2m"
underscore="\x1b[4m"
blink="\x1b[5m"
reverse="\x1b[7m"
hidden="\x1b[8m"

fgBlack="\x1b[30m"
fgRed="\x1b[31m"
fgGreen="\x1b[32m"
fgYellow="\x1b[33m"
fgBlue="\x1b[34m"
fgMagenta="\x1b[35m"
fgCyan="\x1b[36m"
fgWhite="\x1b[37m"

bgBlack="\x1b[40m"
bgRed="\x1b[41m"
bgGreen="\x1b[42m"
bgYellow="\x1b[43m"
bgBlue="\x1b[44m"
bgMagenta="\x1b[45m"
bgCyan="\x1b[46m"
bgWhite="\x1b[47m"

if os.system("curl https://raw.githubusercontent.com/2002Spiele/mc-mod-toggler/main/main.py --ssl-no-revoke > ./mcmodtoggler_update_thingy.txt 2>nul") != 0:
    # failed to curl (could happen when internet connection is missing)
    #time.sleep(5)
    print(bright+fgRed+"Failed to check for updates. (maybe internet connection is missing?)"+reset)
else:
    # file was downloaded
    time.sleep(1) # wait for a sec
    file=open("mcmodtoggler_update_thingy.txt") # open the file to read it
    filecontent=file.read() # reader
    file.close() # close it
    if len(filecontent.split("\n")) <= 1: # if the file has 1 or no lines in the code
        printatcenter(bright+fgRed+"Failed to check for updates ("+filecontent+")"+reset, 4)
    else:
        latestver=filecontent.split("\n")[0].split("=")[1][1:-1]
        if latestver!=ver:
            # if there are updates available
            print(bright+fgYellow+"There are updates available! Please restart."+reset)
            print(bright+fgYellow+"You're on "+ver+", and the latest version is "+latestver+"."+reset)
            os.system("del /q \""+sys.argv[0]+"\"")
            os.system("ren \"./mcmodtoggler_update_thingy.txt\" \""+sys.argv[0].split("\\")[-1]+"\"")
        else:
            # if there are no updates available
            os.system("del /q mcmodtoggler_update_thingy.txt")
            print(bright+fgGreen+"You're up-to-date! ("+ver+")"+reset)

time.sleep(3)

def getcmdresponse(cmd):
    os.system(cmd+">jeofajsso.txt")
    file=open("jeofajsso.txt", encoding='utf-8')
    content=file.read()
    file.close()
    os.system("del /q jeofajsso.txt")
    return content

mods=[]
while True:
    os.system("cls")
    if len(os.getcwd().split("\\")) < 3 or os.getcwd().split("\\")[1] != "Users":
        print("Please run this in your user folder, so I'm able to find your mods folder.")
        time.sleep(30)
        exit()
    while len(os.getcwd().split("\\")) > 3:
        os.chdir("..")
    os.chdir("AppData\\Roaming\\")
    try:
        os.chdir(".minecraft")
    except FileNotFoundError as err:
        print("Please start minecraft once before using this.")
        time.sleep(30)
        exit()
    try:
        os.chdir("mods")
    except FileNotFoundError:
        os.system("mkdir mods")
        time.sleep(1)
        os.chdir("mods")
    mods=[]
    modstartindex=0
    for mod in getcmdresponse("dir").split("\n"):
        if modstartindex==0 and ("<DIR>" in mod):
            if ".minecraft" in mod: continue
            if "." in mod[mod.index("<DIR>"):]:
                modstartindex=mod.index(" .")+1

    for mod in getcmdresponse("dir").split("\n"):
        if modstartindex==0:
            print("Something went wrong when fetching the mods.")
            time.sleep(10)
            break
        filename=mod[modstartindex:]
        try:
            open(filename).close()
            mods+=[filename]
        except Exception:
            os.getcwd()
    print("")
    print("Mods ("+os.getcwd()+"):")
    print("   ["+fgGreen+bright+"ON"+reset+"/"+fgRed+bright+"OFF"+reset+"/"+fgYellow+"UNKNOWN"+reset+"]")
    for mod in mods:
        if mod.endswith(".jar.deactivation"):
            print(" • "+bright+fgRed+".".join(mod.split(".")[:-2])+reset)
        elif mod.endswith(".jar"):
            print(" • "+bright+fgGreen+".".join(mod.split(".")[:-1])+reset)
        else:
            print(" • "+fgYellow+mod+reset)
    import sys
    print("")
    eeeee=input("Enter a mod name (short works too)\n> ")
    for mod in mods:
        if eeeee.lower() in mod.lower():
            if mod.endswith(".jar.deactivation"):
                if os.system("ren \""+mod+"\" \""+".".join(mod.split(".")[:-1])+"\"")!=0:
                    print("There was an error when enabling "+".".join(mod.split(".")[:-1]))
            elif mod.endswith(".jar"):
                if os.system("ren \""+mod+"\" \""+mod+"\".deactivation")!=0:
                    print("There was an error when disabling "+".".join(mod.split(".")[:-2]))
