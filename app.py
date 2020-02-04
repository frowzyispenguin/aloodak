from aloodak import *
import os
import time
status = ""
while True:
    data = aloodak.parser()
    info = info_maker(data)
    info.draw()
    info.cpation()
    if status != os.popen("sha1sum report.png").read().split()[0]: 
        try:
            os.system("python3 bot.py")
            status = info.checksum()
        except:
            pass
    else:
        time.sleep(300)
