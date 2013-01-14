import urllib
import base64
import re

import xmltodict

DEBUG = False

class TVDBConn:
    def __init__(self):
        self.host = "http://www.thetvdb.com/api"
        self.key = "8981BF6D112D3E45"
        self.time = ""

    def makerequest(self, request):
        return urllib.urlopen(self.host + request);

    # Returns the time
    def gettime(self):
        response = self.makerequest("/Updates.php?type=none")
        dic = xmltodict.parse(response.read())
        return dic['Items']['Time']

    # Returns a list of series that have changed since the given time
    def getseriesupdates(self, time):
        response = self.makerequest("/Updates.php?type=series&time=" + str(time))
        dic = xmltodict.parse(response.read())
        return dic['Items']['Series']

    # Returns a list of episodes that have changed since the given time
    def getepisodeupdates(self, time):
        response = self.makerequest("/Updates.php?type=episode&time=" + str(time))
        dic = xmltodict.parse(response.read())
        return dic['Items']['Episode']

    # Lookup the series id for a given series name
    # Returns abridged series info
    def lookup(self, name):
        response = self.makerequest("/GetSeries.php?" + urllib.urlencode({'seriesname': name}))
        dic = xmltodict.parse(response.read())

        # Handle empty result
        if dic['Data'] is None:
            return {}
        # Handle mutiple results
        elif isinstance(dic['Data']['Series'], list):
            return dic['Data']['Series']
        # Handle one result -> make it a list
        else:
            return [dic['Data']['Series']]
    
    # Returns whole series information
    # Format:
    #   Series
    #       Series info
    #   List of episodes
    #       Episode info
    def initseriesbyid(self, seriesid):
        response = self.makerequest("/" + self.key + "/series/" + seriesid + "/all/en.xml")
        dic = xmltodict.parse(response.read())
        return dic['Data']

    # Returns series info
    def getseriesbyid(self, seriesid):
        response = self.makerequest("/" + self.key + "/series/" + str(seriesid) + "/en.xml")
        dic = xmltodict.parse(response.read())
        return dic['Data']['Series']

    # Returns episode info
    def getepisodebyid(self, episodeid):
        response = self.makerequest("/" + self.key + "/episodes/" + str(episodeid) + "/en.xml")
        dic = xmltodict.parse(response.read())
        return dic['Data']['Episode']

    # Returns URL of image
    def getbanner(self, bannerurl):
        return "http://www.thetvdb.com/banners/" + bannerurl

if (DEBUG):
    request = TVDBConn()
    print request.gettime()
    print request.lookup("adventure+time")
    for episode in request.initseriesbyid("152831")['Episode']:
        print episode['EpisodeName']
    print request.getseriesbyid("152831")['Actors']
    print request.getepisodebyid("2289921")['Overview']
    print request.getseriesupdates(12463226)
