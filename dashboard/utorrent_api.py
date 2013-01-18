import httplib
import urllib
import base64
import re
import subprocess
import json

utorrent_loc = "C:\Users\Administrator\Desktop\uTorrent.exe"

DEBUG = False

class UTorrentDL:
    def get(self, link, dest):
        print utorrent_loc + ' /DIRECTORY "' + dest + '" "' + link + '"'
        subprocess.call([utorrent_loc, '/DIRECTORY', dest, link])

class TorrentInfo:
    def __init__(self, data):
        self.hash = data[0]
        self.status = data[1]
        self.name = data[2]
        self.size = data[3]
        self.percent = data[4]
        self.percent_str = float(data[4]) / 10
        self.downloaded = data[5]
        self.uploaded = data[6]
        self.up_speed = data[8]
        self.down_speed = data[9]
        self.down_speed_str = str(data[9] * 0.0009765625)[:6] + ' KBs/sec'
        self.eta = data[10]
        self.label = data[11]
        self.peers = data[12]
        self.seeds = data[14]
        self.remaining = data[18]
        self.dir = data[26]

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

    def setprop(self, prop, value, hashid):
        response = self.makerequest("/gui/?action=setprops&hash=" + hashid + "&s=" + prop + "&v=" + value)
        return response.read()

    def gettorrs(self):
        data = json.loads(self.list())['torrents']
        r = []
        for bit in data:
            torr = TorrentInfo(bit)
            if torr.label != 'Colbert' and torr.label != 'DailyShow' and torr.label != 'Conan':
                r.append(torr)
        return r

    def getbyhash(self, hashid):
        data = json.loads(self.list())['torrents']
        if data != []:
            for bit in data:
                torr = TorrentInfo(bit)
                if torr.hash == hashid:
                    return torr
            return None
        else:
            return None

    def getfilename(self, hashid):
        response = self.makerequest("/gui/?action=getfiles&hash=" + hashid)
        data = json.loads(response.read())['files'][1]
        size = 0
        filename = ''

        print data

        for bit in data:
            if bit[1] > size:
                size = bit[1]
                filename = bit[0]
        return filename

    def getnewest(self):
        data = json.loads(self.list())['torrents']
        if data != []:
            for bit in data:
                torr = TorrentInfo(bit)
                if torr.label == '':
                    return torr
            return None
        else:
            return None

    def stop(self, hashid):
        response = self.makerequest("/gui/?action=stop&hash=" + hashid)
        return response.read()

    def remove(self, hashid):
        response = self.makerequest("/gui/?action=remove&hash=" + hashid)
        return response.read()


if (DEBUG):
    request = UTorrentConn("127.0.0.1:2219", "Boyshouse", "nickc")
    print request.list()
    print request.getfiles("ED926B#47A6DD813796A8C57C13989A11B0FCC951")
    print request.getprops("ED926B47A6DD813796A8C57C13989A11B0FCC951")
