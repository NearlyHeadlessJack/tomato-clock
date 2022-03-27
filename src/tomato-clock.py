# =============================
# tomato-clock.py
# this is a simple application to arrange your time more properly
# author @NearlyHeadlessJack (https://github.com/NearlyHeadlessJack)
# copyright (c) 2022 N.H.J.
# =============================

# import=======================
from pyecharts.charts import Bar
import time
import os
import subprocess
from copy import copy

from pydub import AudioSegment
from pydub.playback import play
import xlrd
from xlrd import xldate_as_tuple
import xlwt
from xlutils.copy import copy
import json
from pathlib import Path


# =============================

# variables====================

localDate = time.strftime("%Y-%m-%d", time.localtime())
curTime = time.localtime(time.time())#当前时间
beginTime = time.localtime(time.time()) #开始时间
global numClocks,history
numClocks = 0 #经历的番茄钟数量
skipTimes = 0 #跳过的休息次数
cur = 1
t1 = time.mktime(curTime)
t2 = time.mktime(beginTime)
song = AudioSegment.from_wav("sound.wav")
path_json = r'/Users/jack/Desktop/repo/Time_Table/data.json'
history = {localDate: 0}

# =============================

# macOS notification===========

def show_notification(title, text):
    cmd = 'display notification \"' + \
          text + '\" with title \"' + title + '\"'
    subprocess.call(["osascript", "-e", cmd])
    play(song)

# =============================
def ReadJson():
    global numClocks,history
    init_data = {localDate: 0}

    if Path(path_json).exists():
        with open(path_json, "r") as f:
            history = json.load(f)
    else:
        with open(path_json, "w+") as f:
            json.dump(init_data, f,indent=4)
        with open(path_json, "r") as f:
            history = json.load(f)

    if localDate not in history.keys():
        history[localDate] = 0
    
    numClocks = int(history[localDate])
        


# # =============================

def WriteJson():
    global history
    history[localDate] += 1
    with open(path_json, "w+") as f:
        json.dump(history, f,indent=4)
    Visualization()
    os.system("./git.sh")
    os.system('clear')  # macOS

# =============================

# visualize====================
def Visualization():
    global history
    bar = Bar()
    list_data = list(history.keys())
    bar.add_xaxis(list_data )
    list_data_2 = [round(i * 25 /60.0,1) for i in list(history.values())]
    bar.add_yaxis("学习时长（小时）",list_data_2 )
    bar.render()
    os.system("cp render.html /Users/jack/Desktop/repo/Time_Table/docs/index.html")

# =============================
ReadJson()
WriteJson()
os.system('clear')  # macOS
out1 = int(357 -curTime.tm_yday+1)
out2 = int((357 -curTime.tm_yday+1)/7)
print("Only "+ str(out1) +" days or "+str(out2)+" weeks left before UNGEE!")
print("\nYou've been learning "+str(numClocks*25)+" minutes today!\n")
time.sleep(3.5)
os.system('clear')  # macOS
print ("This is tomato clock, enjoy studying!\n")
while cur:
    if input("If you are ready to study, please press enter!\n") == '':
        numClocks = numClocks + 1
        show_notification("Study Begins!", "The No." + str(numClocks) + " clock starts.")
        beginTime = time.localtime(time.time())                     # 记录开始时间
        tB = time.mktime(beginTime)
        tC = time.mktime(curTime)
        while tC-tB <= 25 * 60 -4:
            curTime = time.localtime(time.time())
            tC = time.mktime(curTime)
            diff = time.gmtime(tC - tB)
            os.system('clear')                                      # macOS
            print('This is the No.'+ str(numClocks) +' clock!')
            print('{0}  mins  {1} secs remaining!'.format(24-diff.tm_min,59-diff.tm_sec))
            time.sleep(0.98)
        os.system('clear')
        show_notification("Congratulations!", "The No." + str(numClocks) + " clock is done.")
        print('Congratulations! The No.'+ str(numClocks) + ' clock is done.')
        print('\nYou can have a rest for '+str(skipTimes * 5 + 5 )+' minutes!\n')
        time.sleep(2)
        WriteJson()
        if input("Start resting, please press enter!\n\
Skip rest (which would be accumulated), please enter the other:\n") == '':
            beginTime = time.localtime(time.time())
            tB = time.mktime(beginTime)
            tC = time.mktime(curTime)
            breakTime = skipTimes * 5 * 60 + 5 * 60  # accumulate break time
            show_notification("Have a Break! ", "You can rest " + str(skipTimes * 5 + 5) + " minutes.")
            while tC - tB <= breakTime - 4 :
                curTime = time.localtime(time.time())
                tC = time.mktime(curTime)
                diff = time.gmtime(tC - tB)
                os.system('clear')  # macOS
                print('Rest time!')
                print('{0}  mins  {1} secs remaining!'.format(skipTimes * 5 + 5 - 1 - diff.tm_min, 59 - diff.tm_sec))
                time.sleep(0.98)
            os.system('clear')  # macOS
            show_notification("Let's Study!", "Break time is over!")
            print('\n\nBreak time is done! Clock will re-startup in 4 secs.')
            time.sleep(4)
            skipTimes = 0
            os.system('clear')  # macOS
        else:
            skipTimes += 1
    else:
        cur = 0
