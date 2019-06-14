import requests
from bs4 import BeautifulSoup
from rtl import rtl
from khayyam import *
print("\n", rtl(JalaliDate.today().strftime('%A %d %B %Y')), "\n")
weather_url = "https://airnow.tehran.ir"
weather_req = requests.get(weather_url)
if (weather_req.ok != True):
    quit()
weather_src = weather_req.text
soup = BeautifulSoup(weather_src, "html.parser")
last24hour_rate = soup.find(id="ContentPlaceHolder1_lblAqi24h").text
last24hour_img = soup.find(id="ContentPlaceHolder1_imgAqi24")['src']
last24hour_status = soup.find(id="ContentPlaceHolder1_lblAqi24hDesc").text
rightnow_rate = soup.find(id="ContentPlaceHolder1_lblAqi3h").text
rightnow_rate_img = soup.find(id="ContentPlaceHolder1_imgAqi3")['src']
rightnow_status = soup.find(id="ContentPlaceHolder1_lblAqi3hDesc").text
try:
    temprature = soup.find(
        id="ContentPlaceHolder1_lblCurrentTemp").text.split(" ")[2]
except:
    temprature = "?"
try:
    windspeed = soup.find(id="ContentPlaceHolder1_lblCurrentWind").text
except:
    windspeed = "?"


print(rtl("وضعیت آب و هوا "))
print(rtl("\nشاخص آلودگی هوا \n"), rtl("\nهمین الآن \n"), rightnow_rate, rtl(rightnow_status), rtl("\n\nروز پیش \n"),
      last24hour_rate, rtl(last24hour_status), rtl("\n\nدما \n"), temprature, "℃\n", rtl("\nسرعت یاد \n"), windspeed)
