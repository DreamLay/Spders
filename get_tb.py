import requests
import hashlib
import json
import time
import re
from urllib import parse
from pprint import pprint
from get_tb_cookies import Taobao


class TbSpider():
    
    def __init__(self):
        # 初识地址
        self.url = 'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?{}'
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36",
            'referer': 'https://h5.m.taobao.com/?sprefer=sypc00',
        }

        # 从已保存cookies中读取
        with open('./cookies/cookies.json', 'r') as f:
            cookie_json = f.read()
        self.cookies = json.loads(cookie_json)

        self.data = r'{"appId":"3113","params":"{\"catmap_version\":\"3.0\",\"tab\":\"on\",\"industry\":\"\"}"}'.replace('\\', '\\')
        self.parameters = dict(jsv='2.4.5', 
            api='mtop.relationrecommend.WirelessRecommend.recommend', 
            v='2.0', preventFallback='true',
            t=str(int(time.time()*1000)),
            appkey='12574478',
            # type='jsonp',
            # dataType='jsonp',
            # callback='mtopjsonp1',
            data=self.data
        )


    # 编码sign
    def md5decode(self):
        self.parameters['data'] = self.data  
        con = '%s&%s&%s&%s' % (
                self.cookies['_m_h5_tk'].split('_')[0], 
                self.parameters['t'],
                self.parameters['appkey'],
                self.parameters['data'])

        return hashlib.md5(con.encode('utf-8')).hexdigest()


    # 请求地址
    def request_url(self):
        self.parameters['sign'] = self.md5decode()
        self.parameters['data'] = parse.quote_plus(self.parameters['data'])
        new_url = self.url + '&'.join(['{}={}'.format(i, self.parameters[i]) for i in self.parameters])
        self.headers['cookie'] = '; '.join([i+'='+self.cookies[i] for i in self.cookies])
        res = requests.get(new_url, headers=self.headers)

        return res.content.decode()


    # 获取响应状态与字典格式内容
    def get_response_status(self):
        content = self.request_url()
        print(content)
        # content_json = re.findall(r'callback\((.*?)\)$',content)[0]
        content_dict = json.loads(content)
        status = True if content_dict['ret'][0] == "SUCCESS::调用成功" else False

        return (status, content)


    def run(self):
        
        (status, content) = (self.get_response_status())
        if status:
            print('调用成功')
            with open('./responseJson/res.json', 'w+') as f:
                f.write(content)

            return

        print('调用失败')
        taobao = Taobao()
        self.cookies = taobao.get_cookie()
        (status, content) = (self.get_response_status())
        with open('./responseJson/res.json', 'w+') as f:
            f.write(content)

        return


if __name__ == "__main__":
    tb = TbSpider()
    tb.run()