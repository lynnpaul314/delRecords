#-*- coding: UTF-8 -*-
import requests
import json
from tqdm import tqdm
from time import sleep
from JKTZ.Appointment.DoctorInfo.getDoctor_Detail import getDoctorDetail
from JKTZ.Appointment.compareTime import compareTime
import easygui as g
import sys


class getOrderTimes():
    def __init__(self, headers = None, hospital_id = ""):
        # self.scheduleinfo = []
        self.source_num = [] #分时段页面的号源数临时存储到列表中
        self.CT = compareTime()
        self.url = 'http://test.jktz.gov.cn:8083/yygh/yyghAdapter/open/queryOrderTimes'
        self.headers = headers
        self.data = {
                "body":{
                    "schedule_num": ""
                },
                "header":{
                    "sid":"7864A7EA7912EA0BE0500B0A0B514ECB",
                    "sign":"2c3267720541abf8df357c76e0339a9a20d4f3121e6c60004710ded50153c6f6",
                    "timestamp":"20201218105922",
                    "apiVersion":"V1.0",
                    "origin":"h5",
                    "appVersion":"4.5.2"
                },
                "tail":{}
            }
        self.data['body']['hospital_id'] = hospital_id
        OT = getDoctorDetail(self.headers, self.data['body']['hospital_id'])
        # 获取医生详情页，排班信息
        self.schedule = OT.getDD()

    #获取分时段页面，号源数据，列表形式
    def getOT(self):
        num_count = 0
        #循环获得所有号源对应的分时段数据
        print('获取医生对应号源的分时段排班数据------->开始')
        for once_schedule_info in tqdm(self.schedule):
            self.data['body']['schedule_num'] = once_schedule_info['schedule_num']
            # print(once_par_info['par_department_id'])
            try:
                n = 1
                while 1:
                    self.response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
                    # sleep(0.3)
                    res = json.loads(self.response.text)
                    if res['data'] == []:
                        # print('分时段号源信息获取失败===========>>>>>>>', n)
                        n += 1
                        sleep(0.5)
                    else:
                        # print(res['data'])
                        break
                    if n > 6:
                        # CT.comTime(once_schedule_info['schedule_endtime'])
                        # print(once_schedule_info['schedule_endtime'])
                        # message = self.CT.comTime(once_schedule_info['schedule_endtime'])
                        print('>>>分时段号源信息为空@@@@@@@@@@@>>>>>>')
                        break

            except Exception as err:
                # print(err)
                self.source_num = err
            else:
                if self.response.status_code == 200 and res['responseFlag'] == '1':
                    try:
                        #将分时段页面的号源数临时存储到列表中
                        self.source_num.append(res['data'])
                    except Exception as attErr:
                        print(attErr)
                        print(res['data'])
                else:
                    self.source_num = self.response.text

            # if num_count == 2:
            #     break
            # num_count += 1

        # sj = {'ss':self.departmentinfo}
        # print(json.dumps(sj))
        # print(self.source_num)
        print('获取医生对应号源的分时段排班数据----->结束\n')
        return self.source_num

    #分时段页面，号源总数【小于】医生详情页号源总数的科室
    def lessSource(self):
        count = 0
        print('寻找号源个数【小于】详情页个数的科室-------------------------------------------->>>>>>----------------------------------------------开始')
        for once_schedule_info in self.schedule:
            if int(once_schedule_info['last_num']) > len(self.source_num[count]):
                print('号源总数是：%s' % once_schedule_info['last_num'],
                      '==>分时段页面号源总个数：%d' % len(self.source_num[count]))
                print('分时段页面号源数少的科室：' + once_schedule_info['par_department_id'] + once_schedule_info[
                    'par_department_name'] +
                      '-->' + once_schedule_info['department_id'] + once_schedule_info['department_name'] +
                      '-->' + once_schedule_info['doctor_id'] + once_schedule_info['doctor_name'] +
                      '-->' + str(self.CT.comTime(once_schedule_info['schedule_endtime'])))

            # if count > 50:
            #     break
            count += 1
        print('寻找号源个数【小于】详情页个数的科室-------------------------------------------->>>>>>----------------------------------------------结束\n')

    # 分时段页面，号源总数【大于】医生详情页号源总数的科室
    def biggerSource(self):
        count = 0
        print('寻找号源个数【大于】详情页个数的科室-------------------------------------------->>>>>>----------------------------------------------开始')
        for once_schedule_info in self.schedule:
            if int(once_schedule_info['last_num']) < len(self.source_num[count]):
                # print(self.source_num[count])
                # message = self.CT.comTime(once_schedule_info['schedule_endtime'])
                print('号源总数是：%s' % once_schedule_info['last_num'],
                      '==>分时段页面号源总个数：%d' % len(self.source_num[count]))
                print('分时段页面号源数多的科室：' + once_schedule_info['par_department_id'] + once_schedule_info[
                    'par_department_name'] +
                      '-->' + once_schedule_info['department_id'] + once_schedule_info['department_name'] +
                      '-->' + once_schedule_info['doctor_id'] + once_schedule_info['doctor_name'] +
                      '-->' + str(self.CT.comTime(once_schedule_info['schedule_endtime'])))

            # if count > 50:
            #     break
            count += 1
        print('寻找号源个数【大于】详情页个数的科室-------------------------------------------->>>>>>----------------------------------------------结束\n')

    # 分时段页面，寻找空号源科室
    def emptySource(self):
        count = 0
        print('寻找空号源科室-------------------------------------------->>>>>>----------------------------------------------开始')
        for once_schedule_info in self.schedule:
            if len(self.source_num[count]) == 0:
                print('分时段号源为空的科室：' + once_schedule_info['par_department_id'] + once_schedule_info['par_department_name'] +
                                            '-->' + once_schedule_info['department_id'] + once_schedule_info['department_name'] +
                                            '-->' + once_schedule_info['doctor_id'] + once_schedule_info['doctor_name'] +
                                            '-->' + str(self.CT.comTime(once_schedule_info['schedule_endtime'])))

            # if count > 50:
            #     break
            count += 1
        print('寻找空号源科室-------------------------------------------->>>>>>----------------------------------------------结束\n')

    # 分时段页面，寻找是否存在号源重复的科室
    def findRepeatSource(self):
        count = 0
        print('寻找是否存在重复号源-------------------------------------------->>>>>>----------------------------------------------开始')
        for once_schedule_info in self.schedule:
            for once_source in self.source_num[count]:
                if self.source_num[count].count(once_source) > 1:
                    print('重复号源科室：' + once_schedule_info['par_department_id'] + once_schedule_info[
                        'par_department_name'] +
                          '-->' + once_schedule_info['department_id'] + once_schedule_info['department_name'] +
                          '-->' + once_schedule_info['doctor_id'] + once_schedule_info['doctor_name'] +
                          '-->' + str(self.CT.comTime(once_schedule_info['schedule_endtime'])))
                    break

            # if count > 50:
            #     break
            count += 1
        print('寻找是否存在重复号源-------------------------------------------->>>>>>----------------------------------------------结束\n')

    # 接口返回的rated_num【小于】last_num的科室
    def compareSourceNum(self):
        count = 0
        print('寻找号源总个数【小于】实际号源个数的科室-------------------------------------------->>>>>>----------------------------------------------开始')
        for once_schedule_info in self.schedule:
            if int(once_schedule_info['rated_num']) < int(once_schedule_info['last_num']) or int(once_schedule_info['rated_num']) < len(self.source_num[count]):
                # print(self.source_num[count])
                # message = self.CT.comTime(once_schedule_info['schedule_endtime'])
                print('号源rated_num是：%s' % once_schedule_info['rated_num'],'==>号源last_num是：%s' % once_schedule_info['last_num'],
                      '==>分时段页面号源总个数：%d' % len(self.source_num[count]))
                print('号源总个数与实际号源个数不一致的科室：' + once_schedule_info['par_department_id'] + once_schedule_info[
                    'par_department_name'] +
                      '-->' + once_schedule_info['department_id'] + once_schedule_info['department_name'] +
                      '-->' + once_schedule_info['doctor_id'] + once_schedule_info['doctor_name'] +
                      '-->' + str(self.CT.comTime(once_schedule_info['schedule_endtime'])))

            # if count > 50:
            #     break
            count += 1
        print('寻找号源总个数【小于】实际号源个数的科室-------------------------------------------->>>>>>----------------------------------------------结束\n')


if __name__ == '__main__':
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        # 'userid': 'test',
        # 'password': '123'
    }
    # 妇女儿童医院47258103，温岭市第一人民医院74580626，台州市中心医院47258258，台州医院47258021
    # msg = '妇女儿童医院47258103，温岭市第一人民医院74580626，台州市中心医院47258258，台州医院47258021\n' + '请输入需要检查的医疗机构代码'
    # def out_put_value():
    #     try:
    #         hospitalid = g.enterbox(msg, '输入医疗机构代码')
    #         print(hospitalid)
    #         # print(type(hospitalid))
    #     except TypeError:
    #         sys.exit(1)
    #     else:
    #         try:
    #             int(hospitalid)
    #         except ValueError:
    #             g.msgbox('请输入正确医疗机构代码')
    #             out_put_value()
    #         except TypeError:
    #             sys.exit(1)
    #     return hospitalid
    hospitalid = "47258103"
    DT = getOrderTimes(headers, hospitalid)
    DT.getOT()
    DT.lessSource()
    DT.biggerSource()
    DT.emptySource()
    DT.findRepeatSource()
    DT.compareSourceNum()

    # print(res)





