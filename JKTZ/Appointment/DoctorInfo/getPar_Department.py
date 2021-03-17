#-*- coding: UTF-8 -*-
import requests
import json


class getParDepartment():
    def __init__(self, headers=None, hospital_id = ""):
        self.par_departmentinfo = []
        self.url = 'http://test.jktz.gov.cn:8083/yygh/yyghAdapter/open/queryDepList'
        self.headers = headers
        self.data = {
                        "body":{
                            "hospital_id":"",
                            "page_index":1,
                            "page_size":999,
                            "par_department_id":"0",
                            "department_level":"1"
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

    def getPD(self):
        # print(self.data)
        try:
            self.response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
            # print(self.response.text)

        except Exception as err:
            # print(err)
            self.par_departmentinfo = err
        else:
            if self.response.status_code == 200:
                self.response = json.loads(self.response.text)['data']['rows']
                # print(self.response)
                data = {}
                for department in self.response:
                    data['par_department_id'] = department['department_id']
                    data['par_department_name'] = department['department_name']
                    # print(data)
                    self.par_departmentinfo.append(data)
                    data = {}
                    # print(self.departmentinfo)

            else:
                self.par_departmentinfo = self.response.text

        # sj = {'ss': self.par_departmentinfo}
        # print(json.dumps(sj))
        return self.par_departmentinfo

if __name__ == '__main__':
    headers = {
                'Content-Type':'application/json; charset=UTF-8',
                'userid':'test',
                'password':'123'
    }
    PDT = getParDepartment(headers,"74580626")
    res = PDT.getPD()
    # print(res)





