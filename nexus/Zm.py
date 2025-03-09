import time

from .NexusPHP import NexusPHP
from lxml import etree
from utils.custom_requests import CustomRequests

class Zm(NexusPHP):

    def __init__(self, cookie):
        super().__init__(cookie)

    @staticmethod
    def get_url():
        return "https://zmpt.cc"

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message, lambda response: "")

    def medal_bonus(self):
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "cookie": self.cookie,
            "Referer": "https://zmpt.cc/medal.php",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

        url = self.url + "/javaapi/user/drawMedalGroupReward?medalGroupId=3"

        response = CustomRequests.get(url, headers=headers)
        response_data = response.json()

        ## response_data format like this 
        #{
        #    "serverTime": 1741177064362,
        #    "success": true,
        #    "errorCode": 0,
        #    "errorMsg": "",
        #    "result": {
        #        "rewardAmount": 15000,
        #        "seedBonus": "818255.0"
        #    }
        #}
        reward = response_data['result']['rewardAmount']
        seed_bonus = response_data['result']['seedBonus']

        print(f"梅兰竹菊成套勋章奖励: {reward}")
        print(f"总电力: {seed_bonus}")  

class Tasks:
    def __init__(self, cookie: str):
        self.zm = Zm(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["皮总，求电力", "皮总，求上传"]
        rsp_text_list = []
        for item in shbox_text_list:
            self.zm.send_messagebox(item)
            time.sleep(3)
            message_list = self.zm.get_messagebox()
            if message_list:
                message = message_list[0]
                rsp_text_list.append(message)
        return "\n".join(rsp_text_list)

    def daily_checkin(self):
        return self.zm.attendance()

    def medal_bonus(self):
        return self.zm.medal_bonus()
