from pprint import pprint
import requests
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=London&APPID={APIKEY}')

import pyowm
owm = pyowm.OWM()
observation = owm.weather_at_place('London,uk') 
w = observation.get_weather()
w.get_wind()
{u'speed': 3.1, u'deg': 220}
w.get_humidity()