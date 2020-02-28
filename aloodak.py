import jdatetime
import requests
import rtl
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime
import os
import pytz
jdatetime.set_locale("fa_IR")
# defining textcolor / light/dark colors has calculated by hps

# for replacing english digits with persian ones
digits = {'1':'۱', '2':'۲', '3':'۳', '4':'۴', '5':'۵', '6':'۶', '7':'۷', '8':'۸', '9':'۹', '0':'۰'}
statusbar = {
    "Hazardous": "خطر اضطراری",
    "Very Unhealthy": "خیلی ناسالم",
    "Unhealthy": "ناسالم",
    "Unhealthy for Sensitive Groups": "ناسالم برای گروه های حساس",
    "Moderate": "سالم",
    "Good": "پاک"
}
color = {
    "Hazardous": (104,62,81),
    "Very Unhealthy": (99,70,117),
    "Unhealthy": (175,44,59),
    "Unhealthy for Sensitive Groups": (178,88,38),
    "Moderate": (165,127,35),
    "Good": (113,139,58)
}
def now():
    tz = pytz.timezone('Asia/Tehran') 
    tehran_now = datetime.now(tz)    
    return tehran_now.strftime("%H:%M")

def today():
    today = jdatetime.datetime.now(pytz.timezone("Asia/Tehran")).strftime("%A %y/%m/%d").split()
    date = today[-1]
    today.pop(-1)
    day = " ".join(i.strip() for i in today)
    return [day, en2per(date)]

def en2per(string):
    # it parses string in list for acessing to string charachters
    chars = list(map(lambda x: digits[x] if x.isdecimal() else x,list(string)))
    # it returns an string of above list elements wich joined
    return ''.join([str(x) for x in chars]) 
class aloodak:
    def __init__(self):
        pass
    def parser(country,province,city):
        # request webserver and parsing data
        data = {}
        url = f"https://www.airvisual.com/{country}/{province}/{city}"
        src = requests.get(url).text
        soup = bs(src, "html.parser")
        data['status'] = soup.find_all(attrs={"class":"status-text"})[0].text #air status
        data['aqi'] = en2per(soup.find_all(attrs={"class":"aqi"})[0].text.split("US")[0]) #aqi
        data['pm'] = en2per(soup.find_all(attrs={"class":"pm-number"})[0].text.split("|")[1].strip()) #pm2.5
        data['temperature'] = en2per(soup.find_all(attrs={"class":"forecast-info-icon-temp"})[0].text) #temperature
        data['humidity'] = en2per(soup.find_all(attrs={"class":"item-label-val"})[0].text) #humidity
        return data

class info_maker():
    def __init__(self,data):
        self.imgdir = f"badges/{data['status']}.png"
        self.font = ImageFont.truetype("Sahel-Black.ttf", 140) # rate font style
        self.temperature = data['temperature']
        self.humidity = data['humidity']
        self.pm = data['pm']
        self.aqi = str(data['aqi']) # pollution rate
        self.status = statusbar[data['status']] # pollution status
        self.color = color[data['status']]
    def draw(self): 
        self.image = Image.open(self.imgdir) # opening image
        self.draw_object = ImageDraw.Draw(self.image) # loafing draw module 
        # wrting data over image
        if len(self.aqi) == 3:
            self.draw_object.text((100,100),self.aqi,self.color,font=self.font)
        elif len(self.aqi) == 2:
            self.draw_object.text((130,100),self.aqi,self.color,font=self.font)
        elif len(self.aqi) == 1:
            self.draw_object.text((150,100),self.aqi,self.color,font=self.font) 
        # saving image
        self.image.save("report.png")
        return None
    def checksum(self):
        status = os.getenv('STATUS')
        status = os.popen("sha1sum report.png").read().split()[0]
        return status
    def cpation(self):
        items = {"🔹شاخص آلودگی هوا : " : self.aqi,
                 "🔹وضعیت هوا : " : self.status,
                 "💧 رطوبت هوا : ":self.humidity,
                 "🌡 دمای هوا : ":self.temperature,
                 "💨 غلظت ذرات معلق در هوا : ":self.pm,
                 "🗓تاریخ : " : ' - '.join([x for x in today()]),
                 "🕓ساعت : " : en2per(now())
                }
        with open("report.txt","w") as foo :
            caption = [(item+items[item]) for item in items]
            caption = '\n'.join(x for x in caption)
            foo.write(caption)

