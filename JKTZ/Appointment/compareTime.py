#-*- coding: UTF-8 -*-
import time

class compareTime():
    def comTime(self, endtime = ''):
        time1 = endtime
        print(time1)
        enddata = str.split(time1, ' ')[0]
        time2 = enddata + ' 12:30:00'
        # print(time2)
        t1 = time.mktime(time.strptime(time1, "%Y-%m-%d %H:%M:%S"))
        t2 = time.mktime(time.strptime(time2, "%Y-%m-%d %H:%M:%S"))
        if t1 < t2:
            msg = '上午排班'
        else:
            msg = '下午排班'

        return enddata,msg


if __name__ == '__main__':
    time1 = '2021-01-18 11:30:00'
    CT = compareTime()
    msg = CT.comTime(time1)
    print(str(msg))