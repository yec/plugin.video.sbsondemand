import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,json,sys,os
import urlparse

_curDir = os.path.dirname(__file__)
sys.path.append(_curDir + '/resources/lib/sbsOnDemand/')

import SbsOnDemand.config
import SbsOnDemand.Feed

_thisPlugin = int(sys.argv[1])
_scheme = 'plugin://plugin.video.sbsondemand/'

def routes(url):
    global _scheme
    path = url.replace(_scheme, '')

    if path == '':
        view_feeds(url)
    elif re.search('category/.*', path):
        view_shows(path)
    else:
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

    m = re.search('category/(.+)', url)
    feedname = m.group(1)
    feed = SbsOnDemand.Feed.getFeedFromId(feedname)
    for video in feed.getVideos(itemsPerPage=feed.totalResults):
        li = xbmcgui.ListItem(video.title)
        xbmcplugin.addDirectoryItem(_thisPlugin, video.url, li)

    xbmcplugin.endOfDirectory(_thisPlugin)

def play_video(url):
    global _thisPlugin
    ok = True
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(url)
    return ok


routes(sys.argv[0])
