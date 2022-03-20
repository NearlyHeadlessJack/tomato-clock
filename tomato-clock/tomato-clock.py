# =============================
# tomato-clock.py
# this is a simple application to arrange your time more properly
# author @NearlyHeadlessJack (https://github.com/NearlyHeadlessJack)
# copyright (c) 2022 N.H.J.
# =============================

# import=======================

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


# =============================

# variables====================


curTime = time.localtime(time.time())#当前时间
beginTime = time.localtime(time.time()) #开始时间
global numClocks
numClocks = 0 #经历的番茄钟数量
skipTimes = 0 #跳过的休息次数
cur = 1
t1 = time.mktime(curTime)
t2 = time.mktime(beginTime)
song = AudioSegment.from_wav("sound.wav")
path = r'/Users/jack/Desktop/repo/Time_Table/tomatos.xls'


# =============================

# macOS notification===========

def show_notification(title, text):
    cmd = 'display notification \"' + \
          text + '\" with title \"' + title + '\"'
    subprocess.call(["osascript", "-e", cmd])
    play(song)

# =============================

# read and write xls===========
def readxls():
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)
    date = xldate_as_tuple(table.cell(0, 0).value, 0)
    row = 0
    # print(curTime.tm_mday)
    while date[0] != curTime.tm_year or date[1] != curTime.tm_mon or date[2] != curTime.tm_mday:
        row = row + 1
        date = xldate_as_tuple(table.cell(row, 0).value, 0)
    global numClocks
    numClocks = int(table.cell_value(row, 1) + numClocks)

# =============================

def writexls(times):
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)
    date = xldate_as_tuple(table.cell(0, 0).value, 0)
    row = 0
    # print(curTime.tm_mday)
    while date[0] != curTime.tm_year or date[1] != curTime.tm_mon or date[2] != curTime.tm_mday:
        row = row + 1
        date = xldate_as_tuple(table.cell(row, 0).value, 0)
    workbook = copy(data)
    worksheet = workbook.get_sheet(0)
    worksheet.write(row, 1, times)
    workbook.save(path)

    os.system("zsh -e ./git.sh")
    os.system("clear")
    return

# =============================
readxls()
os.system('clear')  # macOS
out1 = int(357 -curTime.tm_yday+1)
out2 = int((357 -curTime.tm_yday+1)/7)
print("Only "+ str(out1) +" days or "+str(out2)+" weeks left before UNGEE!")
print("You have been learning "+str(numClocks*25)+" minutes today!")
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
        show_notification("Well Done!", "The No."+ str(numClocks) + " clock is done.")
        print('\n\nCongratulations! The No.'+ str(numClocks) + ' clock is done.\n\n')
        writexls(numClocks)
        if input("Start resting, please press enter!\nSkip rest (which would be accumulated), please enter the other:\n") == '':
            beginTime = time.localtime(time.time())
            tB = time.mktime(beginTime)
            tC = time.mktime(curTime)
            breakTime = skipTimes * 5 * 60 + 5 * 60  # accumulate break time
            show_notification("Have A Break!", "You can rest for " + str(skipTimes * 5 + 5) + " minutes!" )
	    skipTimes = 0
            while tC - tB <= breakTime - 4 :
                curTime = time.localtime(time.time())
                tC = time.mktime(curTime)
                diff = time.gmtime(tC - tB)
                os.system('clear')  # macOS
                print('Rest time!')
                print('{0}  mins  {1} secs remaining!'.format(skipTimes * 5 + 5 - 1 - diff.tm_min, 59 - diff.tm_sec))
                time.sleep(0.98)
            show_notification("Let's Study!", "Break time is over!")
            print('\n\nBreak time is done! Clock will re-startup in 6 secs.')
            time.sleep(6)
            os.system('clear')  # macOS
        else:
            skipTimes = skipTimes + 1

    else:
        cur = 0
