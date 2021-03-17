#-*- coding: UTF-8 -*-
import requests
import json
from tqdm import tqdm
from time import sleep
from JKTZ.Appointment.DoctorInfo.getDoctor import getDoctor


class getDoctorDetail():
    def __init__(self, headers = None, hospital_id = ""):
        self.doctordetail = []
        self.url = 'http://test.jktz.gov.cn:8083/yygh/yyghAdapter/open/queryDocDetail'
        self.headers = headers
        self.data = {
                    "body": {
                        "hospital_id": "",
                        "department_id": "",
                        "doctor_id": ""
                    },
                    "header": {
                        "sid": "7864A7EA7912EA0BE0500B0A0B514ECB",
                        "sign": "3707f60620e28ee793ce01b3880739dc2a5b044786f7bc049d63763cc7dcc959",
                        "timestamp": "20201223141846",
                        "apiVersion": "V1.0",
                        "origin": "h5",
                        "appVersion": "4.5.3"
                    },
                    "tail": {}
                }
        self.data['body']['hospital_id'] = hospital_id
        self.getD = getDoctor(self.headers, self.data['body']['hospital_id'])


    def getDD(self):
        # getD = getDoctor(self.headers, self.data['body']['hospital_id'])
        doctor_info = self.getD.getDI()[0]
        self.getD.getRepeatDoctor()
        # print(doctor_info)
        # getD.getRepeatDoctor()

        print('获取医生排班信息中......')
        # 循环医生列表数据，进入医生详情页
        num_count = 0
        for once_doctor in (doctor_info):
            # self.data['body']['department_id'] = '69'
            # self.data['body']['doctor_id'] = '745806264539'
            self.data['body']['department_id'] = once_doctor['department_id']
            self.data['body']['doctor_id'] = once_doctor['doctor_id']

            try:
                # print(self.data)
                # 如果请求一次失败，则循环请求，超过6次则继续跳出该循环
                count = 0
                while 1:
                    self.response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
                    # sleep(0.6)
                    res = json.loads(self.response.text)
                    if res['responseFlag'] == '1':
                        break
                    elif res['responseFlag'] == '0':
                        print(once_doctor['par_department_id'] + once_doctor['par_department_name'] +
                              '-->' + once_doctor['department_id'] + once_doctor['department_name'] +
                              '-->' + once_doctor['doctor_id'] + once_doctor['doctor_name'] + '请求失败==================>', count)
                        count += 1
                        sleep(0.6)
                    if count > 10:
                        break
                # self.response = json.loads(self.response.text)
                # print(self.response.text)
            except Exception as err:
                # print(err)
                self.doctordetail = err
            else:
                if self.response.status_code == 200:
                    try:
                        # 获取某个医生详情页号源数
                        schedulinfo = res['data']['schedulings']
                    except Exception as typeerr:
                        print(typeerr)
                        # print(res)
                        print(json.dumps(once_doctor))
                        print('=====================================================================')
                    else:
                        # print(self.response)
                        # print(once_doctor['doctor_name'])
                        source_num = 0
                        # 循环获得某个医生的所有号源
                        for oncedetail in schedulinfo:
                            if oncedetail['stop_treat_flag'] == 'Y' or oncedetail['last_num'] == '0':
                                source_num = source_num
                            else:
                                source_num += int(oncedetail['last_num'])
                                #获得所有医生--医生详情页的号源信息
                                mydata = {}
                                mydata['par_department_id'] = once_doctor['par_department_id']
                                mydata['par_department_name'] = once_doctor['par_department_name']
                                mydata['department_name'] = once_doctor['department_name']
                                mydata['department_id'] = once_doctor['department_id']
                                mydata['doctor_name'] = once_doctor['doctor_name']
                                mydata['doctor_id'] = once_doctor['doctor_id']
                                mydata['schedule_num'] = oncedetail['schedule_num']
                                mydata['schedule_endtime'] = oncedetail['schedule_endtime']
                                mydata['rated_num'] = oncedetail['rated_num']
                                mydata['last_num'] = oncedetail['last_num']
                                self.doctordetail.append(mydata)
                        # print(source_num)

                        #如果号源数不一致，控制台输出相关提示文字
                        if int(once_doctor['sum_dqkyysl']) != source_num:
                            print('医生列表号源总数：' + once_doctor['sum_dqkyysl'])
                            print('医生详情页号源总数：' + str(source_num))
                            print(once_doctor['par_department_id'] + once_doctor['par_department_name'] +
                              '-->' + once_doctor['department_id'] + once_doctor['department_name'] +
                              '-->' + once_doctor['doctor_id'] + once_doctor['doctor_name'] +
                                  '号源数量不一致~~~\n')


                else:
                    self.doctordetail = self.response.text
            # if num_count == 2:
            #     break
            # num_count += 1

        print(len(self.doctordetail))
        # print(json.dumps(self.doctordetail))
        print('获取医生排班信息结束......')
        return self.doctordetail

if __name__ == '__main__':
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        # 'userid': 'test',
        # 'password': '123'
    }
    # 妇女儿童医院47258103，温岭市第一人民医院74580626，台州市中心医院47258258，台州医院47258021
    getDD = getDoctorDetail(headers, "47258103")
    res = getDD.getDD()
    # print(res)





