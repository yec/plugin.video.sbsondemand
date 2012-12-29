import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,json,sys,os
import urlparse

_curDir = os.path.dirname(__file__)
sys.path.append(_curDir + '/resources/lib/sbsOnDemand')

import SbsOnDemand.config

_thisPlugin = int(sys.argv[1])
_scheme = 'plugin://plugin.video.sbsondemand/'

def routes(url):
    global _scheme
    path = url.replace(_scheme, '')

    if path == '':
        view_feeds(url)

def view_feeds(url):
    global _thisPlugin

    for item in SbsOnDemand.config.DEFAULT_FEEDS:
        li = xbmcgui.ListItem(item['name'])
        isfolder = True
        xbmcplugin.addDirectoryItem(_thisPlugin, url + 'category/' + item['feedId'], li, isfolder)

    xbmcplugin.endOfDirectory(_thisPlugin)

routes(sys.argv[0])
