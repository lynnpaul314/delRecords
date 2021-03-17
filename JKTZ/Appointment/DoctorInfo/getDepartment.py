#-*- coding: UTF-8 -*-
import requests
import json
from JKTZ.Appointment.DoctorInfo.getPar_Department import getParDepartment


class getDepartment():
    def __init__(self, headers = None, hospital_id = ""):
        self.departmentinfo = []
        # self.chlidinfo = []
        self.url = 'http://test.jktz.gov.cn:8083/yygh/yyghAdapter/open/queryDepList'
        self.headers = headers
        self.data = {
                "body":{
                    "hospital_id":"74580626",
                    "page_index":1,
                    "page_size":9999,
                    "par_department_id":"",
                    "department_level":"2"
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

    def getDP(self):
        PDT = getParDepartment(self.headers, self.data['body']['hospital_id'])
        par_info = PDT.getPD()

        for once_par_info in par_info:
            self.data['body']['par_department_id'] = once_par_info['par_department_id']
            # print(once_par_info['par_department_id'])

            try:
                self.response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
            except Exception as err:
                # print(err)
                self.departmentinfo = err
            else:
                if self.response.status_code == 200:
                    self.response = json.loads(self.response.text)['data']['rows']
                    # print(self.response)

                    for department in self.response:
                        mydata = {}
                        mydata['par_department_id'] = once_par_info['par_department_id']
                        mydata['par_department_name'] = once_par_info['par_department_name']
                        mydata['department_id'] = department['department_id']
                        mydata['department_name'] = department['department_name']
                        # print(data)
                        self.departmentinfo.append(mydata)
                        # print(self.departmentinfo)
                        # mydata = {}

                else:
                    self.departmentinfo = self.response.text

        # sj = {'ss':self.departmentinfo}
        # print(json.dumps(sj))
        return self.departmentinfo



if __name__ == '__main__':
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        # 'userid': 'test',
        # 'password': '123'
    }
    DT = getDepartment(headers, "47258258")
    res = DT.getDP()


    # print(res)





