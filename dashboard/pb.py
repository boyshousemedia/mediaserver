import re
import urllib
from datetime import date, time, datetime, timedelta

class PBResult():

    def __init__(self):
        self.name = ""
        self.magnet = ""
        self.link = ""
        self.size = ""
        self.date = ""
        self.seeds = ""
        self.leeches = ""
        self.vip = False
        self.trusted = False

    def isLegit(self):
        return self.vip | self.trusted
        
    def __str__(self):
        marker = ""
        if (self.vip):
            marker = "V - "
        elif(self.trusted):
            marker = "T - "
        return marker + self.name + " " + self.size + " " + self.date + " " + self.seeds + " " + self.leeches

    def checkName(self, line):
        match = re.search('<a href="/torrent[^>]*>([^<]*)', line)
        if (match != None):
            self.name = match.group(1)

    def checkLink(self, line):
        match = re.search('<a href="(/torrent[^"]*)', line)
        if (match != None):
            self.link = "http://thepiratebay.se" + match.group(1)

    def checkMagnet(self, line):
        match = re.search('<a href="(magnet[^"]*)', line)
        if (match != None):
            self.magnet = match.group(1)

    def checkSize(self, line):
        match = re.search('Size ([^,]*)', line)
        if (match != None):
            self.size = match.group(1).replace("&nbsp;", " ")

    def checkDate(self, line):
        match = re.search('Uploaded ([^,]*)', line)
        if (match != None):
            date_str = match.group(1).replace("&nbsp;", " ")

            # "mins" -> uploaded very recently
            if(date_str.find("ago") != -1):
                self.date = datetime.now()
            elif(date_str.find("Today") != -1):
                my_datetime = datetime.strptime(date_str, "Today %H:%M")
                my_time = datetime.time(my_datetime)
                my_date = datetime.now()
                self.date = datetime.combine(my_date, my_time)
            elif(date_str.find("Y-day") != -1):
                my_datetime = datetime.strptime(date_str, "Y-day %H:%M")
                my_time = datetime.time(my_datetime)
                my_date = datetime.now() - timedelta(days=1)
                self.date = datetime.combine(my_date, my_time)
            # If it has time -> year is this year
            elif (date_str.find(":") != -1):
                self.date = datetime.strptime(date_str + " " + str(date.today().year), "%m-%d %H:%M %Y")
            else:
                self.date = datetime.strptime(date_str, "%m-%d %Y")

    def checkPeers(self, line):
        match = re.search('<td align="right">([^<]*)', line)
        if (match != None):
            num = match.group(1)

            # Seeds come firs in HTMLt
            if(self.seeds == ""):
                self.seeds = num
            else:
                self.leeches = num

    def checkVIP(self, line):
        match = re.search('<img [^>]*title="VIP"', line)
        if (match != None):
            self.vip = True

    def checkTrusted(self, line):
        match = re.search('<img [^>]*title="Trusted"', line)
        if (match != None):
            self.trusted = True

class PBSearch():

    def makerequest(self, request):
        return urllib.urlopen(request)


    def getUrl(self, search):
        search = re.sub("\s", "%20", search)
        return "http://thepiratebay.se/search/" + search + "/0/7/0"

    def searchFor(self, search):
        url = self.getUrl(search)

        results = []
        response = self.makerequest(url)
        items = re.split('<div class="detName">', response.read())
        for item in items[1:]:
            result = PBResult()
            lines = item.split('\n')
            for line in lines:
                result.checkName(line)
                result.checkMagnet(line)
                result.checkLink(line)
                result.checkSize(line)
                result.checkDate(line)
                result.checkPeers(line)
                result.checkVIP(line)
                result.checkTrusted(line)
            results.append(result)
        return results
        
