import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,json,sys,os
import urlparse

_curDir = os.path.dirname(__file__)
sys.path.append(_curDir + '/resources/lib/sbsOnDemand/')

import SbsOnDemand.config
import SbsOnDemand.Feed
import SbsOnDemand.Video

_thisPlugin = int(sys.argv[1])
_scheme = 'plugin://plugin.video.sbsondemand/'

class Config(object):
    """ Use bitrate less than this """
    MAX_BITRATE = 600000

class Resource(object):
    IMAGE_PLACEHOLDER = os.path.dirname(__file__) + '/resources/media/placeholder.gif'

def routes(url):
    global _scheme
    path = url.replace(_scheme, '')

    if path == '':
        view_feeds(url)
    elif re.search('category/.*', path):
        view_shows(path)
    elif re.search('play/.*', path):
        play_video(url)

def view_feeds(url):
    global _thisPlugin

    for item in SbsOnDemand.config.DEFAULT_FEEDS:
        li = xbmcgui.ListItem(item['name'])
        isfolder = True
        xbmcplugin.addDirectoryItem(_thisPlugin, url + 'category/' + item['feedId'], li, isfolder)

    xbmcplugin.endOfDirectory(_thisPlugin)

def view_shows(url):
    global _thisPlugin
    global _scheme

    m = re.search('category/(.+)', url)
    feedname = m.group(1)
    feed = SbsOnDemand.Feed.getFeedFromId(feedname)
    for video in feed.getVideos(itemsPerPage=feed.totalResults):
        li = xbmcgui.ListItem(video.title, thumbnailImage=video.thumbnail, iconImage=Resource.IMAGE_PLACEHOLDER)
        li.setInfo( 'video', { 'Title':video.title, 'Plot': video.description } )
        xbmcplugin.addDirectoryItem(_thisPlugin, _scheme + '/play/' + video.id , li, isFolder=False, totalItems=feed.totalResults)

    xbmcplugin.endOfDirectory(_thisPlugin)

def play_video(url):
    global _thisPlugin

    ok = True
    m = re.search('play/(.+)', url)
    videoId = m.group(1)
    print 'Video ID: ' + videoId
    video = SbsOnDemand.Video.getVideo(videoId)
    media = _media_with_max_bitrate(video, Config.MAX_BITRATE)
    mediaurl = media.videoUrl
    print 'Media : {0} : {1}'.format(media.bitrate, mediaurl)
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(mediaurl)
    return ok

def _media_with_max_bitrate(video, bitrate):
    media_content = filter(lambda x: x.bitrate < Config.MAX_BITRATE, video.media['content'])
    for media in sorted(media_content, key=lambda x: x.bitrate, reverse=True):
        return media
    return None

routes(sys.argv[0])
