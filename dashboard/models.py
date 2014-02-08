from django.db import models
from tvdb_api import TVDBConn
from utorrent_api import UTorrentDL, UTorrentConn, TorrentInfo
from pb import PBSearch, PBResult
import re
import math
import os
import fnmatch
import operator
import shutil

base_folder = "E:/TV"

class ServerTime(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.IntegerField()

class Episode(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    overview = models.TextField()
    air_date = models.DateField(blank=True, null=True)
    show_id = models.IntegerField()
    show_name = models.CharField(max_length=100)
    path = models.CharField(max_length=100, blank=True)
    image = models.CharField(max_length=100)
    downloading = models.BooleanField()
    dl_hash = models.CharField(max_length=100)

    def getDir(self):
        show = self.show_name
        show = re.sub('\.','',show)
        return base_folder + '/' + show + '/Season ' + str(self.season)

    def getFileName(self, name=None):
        if name is None:
            name = self.name
        name = re.sub(':', '', name)
        name = re.sub('\?', '', name)
        return 'S' + ("%02d" % int(self.season)) + 'E' + ("%02d" % int(self.number)) + ' - ' + name + ' (' + self.air_date.strftime("%m-%d-%Y") +')'

    def download(self, link, name):
        if (not os.path.exists(self.getDir())):
            os.mkdir(self.getDir())

        if (os.path.isfile(self.path)):
            os.remove(self.path)

        dl = UTorrentDL()
        dl.get(link, self.getDir())

        request = UTorrentConn("127.0.0.1:2219", "Boyshouse", "nickc")
        torrents = request.gettorrs()
        for torrent in torrents:
            #print torrent.name
            #print name
            if torrent.name == name:
                # Check if it is a .rar
                error = True
                while(error):
                    try:
                        filename = request.getfilename(torrent.hash)
                    except:
                        continue
                    error = False
                #print filename
                #print 'hi'
                ext = os.path.splitext(filename)[1]
                #print ext
                if ext == '.rar' or fnmatch.fnmatch(ext, '.r[0-9][0-9]'):
                    request.removedata(torrent.hash)
                    request.remove(torrent.hash)
                    return False

                error = True
                while(error):
                    try:
                        request.setprop("label", str(self.id), torrent.hash)
                    except:
                        continue
                    error = False

                self.dl_hash = torrent.hash
                self.downloading = True
                self.save()
                return True
        print "Did not find torrent"
                    
    def cleanup(self):
        request = UTorrentConn("127.0.0.1:2219", "Boyshouse", "nickc")
        request.stop(self.dl_hash)
        self.downloading = False
        self.path = 'pending'
        self.save()

    def rename(self):
        request = UTorrentConn("127.0.0.1:2219", "Boyshouse", "nickc")
        torr = request.getbyhash(self.dl_hash)
        if torr == None:
            print 'no hash ' + self.name
            return

        filename = request.getfilename(self.dl_hash)
        dir = os.path.abspath(torr.dir)
        (root, ext) = os.path.splitext(filename)

        try:
            os.rename(dir + '\\' + filename, self.getDir() + '/' + self.getFileName() + ext)
        except Exception as e:
            print dir + '\\' + filename
            print self.getDir() + '/' + self.getFileName() + ext
            print e
            return
        request.remove(self.dl_hash)
        self.path = self.getDir() + '/' + self.getFileName() + ext

        # If in dir (e.g. dir exists in "Season" folder), remove dir
        for file in os.listdir(self.getDir()):
            if os.path.isdir(self.getDir() + '/' + file):
                try:
                    shutil.rmtree(self.getDir() + '/' + file)
                except:
                    pass

        
        self.dl_hash = ''
        self.save()

    def checkForExistingFile(self):
        if (not os.path.exists(self.getDir())):
            return

        name = re.sub('\([0-9]*\)', '', self.name)
        print name
        for file in os.listdir(self.getDir()):
            print file
            if (fnmatch.fnmatch(file.lower(), '*' + name.strip().lower() + '*') or
               fnmatch.fnmatch(file, '*S' + ("%02d" % int(self.season)) + 'E' + ("%02d" % int(self.number)) + '*')):
                self.path = self.getDir() + '/' + file
                self.save()
    
    def getSearchUrl(self):
        pb = PBSearch()
        url = pb.getUrl(self.getsearch())
        return url

    def gettorrents(self):
        pb = PBSearch()
        torrents = pb.searchFor(self.getsearch())
        return torrents

    def __unicode__(self):
        return self.name

    def getsearch(self):
        show = Show.objects.get(id=self.show_id)
        search = show.search
        
        search = re.sub('{s}', str(self.season), search)
        search = re.sub('{e}', str(self.number), search)
        search = re.sub('{0s}', "%02d" % self.season, search)
        search = re.sub('{0e}', "%02d" % self.number, search)
        search = re.sub('{n}', self.name, search)

        plus_one = self.number + 1
        search = re.sub('{0e\+1}', "%02d" % plus_one, search)

        avNum = "%02d" % (math.ceil(self.number/2.0))
        if(self.number % 2 != 0):
            num = str(self.season) + avNum + 'a'
        else:
            num = str(self.season) + avNum + 'b'
        search = re.sub('{a}', num, search)

        return search

    def renameIfNeeded(self, name):
        if bool(self.path) and (self.name != name):
            try:
                _,ext = os.path.splitext(self.path)
                path = self.getDir() + '/' + self.getFileName(name) + ext
                os.rename(self.path, path)
                self.path = path
                print 'Renamed: ' + path
            except Exception, e:
                print "Couldn't rename: %s" % e
                return
        self.name = name

    def update(self, dic=None):
        tvdb = TVDBConn()
        if dic is None:
            dic = tvdb.getepisodebyid(self.id)
        self.season = dic['SeasonNumber']
        self.number = dic['EpisodeNumber']
        name = Episode.getField(dic, 'EpisodeName','No Name on TVDB')
        self.renameIfNeeded(name)
        self.air_date = dic.get('FirstAired')
        self.overview = Episode.getField(dic,'Overview','No overview available.')
        self.image = "http://www.thetvdb.com/banners/" + Episode.getField(dic, 'filename',)
        self.save()

    #Get method for xmltodict obj that handles None
    #as an empty string
    @classmethod
    def getField(cls, episode, field, alternate = ''):
        result = episode[field]
        if (result is None):
            return alternate
        else:
            # emcode to protect against wiki assholes
            return result

    @classmethod
    def create(cls, episode, show_id, show_name):
        e = cls(id = episode['id'],
               	season = episode['SeasonNumber'],
               	number = episode['EpisodeNumber'],
                name = cls.getField(episode, 'EpisodeName','No Name on TVDB'),
                overview = cls.getField(episode,'Overview','No overview available.'),
                show_id = show_id,
                show_name = show_name,
                path = '',
                image = "http://www.thetvdb.com/banners/" + cls.getField(episode, 'filename',),
                downloading = False,
                dl_hash = '',

                # use episode.get() to allow None for DateField
                air_date = episode.get('FirstAired'))
        e.checkForExistingFile()
        e.save();

class Show(models.Model):
    id = models.IntegerField(primary_key=True);
    name = models.CharField(max_length=100)
    air_day = models.CharField(max_length=10)
    air_time = models.CharField(max_length=10)
    banner = models.CharField(max_length=100)
    poster = models.CharField(max_length=100)
    download = models.BooleanField()
    search = models.CharField(max_length=100)

    #TODO - Note: Name not changed to avoid folder name mismatch
    def update(self):
        tvdb = TVDBConn()
        series = tvdb.getseriesbyid(self.id)
        self.air_day = Show.getField(series, 'Airs_DayOfWeek')
        self.air_time = Show.getField(series, 'Airs_Time')
        self.banner = "http://www.thetvdb.com/banners/" + Show.getField(series, 'banner')
        self.poster = "http://www.thetvdb.com/banners/" + Show.getField(series, 'poster')
        self.save()

    def remove(self):
        eps = Episode.objects.filter(show_id=self.id)
        for ep in eps:
            ep.delete()
        self.delete()

    #Get method for xmltodict obj that handles None
    #as an empty string
    @classmethod
    def getField(cls, series, field, alternate = ''):
        result = series[field]
        if (result is None):
            return alternate
        else:
            return result

    @classmethod
    def create(cls, show_id):
        tvdb = TVDBConn()
    	dic = tvdb.initseriesbyid(show_id)

    	#Add Series
    	series = dic['Series']
    	temp_name = re.sub('\s*\([0-9]*\)', '', series['SeriesName'])
    	temp_name = re.sub('&', 'and', temp_name)
    	temp_name = re.sub(':', '', temp_name)
    	temp_name = re.sub('\.', '', temp_name)
    	s = cls(id = series['id'],
                name = temp_name,
                air_day = cls.getField(series, 'Airs_DayOfWeek'),
                air_time = cls.getField(series, 'Airs_Time'),
                banner = "http://www.thetvdb.com/banners/" + cls.getField(series, 'banner'),
                poster = "http://www.thetvdb.com/banners/" + cls.getField(series, 'poster'),
                download = False,
                search = temp_name + " S{0s}E{0e}")
    	s.save()
        
        if (not os.path.exists(base_folder + '/' + unicode(temp_name))):
            os.mkdir(base_folder + '/' + unicode(temp_name))
        
    	episodes = dic['Episode']
    	for episode in episodes:
            Episode.create(episode, show_id, s.name)

    def __unicode__(self):
        return self.name

    def toggleDownload(self):
        if (self.download):
            self.download = False
        else:
            self.download = True
