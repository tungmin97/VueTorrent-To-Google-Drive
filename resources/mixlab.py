import os
import time
import uuid
import re
import IPython
import sys
import json
import ipywidgets as widgets
from sys import exit as exx
from subprocess import Popen, PIPE
from google.colab import files  # pylint: disable=import-error
from glob import glob
from IPython.display import HTML, display, clear_output

HOME = os.path.expanduser("~")
CWD = os.getcwd()

# ====================================================================================================


def createButton(name, *, func=None, style="", icon="check"):
    import ipywidgets as widgets  # pylint: disable=import-error

    button = widgets.Button(
        description=name, button_style=style, icon=icon, disabled=not bool(
            func)
    )
    button.style.font_weight = "900"
    button.on_click(func)
    output = widgets.Output()
    display(button, output)


def generateRandomStr():
    from uuid import uuid4

    return str(uuid4()).split("-")[0]


def accessSettingFile(file="", setting={}, v=True):
    from json import load, dump

    if not isinstance(setting, dict):
        if v:
            print("Could only accept Dictionary object!")
        exx()
    fullPath = f"/usr/local/sessionSettings/{file}"
    try:
        if not len(setting):
            if not checkAvailable(fullPath):
                if v:
                    print(f"File unavailable: {fullPath}.")
                exx()
            with open(fullPath) as jsonObj:
                return load(jsonObj)
        else:
            with open(fullPath, "w+") as outfile:
                dump(setting, outfile)
    except:
        if v:
            print(f"Error accessing the file: {fullPath}.")


def memGiB():
    from os import sysconf as _sc  # pylint: disable=no-name-in-module
    return _sc("SC_PAGE_SIZE") * _sc("SC_PHYS_PAGES") / (1024.0 ** 3)
# ====================================================================================================


def checkAvailable(path_="", userPath=False):
    from os import path as _p

    if path_ == "":
        return False
    else:
        return (
            _p.exists(path_)
            if not userPath
            else _p.exists(f"/usr/local/sessionSettings/{path_}")
        )


def displayUrl(data, btc='b', pNamU='URL : ', EcUrl=None, ExUrl=None, cls=True):
    from IPython.display import HTML, clear_output

    if cls:
        clear_output()
    showTxT = f'{pNamU}{data["url"]}'
    if EcUrl:
        showUrL = data["url"]+EcUrl
    elif ExUrl:
        showUrL = ExUrl
    else:
        showUrL = data["url"]
    if btc == 'b':
        # blue
        bttxt = 'hsla(210, 50%, 85%, 1)'
        btcolor = 'hsl(210, 80%, 42%)'
        btshado = 'hsla(210, 40%, 52%, .4)'
    elif btc == 'g':
        # green
        bttxt = 'hsla(110, 50%, 85%, 1)'
        btcolor = 'hsla(110, 86%, 56%, 1)'
        btshado = 'hsla(110, 40%, 52%, .4)'
    elif btc == 'r':
        # red
        bttxt = 'hsla(10, 50%, 85%, 1)'
        btcolor = 'hsla(10, 86%, 56%, 1)'
        btshado = 'hsla(10, 40%, 52%, .4)'

    return display(HTML('''<style>@import url('https://fonts.googleapis.com/css?family=Source+Code+Pro:200,900');  :root {   --text-color: '''+bttxt+''';   --shadow-color: '''+btshado+''';   --btn-color: '''+btcolor+''';   --bg-color: #141218; }  * {   box-sizing: border-box; } button { position:relative; padding: 10px 20px;     border: none;   background: none;   cursor: pointer;      font-family: "Source Code Pro";   font-weight: 900;   font-size: 100%;     color: var(--text-color);      background-color: var(--btn-color);   box-shadow: var(--shadow-color) 2px 2px 22px;   border-radius: 4px;    z-index: 0;     overflow: hidden;    }  button:focus {   outline-color: transparent;   box-shadow: var(--btn-color) 2px 2px 22px; }  .right::after, button::after {   content: var(--content);   display: block;   position: absolute;   white-space: nowrap;   padding: 40px 40px;   pointer-events:none; }  button::after{   font-weight: 200;   top: -30px;   left: -20px; }   .right, .left {   position: absolute;   width: 100%;   height: 100%;   top: 0; } .right {   left: 66%; } .left {   right: 66%; } .right::after {   top: -30px;   left: calc(-66% - 20px);      background-color: var(--bg-color);   color:transparent;   transition: transform .4s ease-out;   transform: translate(0, -90%) rotate(0deg) }  button:hover .right::after {   transform: translate(0, -47%) rotate(0deg) }  button .right:hover::after {   transform: translate(0, -50%) rotate(-7deg) }  button .left:hover ~ .right::after {   transform: translate(0, -50%) rotate(7deg) }  /* bubbles */ button::before {   content: '';   pointer-events: none;   opacity: .6;   background:     radial-gradient(circle at 20% 35%,  transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),     radial-gradient(circle at 75% 44%, transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),     radial-gradient(circle at 46% 52%, transparent 0, transparent 4px, var(--text-color) 5px, var(--text-color) 6px, transparent 6px);    width: 100%;   height: 300%;   top: 0;   left: 0;   position: absolute;   animation: bubbles 5s linear infinite both; }  @keyframes bubbles {   from {     transform: translate();   }   to {     transform: translate(0, -66.666%);   } }    Resources</style><center><a href="'''+showUrL+'''" target="_blank"><div style="width: 570px;   height: 80px; padding-top:15px"><button style='--content: "'''+showTxT+'''";'">   <div class="left"></div>'''+showTxT+'''<div class="right"></div> </div></button></a></center>'''))


def findProcess(process, command="", isPid=False):
    from psutil import pids, Process

    if isinstance(process, int):
        if process in pids():
            return True
    else:
        for pid in pids():
            try:
                p = Process(pid)
                if process in p.name():
                    for arg in p.cmdline():
                        if command in str(arg):
                            return True if not isPid else str(pid)
                        else:
                            pass
                else:
                    pass
            except:
                continue


def installArgoTunnel():
    if checkAvailable(f"{HOME}/tools/argotunnel/cloudflared"):
        return
    else:
        import os
        from shutil import unpack_archive
        from urllib.request import urlretrieve

        os.makedirs(f'{HOME}/tools/argotunnel/', exist_ok=True)
        aTURL = findPackageR("cloudflare/cloudflared",
                             "cloudflared-linux-amd64")
        urlretrieve(aTURL, f'{HOME}/tools/argotunnel/cloudflared')
        # unpack_archive('cloudflared.tgz',
        #   f'{HOME}/tools/argotunnel')
        os.chmod(f'{HOME}/tools/argotunnel/cloudflared', 0o755)
        # os.unlink('cloudflared.tgz')


def runSh(args, *, output=False, shell=False, cd=None):
    import subprocess
    import shlex

    if not shell:
        if output:
            proc = subprocess.Popen(
                shlex.split(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cd
            )
            while True:
                output = proc.stdout.readline()
                if output == b"" and proc.poll() is not None:
                    return
                if output:
                    print(output.decode("utf-8").strip())
        return subprocess.run(shlex.split(args), cwd=cd).returncode
    else:
        if output:
            return (
                subprocess.run(
                    args,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=cd,
                )
                .stdout.decode("utf-8")
                .strip()
            )
        return subprocess.run(args, shell=True, cwd=cd).returncode


def loadingAn(name="cal"):
    from IPython.display import HTML

    if name == "cal":
        return display(HTML('<style>.lds-ring {   display: inline-block;   position: relative;   width: 34px;   height: 34px; } .lds-ring div {   box-sizing: border-box;   display: block;   position: absolute;   width: 34px;   height: 34px;   margin: 4px;   border: 5px solid #cef;   border-radius: 50%;   animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;   border-color: #cef transparent transparent transparent; } .lds-ring div:nth-child(1) {   animation-delay: -0.45s; } .lds-ring div:nth-child(2) {   animation-delay: -0.3s; } .lds-ring div:nth-child(3) {   animation-delay: -0.15s; } @keyframes lds-ring {   0% {     transform: rotate(0deg);   }   100% {     transform: rotate(360deg);   } }</style><div class="lds-ring"><div></div><div></div><div></div><div></div></div>'))
    elif name == "lds":
        return display(HTML('''<style>.lds-hourglass {  display: inline-block;  position: relative;  width: 34px;  height: 34px;}.lds-hourglass:after {  content: " ";  display: block;  border-radius: 50%;  width: 34px;  height: 34px;  margin: 0px;  box-sizing: border-box;  border: 20px solid #dfc;  border-color: #dfc transparent #dfc transparent;  animation: lds-hourglass 1.2s infinite;}@keyframes lds-hourglass {  0% {    transform: rotate(0);    animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);  }  50% {    transform: rotate(900deg);    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);  }  100% {    transform: rotate(1800deg);  }}</style><div class="lds-hourglass"></div>'''))


def textAn(TEXT, ty='d'):
    from IPython.display import HTML

    if ty == 'd':
        return display(HTML('''<style>@import url(https://fonts.googleapis.com/css?family=Raleway:400,700,900,400italic,700italic,900italic);#wrapper {   font: 17px 'Raleway', sans-serif;animation: text-shadow 1.5s ease-in-out infinite;    margin-left: auto;    margin-right: auto;    }#container {    display: flex;    flex-direction: column;    float: left;     }@keyframes text-shadow { 0% 20% {          transform: translateY(-0.1em);        text-shadow:             0 0.1em 0 #0c2ffb,             0 0.1em 0 #2cfcfd,             0 -0.1em 0 #fb203b,             0 -0.1em 0 #fefc4b;    }    40% {          transform: translateY(0.1em);        text-shadow:             0 -0.1em 0 #0c2ffb,             0 -0.1em 0 #2cfcfd,             0 0.1em 0 #fb203b,             0 0.1em 0 #fefc4b;    }       60% {        transform: translateY(-0.1em);        text-shadow:             0 0.1em 0 #0c2ffb,             0 0.1em 0 #2cfcfd,             0 -0.1em 0 #fb203b,             0 -0.1em 0 #fefc4b;    }   }@media (prefers-reduced-motion: reduce) {    * {      animation: none !important;      transition: none !important;    }}</style><div id="wrapper"><div id="container">'''+TEXT+'''</div></div>'''))
    elif ty == 'twg':
        textcover = str(len(TEXT)*0.55)
        return display(HTML('''<style>@import url(https://fonts.googleapis.com/css?family=Anonymous+Pro);.line-1{font-family: 'Anonymous Pro', monospace;    position: relative;   border-right: 1px solid;    font-size: 15px;   white-space: nowrap;    overflow: hidden;    }.anim-typewriter{  animation: typewriter 0.4s steps(44) 0.2s 1 normal both,             blinkTextCursor 600ms steps(44) infinite normal;}@keyframes typewriter{  from{width: 0;}  to{width: '''+textcover+'''em;}}@keyframes blinkTextCursor{  from{border-right:2px;}  to{border-right-color: transparent;}}</style><div class="line-1 anim-typewriter">'''+TEXT+'''</div>'''))


class ArgoTunnel:
    def __init__(self, port, proto='http', metrics=49589, interval=30, retries=30):
        import os
        filePath = "/usr/local/sessionSettings/argotunnelDB.json"
        if not os.path.exists(filePath):
            os.makedirs(filePath[:-17], exist_ok=True)
            open(filePath, 'w').close()

        # Installing argotunnel
        installArgoTunnel()

        self.connection = None
        self.proto = proto
        self.port = port
        self.metricPort = metrics
        self.interval = interval
        self.retries = retries

    # def start(self):
    #   if self.connection:self.connection.kill()
    #   # self.connection=Popen(f"ssh -R 80:localhost:{self.port} {self.id}@ssh.localhost.run -o StrictHostKeyChecking=no".split(), stdout=PIPE, stdin=PIPE)
    #   self.connection=Popen(f"/content/tools/argotunnel/cloudflared tunnel --url {self.proto}://0.0.0.0:{self.port} --logfile cloudflared.log".split(), stdout=PIPE, stdin=PIPE)
    #   try:
    #     return re.findall("https://(.*?.trycloudflare.com)",self.connection.stdout.readline().decode("utf-8"))[0]
    #   except:
    #     raise Exception(self.connection.stdout.readline().decode("utf-8"))

    def keep_alive(self):
        # if self.connection:self.connection.kill()
        import urllib
        import requests
        import re
        from urllib.error import HTTPError

        try:
            argotunnelOpenDB = dict(
                accessSettingFile("argotunnelDB.json", v=False))
        except TypeError:
            argotunnelOpenDB = dict()

        if findProcess("cloudflared", f"localhost:{self.metricPort}"):
            try:
                oldAddr = argotunnelOpenDB[str(self.port)]
                if requests.get("http://"+oldAddr).status_code == 200:
                    return oldAddr
            except:
                pass

        self.connection = Popen(f"{HOME}/tools/argotunnel/cloudflared tunnel --url {self.proto}://0.0.0.0:{self.port} --logfile {HOME}/tools/argotunnel/cloudflared.log --metrics localhost:{self.metricPort}".split(),
                                stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)

        time.sleep(5)

        hostname = None
        for i in range(20):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{self.metricPort}/metrics") as response:
                    hostname = re.search(r'userHostname=\"https://(.+)\"',
                                         response.read().decode('utf-8'), re.MULTILINE)
                    if not hostname:
                        time.sleep(1)
                        continue
                    hostname = hostname.group(1)
                    break
            except HTTPError:
                time.sleep(2)

        if not hostname:
            raise RuntimeError("Failed to get user hostname from cloudflared")

        argotunnelOpenDB[str(self.port)] = hostname
        accessSettingFile("argotunnelDB.json", argotunnelOpenDB, v=False)
        return hostname

    def kill(self):
        self.connection.kill()


class jprq:
    def __init__(self, port, proto='http', ids=None):
        import os
        import uuid
        filePath = "/usr/local/sessionSettings/jprqDB.json"
        if not os.path.exists(filePath):
            os.makedirs(filePath[:-11], exist_ok=True)
            open(filePath, 'w').close()

        if not ids:
            self.ids = str(uuid.uuid4())[:12]

        # Installing the jprq module
        runSh("pip install jprq")
        runSh("pip install jprq --upgrade")

        self.connection = None
        self.proto = proto
        self.port = port

    def keep_alive(self):
        # if self.connection:self.connection.kill()
        import urllib
        import requests
        import re
        try:
            jprqOpenDB = dict(accessSettingFile("jprqDB.json", v=False))
        except TypeError:
            jprqOpenDB = dict()

        if findProcess("jprq", f"{self.port}"):
            try:
                oldAddr = jprqOpenDB[str(self.port)]
                if requests.get("http://"+oldAddr).status_code == 200:
                    return oldAddr
            except:
                pass
        hostname = f"mixlab-{self.ids}"
        self.connection = Popen(f"jprq -s {hostname} {self.port}".split(),
                                stdout=PIPE, stdin=PIPE, stderr=PIPE)

        time.sleep(3)

        # try:
        #   return re.findall("https://(.*?.jprq.live/)", self.connection.stdout.readline().decode("utf-8"))[0]
        # except:
        #   raise Exception(self.connection.stdout.readline().decode("utf-8"))
        hostname += ".jprq.live"
        jprqOpenDB[str(self.port)] = hostname
        accessSettingFile("jprqDB.json", jprqOpenDB, v=False)
        return hostname

    def kill(self):
        self.connection.kill()


class PortForward:
    def __init__(self, connections, region=None, SERVICE="localhost", TOKEN=None, USE_FREE_TOKEN=None, config=None):
        c = dict()
        for con in connections:
            c[con[0]] = dict(port=con[1], proto=con[2])
        self.connections = c
        if config:
            config[1] = closePort(config[1])
        self.config = config
        if SERVICE == "ngrok":
            self.ngrok = ngrok(TOKEN, USE_FREE_TOKEN,
                               connections, region, self.config)
        self.SERVICE = SERVICE

    def start(self, name, btc='b', displayB=True, v=True):
        from IPython.display import clear_output

        if self.SERVICE == "localhost":
            con = self.connections[name]
            port = con["port"]
            proto = con["proto"]
            if(proto == "tcp"):
                return self.ngrok.start(name, btc, displayB, v)
            else:
                if v:
                    clear_output()
                    loadingAn(name="lds")
                    textAn("Preparing localhost...", ty="twg")
                data = dict(url="https://"+LocalhostRun(port).keep_alive())
                if displayB:
                    displayUrl(data, btc)
                return data
        elif self.SERVICE == "ngrok":
            return self.ngrok.start(name, btc, displayB, v)
        elif self.SERVICE == "argotunnel":
            con = self.connections[name]
            port = con["port"]
            proto = con["proto"]
            if v:
                clear_output()
                loadingAn(name="lds")
                textAn("Preparing argo tunnel...", ty="twg")
            data = dict(url="https://"+ArgoTunnel(port, proto,
                        closePort(self.config[1])).keep_alive())
            if displayB:
                displayUrl(data, btc)
            return data
        elif self.SERVICE == "jprq":
            con = self.connections[name]
            port = con["port"]
            proto = con["proto"]
            if v:
                clear_output()
                loadingAn(name="lds")
                textAn("Preparing jprq...", ty="twg")
            data = dict(url="https://"+jprq(port, proto).keep_alive())
            if displayB:
                displayUrl(data, btc)
            return data


class PortForward_wrapper(PortForward):
    def __init__(self, SERVICE, TOKEN, USE_FREE_TOKEN, connections, region, config):
        super(self.__class__, self).__init__(connections,
                                             region, SERVICE, TOKEN, USE_FREE_TOKEN, config)


def findPackageR(id_repo, p_name, tag_name=False, all_=False):
    import requests

    for rawData in requests.get(f"https://api.github.com/repos/{id_repo}/releases").json():
        if tag_name:
            if rawData['tag_name'] != tag_name:
                continue

        for f in rawData['assets']:
            if p_name == f['browser_download_url'][-len(p_name):]:
                rawData['assets'] = f
                return f['browser_download_url'] if not all_ else rawData
    raise Exception(
        "Unable to call API!\n Try again with change packages name")


def closePort(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        for _ in range(100):
            if s.connect_ex(('localhost', port)) == 0:
                port += 1
            else:
                return port
    raise Exception("Unable to close port!")

# ====================================================================================================


def installJDownloader():
    if checkAvailable("/root/.JDownloader/JDownloader.jar"):
        return
    else:
        runSh("mkdir -p -m 666 /root/.JDownloader/libs")
        runSh("apt-get install openjdk-8-jre-headless -qq -y")
        runSh(
            "wget -q http://installer.jdownloader.org/JDownloader.jar -O /root/.JDownloader/JDownloader.jar"
        )
        runSh("java -jar /root/.JDownloader/JDownloader.jar -norestart -h")
        runSh(
            "wget -q https://shirooo39.github.io/MiXLab/resources/packages/jdownloader/sevenzipjbinding1509.jar -O /root/.JDownloader/libs/sevenzipjbinding1509.jar"
        )
        runSh(
            "wget -q https://shirooo39.github.io/MiXLab/resources/packages/jdownloader/sevenzipjbinding1509Linux.jar -O /root/.JDownloader/libs/sevenzipjbinding1509Linux.jar"
        )


Email = widgets.Text(placeholder="*Required", description="Email:")
Password = widgets.Text(placeholder="*Required", description="Password:")
Device = widgets.Text(placeholder="Optional", description="Name:")
SavePath = widgets.Dropdown(
    value="/content/downloads",
    options=["/content", "/content/downloads"],
    description="Save Path:",
)


def refreshJDPath(a=1):
    if checkAvailable("/content/drive/"):
        if checkAvailable("/content/drive/Shareddrives/"):
            SavePath.options = (
                ["/content", "/content/Downloads", "/content/drive/MyDrive"]
                + glob("/content/drive/MyDrive/*/")
                + glob("/content/drive/Shareddrives/*/")
            )
        else:
            SavePath.options = [
                "/content",
                "/content/downloads",
                "/content/drive/MyDrive",
            ] + glob("/content/drive/MyDrive/*/")
    else:
        SavePath.options = ["/content", "/content/downloads"]


def exitJDWeb():
    runSh("pkill -9 -e -f java")
    clear_output(wait=True)
    createButton("Start", func=startJDService, style="info")


def confirmJDForm(a):
    clear_output(wait=True)
    action = a.description
    createButton(f"{action} Confirm?")
    if action == "Restart":
        createButton("Confirm", func=startJDService, style="danger")
    else:
        createButton("Confirm", func=exitJDWeb, style="danger")
    createButton("Cancel", func=displayJDControl, style="warning")


def displayJDControl(a=1):
    clear_output(wait=True)
    createButton("Control Panel")
    display(
        HTML(
            """
            <h3 style="font-family:Trebuchet MS;color:#4f8bd6;">
                You can login to the WebUI by clicking
                    <a href="https://my.jdownloader.org/" target="_blank">
                        here
                    </a>.
            </h3>
            """
        ),
        HTML(
            """
            <h4 style="font-family:Trebuchet MS;color:#4f8bd6;">
                If the server didn't showup in 30 sec. please re-login.
            </h4>
            """
        ),
    )
    createButton("Re-Login", func=displayJDLoginForm, style="info")
    createButton("Restart", func=confirmJDForm, style="warning")
    createButton("Exit", func=confirmJDForm, style="danger")


def startJDService(a=1):
    runSh("pkill -9 -e -f java")
    runSh(
        "java -jar /root/.JDownloader/JDownloader.jar -norestart -noerr -r &",
        shell=True,  # nosec
    )
    displayJDControl()


def displayJDLoginForm(a=1):
    clear_output(wait=True)
    Email.value = ""
    Password.value = ""
    Device.value = ""
    refreshJDPath()
    display(
        HTML(
            """
            <h3 style="font-family:Trebuchet MS;color:#4f8bd6;">
                If you don't have an account yet, please register
                    <a href="https://my.jdownloader.org/login.html#register" target="_blank">
                        here
                    </a>.
            </h3>
            """
        ),
        HTML("<br>"),
        Email,
        Password,
        Device,
        SavePath,
    )
    createButton("Refresh", func=refreshJDPath)
    createButton("Login", func=startJDFormLogin, style="info")
    if checkAvailable(
        "/root/.JDownloader/cfg/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json"
    ):
        createButton("Cancel", func=displayJDControl, style="danger")


def startJDFormLogin(a=1):
    try:
        if not Email.value.strip():
            ERROR = "Email field is empty."
            THROW_ERROR
        if not "@" in Email.value and not "." in Email.value:
            ERROR = "Email is an incorrect format."
            THROW_ERROR
        if not Password.value.strip():
            ERROR = "Password field is empty."
            THROW_ERROR
        if not bool(re.match("^[a-zA-Z0-9]+$", Device.value)) and Device.value.strip():
            ERROR = "Only alphanumeric are allowed for the device name."
            THROW_ERROR
        clear_output(wait=True)
        if SavePath.value == "/content":
            savePath = {"defaultdownloadfolder": "/content/downloads"}
        elif SavePath.value == "/content/downloads":
            runSh("mkdir -p -m 666 /content/downloads")
            savePath = {"defaultdownloadfolder": "/content/downloads"}
        else:
            savePath = {"defaultdownloadfolder": SavePath.value}

        with open(
            "/root/.JDownloader/cfg/org.jdownloader.settings.GeneralSettings.json", "w+"
        ) as outPath:
            json.dump(savePath, outPath)
        if Device.value.strip() == "":
            Device.value = Email.value
        runSh("pkill -9 -e -f java")
        data = {
            "email": Email.value,
            "password": Password.value,
            "devicename": Device.value,
            "directconnectmode": "LAN",
        }
        with open(
            "/root/.JDownloader/cfg/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json",
            "w+",
        ) as outData:
            json.dump(data, outData)
        startJDService()
    except:
        print(ERROR)


def handleJDLogin(newAccount):
    installJDownloader()
    if newAccount:
        displayJDLoginForm()
    else:
        data = {
            "email": "daniel.dungngo@gmail.com",
            "password": "ZjPNiqjL4e6ckwM",
            "devicename": "daniel.dungngo@gmail.com",
            "directconnectmode": "LAN",
        }
        with open(
            "/root/.JDownloader/cfg/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json",
            "w+",
        ) as outData:
            json.dump(data, outData)
        startJDService()
# ====================================================================================================
# ====================================================================================================


# PATH_RClone_Config renamed to rcloneConfigurationPath
rcloneConfigurationPath = "/root/.config/rclone"


def displayOutput(operationName="", color="#ce2121"):
    if color == "success":
        hColor = "#28a745"
        displayTxt = f"👍 Operation {operationName} has been successfully performed."
    elif color == "danger":
        hColor = "#dc3545"
        displayTxt = f"❌ Unable to perform operation {operationName}!"
    elif color == "info":
        hColor = "#17a2b8"
        displayTxt = f"👋 Operation {operationName} have some information."
    elif color == "warning":
        hColor = "#ffc107"
        displayTxt = f"⚠ Operation {operationName} have a warning!"
    else:
        hColor = "#ffc107"
        displayTxt = f"{operationName} works."
    display(
        HTML(
            f"""
            <center>
                <h2 style="font-family:monospace;color:{hColor};">
                    {displayTxt}
                </h2>
                <br>
            </center>
            """
        )
    )


def addUtils():
    if checkAvailable("/content/sample_data"):
        runSh("rm -rf /content/sample_data")
    if not checkAvailable("/usr/local/sessionSettings"):
        runSh("mkdir -p -m 777 /usr/local/sessionSettings")
    if not checkAvailable("/content/upload.txt"):
        runSh("touch /content/upload.txt")
    if not checkAvailable("/root/.ipython/mixlab.py"):
        runSh(
            "wget -qq https://shirooo39.github.io/MiXLab/resources/mixlab.py \
                -O /root/.ipython/mixlab.py"
        )
    if not checkAvailable("checkAptUpdate.txt", userPath=True):
        runSh("apt update -qq -y")
        runSh("apt-get install -y iputils-ping")
        data = {"apt": "updated", "ping": "installed"}
        accessSettingFile("checkAptUpdate.txt", data)


def configTimezone(auto=True):
    if checkAvailable("timezone.txt", userPath=True):
        return
    if not auto:
        runSh("sudo dpkg-reconfigure tzdata")
    else:
        runSh("sudo ln -fs /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime")
        runSh("sudo dpkg-reconfigure -f noninteractive tzdata")
    data = {"timezone": "Asia/Ho_Chi_Minh"}
    accessSettingFile("timezone.txt", data)

# def installRclone():
#    if not checkAvailable("/usr/bin/rclone"):
#        runSh(
#            "curl -s https://rclone.org/install.sh | sudo bash",
#            shell=True,  # nosec
#        )


def uploadRcloneConfig(localUpload=False):
    if not localUpload and checkAvailable("rclone.conf", userPath=True):
        return
    elif not localUpload:
        runSh(
            "wget -qq https://raw.githubusercontent.com/tungmin97/VueTorrent-To-Google-Drive/master/resources/configurations/rclone/rclone.conf \
                -O /usr/local/sessionSettings/rclone.conf"
        )
    else:
        try:
            print("Upload rclone.conf from your computer.")
            uploadedFileName = files.upload().keys()
            if len(uploadedFileName) > 1:
                for fn in uploadedFileName:
                    runSh(f'rm -f "/content/{fn}"')
                return print("Please only upload a single configuration file.")
            elif len(uploadedFileName) == 0:
                return print("File upload have been cancelled.")
            else:
                for fn in uploadedFileName:
                    if checkAvailable(f"/content/{fn}"):
                        runSh(
                            f'mv -f "/content/{fn}" /usr/local/sessionSettings/rclone.conf'
                        )
                        runSh("chmod 666 /usr/local/sessionSettings/rclone.conf")
                        runSh('rm -f "/content/{fn}"')
                        print("The file have been successfully uploaded.")

        except:
            return print("Upload failed!")


def uploadQBittorrentConfig():
    if checkAvailable("updatedQBSettings.txt", userPath=True):
        return
    runSh(
        "mkdir -p -m 666 /content/qBittorrent /root/.qBittorrent_temp /root/.config/qBittorrent"
    )
    runSh(
        "wget -qq https://raw.githubusercontent.com/tungmin97/VueTorrent-To-Google-Drive/master/resources/configurations/qbittorrent/qBittorrent.conf \
            -O /root/.config/qBittorrent/qBittorrent.conf"
    )
    data = {"uploaded": "True"}
    accessSettingFile("updatedQBSettings.txt", data)


def prepareSession():
    if checkAvailable("ready.txt", userPath=True):
        return
    else:
        addUtils()
        configTimezone()
        uploadRcloneConfig()
        uploadQBittorrentConfig()
        # installRclone()
        accessSettingFile("ready.txt", {"prepared": "True"})
