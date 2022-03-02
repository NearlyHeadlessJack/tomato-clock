# =============================
# tomato-clock.py
# this is a simple application to arrange your time more properly
# author @NearlyHeadlessJack (https://github.com/NearlyHeadlessJack)
# copyright (c) 2022 N.H.J.
# =============================

# import=======================

import time
import os

# =============================

# variables====================

curTime = time.localtime(time.time())#当前时间
beginTime = time.localtime(time.time()) #开始时间
numClocks = 0 #经历的番茄钟数量
skipTimes = 0 #跳过的休息次数
cur = 1
t1 = time.mktime(curTime)
t2 = time.mktime(beginTime)

# =============================

os.system('clear')  # macOS
print ("This is tomato clock, enjoy studying!\n")
while cur:
    if input("If you are ready to study, please press enter!\n") == '':
        numClocks = numClocks + 1
        beginTime = time.localtime(time.time())                     # 记录开始时间
        tB = time.mktime(beginTime)
        tC = time.mktime(curTime)
        while tC-tB <= 5:
            curTime = time.localtime(time.time())
            tC = time.mktime(curTime)
            diff = time.gmtime(tC - tB)
            os.system('clear')                                      # macOS
            print('This is the No.'+ str(numClocks) +' clock!')
            print('{0}  mins  {1} secs remaining!'.format(24-diff.tm_min,59-diff.tm_sec))
            time.sleep(0.98)

        print('\n\nCongratulations! The No.'+ str(numClocks) + ' clock is done.\n\n')
        time.sleep(2)
        if input("Start resting, please press enter!\nSkip rest (which would be accumulated), please enter the other:\n") == '':
            beginTime = time.localtime(time.time())
            tB = time.mktime(beginTime)
            tC = time.mktime(curTime)
            breakTime = skipTimes * 5 + 5  # accumulate break time
            while tC - tB <= breakTime:
                curTime = time.localtime(time.time())
                tC = time.mktime(curTime)
                diff = time.gmtime(tC - tB)
                os.system('clear')  # macOS
                print('Rest time!')
                print('{0}  mins  {1} secs remaining!'.format(skipTimes * 5 + 5 - 1 - diff.tm_min, 59 - diff.tm_sec))
                time.sleep(0.98)
            print('\n\nBreak time is done! Clock will re-startup in 6 secs.')
            time.sleep(6)
            os.system('clear')  # macOS
        else:
            skipTimes = skipTimes + 1

    else:
        cur = 0