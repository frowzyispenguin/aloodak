import requests
from bs4 import BeautifulSoup
from rtl import rtl
from khayyam import *
print("\n",rtl(JalaliDate.today().strftime('%A %d %B %Y')),"\n")
weather_url = "https://airnow.tehran.ir"
weather_req = requests.get(weather_url)
if (weather_req.ok != True):
    quit()
weather_src = weather_req.text
soup = BeautifulSoup(weather_src,"lxml")
last24hour_rate = str(soup('span', {'id' : 'ContentPlaceHolder1_lblAqi24h'})[0]).split('>')[1].split("<")[0]
last24hour_status = str(soup('span', {'id' : 'ContentPlaceHolder1_lblAqi24hDesc'})[0]).split('>')[1].split("<")[0]
rightnow_rate = str(soup('span', {'id' : 'ContentPlaceHolder1_lblAqi3h'})[0]).split('>')[1].split("<")[0]
rightnow_status = str(soup('span', {'id' : 'ContentPlaceHolder1_lblAqi3hDesc'})[0]).split('>')[1].split("<")[0]
temprature = str(soup('span', {'id' : 'ContentPlaceHolder1_lblCurrentTemp'})[0]).split(">")[3].split("<")[0][1]
windspeed =  str(soup('span', {'id' : 'ContentPlaceHolder1_lblCurrentWind'})[0]).split('>')[1].split("<")[0]
print(rtl("وضعیت آب و هوا "))
print(rtl("\nشاخص آلودگی هوا \n"),rtl("\nهمین الآن \n"),rightnow_rate,rtl(rightnow_status),rtl("\n\nروز پیش \n"),last24hour_rate,rtl(last24hour_status),rtl("\n\nدما \n"),temprature,"℃\n",rtl("\nسرعت یاد \n"),windspeed,"m/s")
