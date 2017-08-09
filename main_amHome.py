from pyHS100 import SmartBulb, SmartPlug
from datetime import datetime, timedelta
import pytz, time
from astral import Astral
from platform import system as system_name # Returns the system/OS name
#from os import system as system_call       # Execute a shell command
import subprocess

PLUG_IP = '192.168.1.103'
BULB_IP = '192.168.1.104'
PHONE_IP = '192.168.1.100'

cityName = 'Boston'
'''
for list of possible cities: http://pythonhosted.org/astral/index.html

'''
# returns true if the current time is between dusk and dawn using the Astral library

def lampTime():    
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

def bulbTime():    
    a = Astral()
    location = a[cityName]
    location.solar_depression = 3 #defines angle of sun to calculate time
    sun = location.sun(date=datetime.today(), local=True) #returns a dictionary containing sunset,sunrise,dusk,dawn : times

    timeSunset = sun['dusk']
    timeNow = datetime.now(pytz.timezone(location.timezone)) #gets current time with same time zone to be time zone aware
    timeDark = timeSunset - timedelta(minutes=30) 

    # print("sunset: " + str(timeSunset))
    # print('sunrise: ' + str(timeSunrise))

    return (timeNow > timeDark and timeNow < timeSunset)

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that some hosts may not respond to a ping request even if the host name is valid.
    """
    args = ['ping', '-c', '1', '-s', '0', host] # -c 1 = 1 packet, -s 2 = 2 byte packet
    os = system_name().lower()

    if(os == "windows"): #replace arguments for number of packets and packet size for windows 
        args[1]='-n'
        args[3]='-l'

    output = subprocess.Popen(args ,stdout = subprocess.PIPE).communicate()[0].decode()

    #returns true if can ping phone
    if(os == "windows"):
        return 'unreachable' not in output 
    else:
        return 'Unreachable' not in output

if (__name__ == "__main__"):
    plug = SmartPlug(PLUG_IP)
    bulb = SmartBulb(BULB_IP)
    amHome = ping(PHONE_IP)

  #  v = sunset()
    if(amHome and lampTime()): #if the bulb is currently on and it's night time then turn off the bulb and turn on lamp#transition to 50% then turn on lamp then transition to 0
        if(bulb.is_on):
            bulb.set_light_state({'on_off': 0, 'transition_period': 3000})
        plug.turn_on()

    #print('ping: ' + str(ping(PHONE_IP)))
    elif(amHome and bulbTime()):
        #bulb.set_light_state({'on_off': 1, 'transition_period': 3000})

"""
    #for easier testing comment out for implementation
    elif(plug.is_on): #if daytime and the lamp is still on, turn it off
        bulb.set_light_state({'on_off': 1, 'transition_period': 3000})
        plug.turn_off()
"""
