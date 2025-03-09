from .NexusPHP import NexusPHP
import re
from utils.custom_requests import CustomRequests
from lxml import etree
from lxml import html
import datetime


class Vicomo(NexusPHP):

    def __init__(self, cookie):
        super().__init__(cookie)

    @staticmethod
    def get_url():
        return "https://ptvicomo.net"

    def send_messagebox(self, message: str, callback=None) -> str:
        return super().send_messagebox(message,
                                       lambda response: "")
    def vs_boss(self):
        vicomo_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
            "sec-ch-ua-arch": "\"x86\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-full-version": "\"133.0.3065.59\"",
            "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"99.0.0.0\", \"Microsoft Edge\";v=\"133.0.3065.59\", \"Chromium\";v=\"133.0.6943.60\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"19.0.0\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "cookie": self.cookie,
            "Referer": "https://ptvicomo.net/customgame.php",
            "Referrer-Policy": "strict-origin-when-cross-origin" 
        }
        vs_boss_url = self.url + "/customgame.php?action=exchange"

        if datetime.date.today().weekday() in [0,2]:
            vs_boss_data = "option=1&vs_member_name=0&submit=%E9%94%8B%E8%8A%92%E4%BA%A4%E9%94%99+-+1v1" # Monday Wednesday
        elif datetime.date.today().weekday() in [1,3]:
            vs_boss_data = "option=1&vs_member_name=0%2C1%2C2%2C3%2C4&submit=%E9%BE%99%E4%B8%8E%E5%87%A4%E7%9A%84%E6%8A%97%E8%A1%A1+-+%E5%9B%A2%E6%88%98+5v5" #Thuesday Thursday
        elif datetime.date.today().weekday() in [4,5,6]:
            vs_boss_data = "option=1&vs_member_name=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16&submit=%E4%B8%96%E7%95%8Cboss+-+%E5%AF%B9%E6%8A%97Sysrous"

        response = CustomRequests.post(vs_boss_url, headers=vicomo_headers, data=vs_boss_data)

        # """提取签到信息"""
        match = re.search(r"\[签到已得(\d+), 补签卡: (\d+)\]", response.text)
        if match:
            days = match.group(1)  # 签到天数
            cards = match.group(2)  # 补签卡数量
            print(f"签到已得: {days} , 补签卡: {cards} 张")
        else:
            print("今日未签到")

        # 从响应中提取重定向 URL
        redirect_url = None
        match = re.search(r"window\.location\.href\s*=\s*'([^']+战斗结果[^']+)'", response.text)
        if match:
            redirect_url = match.group(1)
            print(f"提取到的战斗结果重定向 URL: {redirect_url}")
        else:
            print("未找到战斗结果重定向 URL")
            return None

        # 访问重定向 URL
        battle_result_response = CustomRequests.get(redirect_url, headers=vicomo_headers)
        print(f"战斗结果重定向页面状态码: {battle_result_response.status_code}")
        # print(battle_result_response.text)  # 可选：调试时查看响应内容
        
        # 解析战斗结果页面并提取 battleMsgInput
        parsed_html = html.fromstring(battle_result_response.text)
        battle_msg_input = parsed_html.xpath('//*[@id="battleMsgInput"]')
        if battle_msg_input:
            battle_info = parsed_html.xpath('//*[@id="battleResultStringLastShow"]/div[1]//text()')
            battle_text = ' '.join([text.strip() for text in battle_info if text.strip()])
            print("找到Battle Info:", battle_text) 
            print("找到Battle Result:", parsed_html.xpath('//*[@id="battleResultStringLastShow"]/div[2]/text()')[0].strip())
            return parsed_html.xpath('//*[@id="battleResultStringLastShow"]/div[2]/text()')[0].strip()
        else:
            print("未找到Battle Result")
            return None


class Tasks:
    def __init__(self, cookie: str):
        self.vicomo = Vicomo(cookie)

    def daily_shotbox(self):
        shbox_text_list = ["小象求象草"]
        rsp_text_list = []
        for item in shbox_text_list:
            self.vicomo.send_messagebox(item)
            message_list = self.vicomo.get_message_list()
            if message_list:
                message = message_list[1].get("topic", "")
                rsp_text_list.append(message)
                self.vicomo.set_message_read(message_list[1].get("id", ""))
        return "\n".join(rsp_text_list)

    def daily_checkin(self):
        return self.vicomo.attendance()

    def daily_vs_boss(self):
        for i in range(3):
            self.vicomo.vs_boss()
            time.sleep(10)  # 休眠10秒
        return 
