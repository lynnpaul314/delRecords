#-*- coding: UTF-8 -*-
import hashlib

class Sign():
    def __init__(self, data):
        self.data = data

    def getData(self):
        data = self.data['body']
        print(data)
        keylist = data.keys()
        STRINGA = []
        for key in keylist:
            key_value = key + '=' + str(data[key])
            STRINGA.append(key_value)
        STRINGA = '&'.join(STRINGA)
        print(STRINGA)
        self.STRINGSignTemp = STRINGA + "&key=MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIOvAdpkrGbR8J+s1i3LrA1s2FQDE7/816ONk2mVTLFfxpz7d2MzxSYUPSAEMptvb8RlMptHmjdAXk0pnfDvExIeuAHS7uhYSlIGpJCKyYyGu+79ijDQwU0RjzHvUf1dAtcMbW5w3ZrMiXAYjPh7jxekiAicV6kaAKpUVGF3XARDAgMBAAECgYA59NBv+lcWedfZrwwk47s5vWoIr8IFgZa22RzEH329o1WayeJluudONyIf8TkEyCr82T1Isl7hamcWtvZYkCBn93/fut7/Teb2WefTvwVRcLpA6eyj+Eq85E4enaqLN2TK8ZXs53IZ72LI1aHJuN0LgUKWsls1lT5fzQgRQozqYQJBAOXQ80zVlSrRmowY/6mvvTwf3J/BaTnvQ6hHA5U/Zyy53K7j08K71loOTCjdp3msltZJrZ4n15EHwoepmXg7x58CQQCSr9LSXfcUR++HDsy1kRcOlGOOaEUvPTRpbsfTcPoSdsECeAtifMfOfnm9P+tFxjSQWKB16nMP4K8uHpDyQVDdAkEAx0/OkoZx1i7uwC42HO5DSk+/wfW10v8FSH4+R0QzsQCIukzwrOTHZFceChsiUk4yiypfHtkjBa8bMRkP9syxtQJAbG7oy3WGtklO+WmpTfbJMo/i4FyX+Amoet/Xe6giVA/RMcAHunA/S5gW6h0cEGIqbSH2y/PZxrzzAoa54zsBSQJAevRm727u9aku6U307mBFU13in7uWNMIgzN61QaTc6iTYtmL50rwi1y4sGPX7MuKkudIWPTUMHyJoa2byelKF6Q=="
        print(self.STRINGSignTemp)

        val = hashlib.md5(self.STRINGSignTemp.encode('utf-8')).hexdigest()
        # val.update(self.STRINGSignTemp.encode("utf-8"))
        # val = val.hexdigest()
        print(val)
        sign = hashlib.sha256(val.encode('utf-8')).hexdigest()
        print(sign)


if __name__ == '__main__':
    data = {
                        "body":{
                            "hospital_id":"74580626",
                            "page_index":1,
                            "page_size":999,
                            "par_department_id":"0",
                            "department_level":"1"
                        },
                        "header":{
                            "sid":"7864A7EA7912EA0BE0500B0A0B514ECB",
                            "sign":"8ac5fd67eaaebf739c5fa1e38b6a4d6cc15a33fc40c649e4844facfa3ae379ae",
                            "timestamp":"20201218105922",
                            "apiVersion":"V1.0",
                            "origin":"h5",
                            "appVersion":"4.5.2"
                        },
                        "tail":{

                        }
                    }
    sign = Sign(data).getData()
