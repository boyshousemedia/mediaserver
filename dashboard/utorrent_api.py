import httplib
import urllib
import base64
import re
import subprocess

utorrent_loc = "/Applications/uTorrent.app/Contents/MacOS/uTorrent"

DEBUG = False

class UTorrentDL:
    def __init__(self):
        self.utorrent = utorrent_loc

    def get(self, link, dest):
        subprocess.call([self.utorrent + ' /DIRECTORY "' + dest + '" "' + link + '"'])

class UTorrentConn:
    def __init__(self, host, user, passw):
        self.host = host
        self.token = ""
        self.cookie = ""
        self.user = user
        self.passw = passw
        self.connect()

    def connect(self):
        h = httplib.HTTPConnection(self.host)
        headers = {"Authorization": "Basic " + base64.b64encode(self.user + ":" + self.passw),  "Host": self.host}
        h.request("GET", "/gui/token.html", "", headers);

        r1 = h.getresponse()
        if r1.status != 200:
            raise PasswordError("Password wrong")
        self.parse(r1)
        print r1.read()

    def parse(self, response):
        temp = response.getheader("Set-Cookie")
        self.cookie,sep,_ = temp.partition("; path=/")
        if sep == "":
            self.cookie = temp
        
        html = response.read()
        p = re.compile(">([^<]*)</div>")
        m = p.search(html)
        self.token = m.group(1)

    def makerequest(self, request):
        h = httplib.HTTPConnection(self.host)
        headers = {"Authorization": "Basic " + base64.b64encode(self.user + ":" + self.passw),  "Host": self.host, "Cookie" : self.cookie}
        h.request("GET", request + "&token=" + self.token, "", headers)
        return h.getresponse()

    def list(self):
        response = self.makerequest("/gui/?list=1");
        return response.read()

    def getfiles(self, hashid):
        response = self.makerequest("/gui/?action=getfiles&hash=" + hashid)
        return response.read()
       
    def getprops(self, hashid):
        response = self.makerequest("/gui/?action=getprops&hash=" + hashid)
        return response.read()

if (DEBUG):
    request = UTorrentConn("127.0.0.1:2219", "Boyshouse", "nickc")
    print request.list()
    print request.getfiles("ED926B#47A6DD813796A8C57C13989A11B0FCC951")
    print request.getprops("ED926B47A6DD813796A8C57C13989A11B0FCC951")
