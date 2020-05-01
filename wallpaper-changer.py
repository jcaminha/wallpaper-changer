#Wallpaper changer
#https://downlinkapp.com/sources.json

import sys
import urllib.request
import datetime
import os
import random
import time
import requests

def download(url, destination):
    exception = None

    for i in range(1, 4):  # retry max 3 times
        try:
            urllib.request.urlretrieve(url, destination)
        except Exception as e:
            exception = e
            #print("[{}/3] Retrying to download '{}'...".format(i, url))
            time.sleep(1)
    '''
    if exception:
        sys.exit("Could not download '{}'!\n".format(url))
    else:
        sys.exit("Success download '{}'!\n".format(url))
    '''
    return


def nasa_iotd():
    
    api    = 'https://www.nasa.gov/api/1/'
    public = 'https://www.nasa.gov/sites/default/files'

    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'
        nasa_iotd = []
        # first 1 pages
        for page in range(1):
            r = s.get(api + 'query/ubernodes.json', 
                    params={'page': page, 'unType[]': 'image'})
            for ubernode in r.json()['ubernodes']:
                nid = ubernode['nid']
                r = s.get(api + 'record/node/{}.json'.format(nid))
                for image in r.json()['images']:
                    uri = image['uri'].replace('public:/', public, 1)
                    nasa_iotd.append(uri)
    return random.choice(nasa_iotd)


def main():
    
    urllist = ['https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/5424x5424.jpg',
               'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/ssa/GEOCOLOR/3600x2160.jpg',
               'nasa_iotd',
               'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/taw/GEOCOLOR/3600x2160.jpg',
               'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/nsa/GEOCOLOR/3600x2160.jpg']
    
    destination = '/home/jean/.cache/goes16wallpaper/'
    filename = "wallpaper.jpg"
    url = random.choice(urllist)
    
    if (url == 'nasa_iotd'): url = nasa_iotd()

    download(url, destination+filename)

    cmd = "convert "+destination+filename+" -resize 1024x768 "+destination+filename
    os.system(cmd)

    cmd = "gsettings set org.gnome.desktop.background picture-uri file://"+destination+filename
    os.system(cmd)
    
    sys.exit(0)

if __name__ == "__main__":
    main()