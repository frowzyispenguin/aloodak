import requests
import rtl
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageDraw, ImageFont
# defining textcolor / light/dark colors has calculated by hps
bg={\
 'bg-aqua': (0, 0, 0),\
 'bg-blue': (255, 255, 255),\
 'bg-green': (0, 0, 0),\
 'bg-light-blue': (0, 0, 0),\
 'bg-lime': (0, 0, 0),\
 'bg-navy': (255, 255, 255),\
 'bg-olive': (0, 0, 0),\
 'bg-red': (0, 0, 0),\
 'bg-teal': (0, 0, 0),\
 'bg-yellow': (0, 0, 0),\
 'bg-yellowgreen': (255, 255, 255)}
# for replacing english digits with persian ones
digits = {'1':'۱', '2':'۲', '3':'۳', '4':'۴', '5':'۵', '6':'۶', '7':'۷', '8':'۸', '9':'۹', '0':'۰'}
def en2per(string):
    # it parses string in list for acessing to string charachters
    chars = list(map(lambda x: digits[x] if x.isdecimal() else x,list(string)))
    # it returns an string of above list elements wich joined
    return ''.join([str(x) for x in chars]) 
class aloodak:
    def __init__(self):
        pass
    def parser():
        # request webserver and parsing data
        soup = bs(requests.get("http://airnow.tehran.ir/home/home.aspx").text, "html.parser")
        image_stat = soup.find_all(attrs={'id':'ContentPlaceHolder1_lblAqi3hBoxInfo23'})[0].img['src'].split("/")[-1]
        pollution_rate = int(soup.find_all(attrs={'id':'ContentPlaceHolder1_lblAqi3h'})[0].text)
        color = soup.find_all(attrs={'id':'ContentPlaceHolder1_lblAqi3hBoxInfo23'})[0]['class'][1]
        status = rtl.rtl(soup.find_all(attrs={'id':'ContentPlaceHolder1_lblAqi3hDesc'})[0].text.split()[0])
        return {'color' : color,'polution_rate': pollution_rate, 'image_stat': image_stat, 'status' : rtl.rtl(status)}
class image_maker():
    def __init__(self,data):
        self.name = "report.png"
        self.number_font = ImageFont.truetype("Sahel-Black.ttf", 140) # rate font style
        self.name_font =  ImageFont.truetype("Sahel-Black.ttf", 20) # title font style
        self.badge_font = ImageFont.truetype("Sahel-Bold.ttf", 20) # badge font style
        self.status_font =  ImageFont.truetype("Sahel-Black.ttf", 50) # status font style
        self.color = data['color'] # image color -> for example 'bg-green'
        self.rate = str(data['polution_rate']) # pollution rate
        self.status = data['status'] # pillution status
        self.status = "ناسالم" if self.status.count("حساس") else self.status # changing long status
    def draw(self):
        self.image = Image.open(f"{self.color}.png") # opening image
        self.draw_object = ImageDraw.Draw(self.image) # loafing draw module 
        # wrting data over image
        self.draw_object.text((100, 30), rtl.rtl("شاخص آلودگی هوا"), bg[self.color], font=self.name_font) 
        self.draw_object.text((50, 50) if len(str(self.rate)) == 3 else (100,50), en2per(self.rate),bg[self.color], font=self.number_font)
        self.draw_object.text((400, 100), rtl.rtl(self.status),bg[self.color], font=self.status_font)
        self.draw_object.text((175,250), rtl.rtl("اطلاع‌رسانی غیر‌رسمی آلودک"),bg[self.color],font=self.badge_font) 
        # saving image
        self.image.save(self.name)
        return None