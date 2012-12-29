import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,json

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        #liz.setProperty("SWFPlayer", swfUrl)
        #liz.setProperty("PlayPath", playpath)
        #ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(url, liz)
        return ok

#url = 'rtmp://aveo.ischool.utexas.edu/vod'
#url = 'rtmp://sdwfchwqitj2v.cloudfront.net:1935/cfx/st/'

# when we left the earth
#url = "http://sbsauvod-f.akamaihd.net/SBS_Production/managed/2012/12/2012-12-19_449580_,128,512,1000,1500,K.mp4.csmil/bitrate=2?v=2.9.4&fp=MAC%2011,5,31,5&r=UHUPB&g=BNZSXGYJFVHW"

url = "http://sbsauvod-f.akamaihd.net/SBS_Production/managed/2012/12/2012-12-03_436348_,128,512,1000,1500,K.mp4.csmil/bitrate=3?v=2.9.4&fp=MAC%2011,5,31,5&r=SRSHV&g=KKASGWQJGRHG"
playpath = ''
name = 'Gloria Swanson'
iconimage = 'http://solstice.ischool.utexas.edu/tmwi/images/1/1a/Gloria_Swanson_tn.jpg'
#swfUrl = "http://solstice.ischool.utexas.edu/tmwi/extensions/player/flvplayer.swf"
#swfUrl = "http://www-tc.pbs.org/video/media/swf/PBSPlayer.swf"
swfUrl = "http://resources.sbs.com.au/vod/theplatform/core/current/swf/flvplayer.swf"
#addLink(name,url,iconimage,playpath,swfUrl)
#addLink(name,url,iconimage)

#inStream
#akamaiHD
#advancedText

#/vod/sbs/swf/resumePlaybackSBS.swf

#http://sbsauvod-f.akamaihd.net
#/SBS_Production/managed/2012/12/2012-12-19_449580_,128,512,1000,1500,K.mp4.csmil/bitrate=3?v=2.9.4&fp=MAC%2011,5,31,5&r=UHUPB&g=BNZSXGYJFVHW&seek=34.613 HTTP/1.1



thisPlugin = int(sys.argv[1])

def getFeatured():
    url = 'http://feed.theplatform.com/f/dYtmxB/featured-programs-prod?form=json&defaultThumbnailAssetType=Thumbnail'
    req = urllib2.Request(url)
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return json.loads(response)

def createListing():
    listing = getFeatured()['entries']
    return listing

def log(msg):
    f = open('/tmp/sbs.log', 'a')
    f.write(msg + '\n')
    f.close()

def logover(msg):
    f = open('/tmp/sbs.json', 'w')
    f.write(msg + '\n')
    f.close()

def sendToXbmc(listing):
    global thisPlugin

    for item in listing:

        if item.has_key('media$thumbnails'):
            thumb = item['media$thumbnails'][0]['plfile$downloadUrl']
        else:
            thumb = ''
            #log(item['id'] + ' ' + thumb)
            logover(json.dumps(item))

        listItem = xbmcgui.ListItem(item['title'], item['description'], iconImage = 'icon.png', thumbnailImage = thumb)
        listItem.setInfo( type='Video', infoLabels={'Title': item['title']} )

        u = item['id']

        xbmcplugin.addDirectoryItem(thisPlugin, u,listItem)

    xbmcplugin.endOfDirectory(thisPlugin)

sendToXbmc(createListing())

