#-*- coding: UTF-8 -*-
import requests
import json
from tqdm import tqdm
from time import sleep
from JKTZ.Appointment.DoctorInfo.getDepartment import getDepartment


class getDoctor():
    def __init__(self, headers = None, hospital_id = ""):
        self.doctorinfo = [] #存储医生信息，包含号源总数
        self.doctorinfo_nosum = [] #存储医生信息，不含号源总数
        self.repeat_doctorinfo = [] #重复的医生信息
        self.url = 'http://test.jktz.gov.cn:8083/yygh/yyghAdapter/open/queryDocList'
        self.headers = headers
        self.data = {
                        "body":{
                            "page_index": 1,
                            "hospital_id": "",
                            "department_id": "",
                            "department_type": "",
                            "page_size": 9999,
                            "fileorder": "1",
                            "resources_type": "Y"
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

    def getDI(self):
        DT = getDepartment(self.headers, self.data['body']['hospital_id'])
        dp_info = DT.getDP()
        print('医生信息获取中......')
        for once_dp_info in tqdm(dp_info):
            self.data['body']['department_id'] = once_dp_info['department_id']
            # print(self.data)
            # print(self.data['body']['department_id'])
            try:
                self.response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
            except Exception as err:
                print(err)
                # self.doctorinfo = err
            else:
                self.response = json.loads(self.response.text)
                if self.response["responseFlag"] == "1":
                    # print(json.dumps(self.response))
                    self.doctorlist = self.response['data']['rows']
                    # print(self.response)
                    for doctor in self.doctorlist:
                        mydata = {} #临时存储含号源数
                        mydata2 = {} #临时存储不含号源数
                        mydata['par_department_id'] = once_dp_info['par_department_id']
                        mydata['par_department_name'] = once_dp_info['par_department_name']
                        mydata['department_name'] = doctor['department_name']
                        mydata['department_id'] = doctor['department_id']
                        mydata['doctor_name'] = doctor['doctor_name']
                        mydata['doctor_id'] = doctor['doctor_id']
                        mydata['sum_dqkyysl'] = doctor['sum_dqkyysl']
                        # print(mydata)
                        self.doctorinfo.append(mydata)

                        mydata2['par_department_id'] = once_dp_info['par_department_id']
                        mydata2['par_department_name'] = once_dp_info['par_department_name']
                        mydata2['department_name'] = doctor['department_name']
                        mydata2['department_id'] = doctor['department_id']
                        mydata2['doctor_name'] = doctor['doctor_name']
                        mydata2['doctor_id'] = doctor['doctor_id']
                        self.doctorinfo_nosum.append(mydata2)

                else:
                    # self.doctorinfo = self.response
                    # print(json.dumps(self.data))
                    print(once_dp_info['par_department_id'] + once_dp_info['par_department_name'] +
                                            '-->' + once_dp_info['department_id'] + once_dp_info['department_name'])
                    print(self.response)
            # sleep(0.01)
        print(json.dumps(self.doctorinfo))
        print('医生信息获取完成......')
        # print(self.doctorinfo)
        return self.doctorinfo, self.doctorinfo_nosum

    def getRepeatDoctor(self):
        repeat_doctorinfo = []  # 重复的医生信息
        # doctorid = []
        # count = 0
        # n = 0
        # repeat_num = []
        # notrepeat_id = []   #不重复的医生ID


        # self.doctorinfo  是原始列表
        # docinfo  是列表中的一个字典
        # t  是从字典中创建的元组之一
        seen = set()
        # new_l = []
        for docinfo in self.doctorinfo_nosum:
            t = tuple(docinfo.items())
            # print(t)
            if t not in seen:
                seen.add(t)
                # new_l.append(docinfo)
            else:
                print('医生列表数据重复：' + docinfo['par_department_id'] + docinfo['par_department_name'] +
                                            '-->' + docinfo['department_id'] + docinfo['department_name'] +
                                            '-->' + docinfo['doctor_id'] + docinfo['doctor_name'] )
                repeat_doctorinfo.append(docinfo)

        # print(new_l)
        if repeat_doctorinfo == []:
            print('没有重复医生数据......')
        # print(repeat_doctorinfo)

        # print(json.dumps(repeat_doctorinfo))
        self.repeat_doctorinfo = repeat_doctorinfo
        return self.repeat_doctorinfo

if __name__ == '__main__':
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        # 'userid': 'test',
        # 'password': '123'
    }
    # 妇女儿童医院47258103，温岭市第一人民医院74580626，台州市中心医院47258258，台州医院47258021
    getD = getDoctor(headers,"47258103")
    res = getD.getDI()
    getD.getRepeatDoctor()
    # print(res)





