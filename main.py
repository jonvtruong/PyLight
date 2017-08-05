'''
Sunset API: https://sunrise-sunset.org
'''

from pyHS100 import SmartBulb, SmartPlug
from datetime import datetime, timedelta

import requests

googleParams = {'address': '02134', 'key': 'AIzaSyBqnPBbHIGdTwE-QVRtbwXUVPnzisQ4Prc'}

plugIP = '192.168.1.103'
bulbIP = '192.168.1.104'

def sunset():
    google = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=googleParams)
   # print("Google status: " + str(google.status_code))
    googleDict = google.json()
    
    #34x per minute
    # for k,v in googleDict['results'].items():
    #      print(str(k) + ": " + str(v))

    googleDict['results'][0]['geometry']['location']['formatted'] = 0


    sun = requests.get('https://api.sunrise-sunset.org/json', params=googleDict['results'][0]['geometry']['location'])
  #  print("sun status: " + str(sun.status_code))
    sunDict = sun.json()
   # sunsetTime = datetime.strptime(sunDict['results']['sunset'], '%I:%M:%S %p')
    sunsetTime = sunDict['results']['sunset']
    nowUTC = datetime.utcnow()
    print("sunset: " + str(sunsetTime))
    print("time now: " + str(nowUTC))

    d = timedelta(minutes = 30)

    #if(nowUTC < sunsetTime):
    #    print("its sunset")

    return False

if (__name__ == "__main__"):
    plug = SmartPlug(plugIP)
    bulb = SmartBulb(bulbIP)
    sunset()

    # if(bulb.is_on):
    #     plug.turn_on()
    #     bulb.turn_off()

