from pyHS100 import SmartBulb, SmartPlug
from datetime import datetime, timedelta
import pytz, time
from astral import Astral

plugIP = '192.168.1.103'
bulbIP = '192.168.1.104'

cityName = 'Boston'
'''
for list of possible cities: http://pythonhosted.org/astral/index.html

'''
# returns true if the current time is between dusk and dawn using the Astral library

def sunset():    
    a = Astral()
    location = a[cityName]
    location.solar_depression = 3 #defines angle of sun to calculate time
    sun = location.sun(date=datetime.today(), local=True) #returns a dictionary containing sunset,sunrise,dusk,dawn : times

    timeSunset = sun['dusk']
    timeNow = datetime.now(pytz.timezone(location.timezone)) #gets current time with same time zone to be time zone aware
    timeSunrise = sun['dawn'] + timedelta(days=1) #gets sunrise time of next day

    # print("sunset: " + str(timeSunset))
    # print('sunrise: ' + str(timeSunrise))

    return (timeNow < timeSunrise and timeNow > timeSunset)

if (__name__ == "__main__"):
    plug = SmartPlug(plugIP)
    bulb = SmartBulb(bulbIP)
  #  v = sunset()
    if(bulb.is_on and sunset()): #if the bulb is currently on and it's night time then turn off the bulb and turn on lamp#transition to 50% then turn on lamp then transition to 0
        bulb.set_light_state({'on_off': 0, 'transition_period': 3000})
        plug.turn_on()
        
'''
    #for easier testing comment out for implementation
    elif(plug.is_on): #if daytime and the lamp is still on, turn it off
        bulb.set_light_state({'on_off': 1, 'transition_period': 3000})
        plug.turn_off()
'''
