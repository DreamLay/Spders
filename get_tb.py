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
        self.url = 'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?{}'
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36",
            # 'cookie': 'thw=cn; cna=lc9QE+1xxD0CATo/P/Uy2jAX; hng=CN%7Czh-CN%7CCNY%7C156; tg=0; miid=8623805661003266337; t=4745475684cab026f92f901ade3def0c; UM_distinctid=1673ac281cd3cc-0dff01009bb12d-35677407-1aeaa0-1673ac281cfaa1; tracknick=ljyfys; enc=OywRz8FSNJHdD6EmX1Q5MnP888K7Xta2HTVBWwyr6HsEUXcc4WLZdzXyTEvtGVRrp4LynogxhMIeCssu3MJ29w%3D%3D; v=0; cookie2=3c94256f53834541047a155099552c56; _tb_token_=fefa50bf55ee7; lgc=ljyfys; dnk=ljyfys; skt=944150b901eed856; csg=ec7a85c0; uc3=vt3=F8dByEze4hKro58jJ4U%3D&id2=UUjTSzs8IcZO1w%3D%3D&nk2=D8n1Jp%2F0&lg2=URm48syIIVrSKA%3D%3D; existShop=MTU1MDQ3ODAxNQ%3D%3D; _cc_=U%2BGCWk%2F7og%3D%3D; l=bBg5mFlIvrMEtHu-BOCNVuIRIiQ9kIRAguPRwW4Bi_5p56-DbcQOlllY1FJ6Vj5R_ITp4cyBlup9-etXv; mt=ci=-1_0; uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=Vq8l%2BKCLjhS4UhJVbCU7&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTZ5bDcntXV0g%3D%3D&tag=8&lng=zh_CN; _m_h5_tk=a258f81a8e10bb3cd86aec69360b68f1_1551411147941; _m_h5_tk_enc=85306e557a5beeaed97de23bac91c3ac; isg=BGlpRNoAEeC9niojlyAWMh9ReBMDnhWSLOlYhQte5dCP0onkUYZtOFfQkjDB0fWg',
            'referer': 'https://h5.m.taobao.com/?sprefer=sypc00',
        }
        taobao = Taobao()
        self.cookies = taobao.get_cookie()
        self.headers['cookie'] = '; '.join([i+'='+self.cookies[i] for i in self.cookies])
        data = r'{"appId":"3113","params":"{\"catmap_version\":\"3.0\",\"tab\":\"on\",\"industry\":\"\"}"}'
        data = data.replace('\\', '\\')
        self.parameters = dict(
            jsv='2.4.5',
            t=str(int(time.time()*1000)),
            appkey='12574478',
            api='mtop.relationrecommend.WirelessRecommend.recommend',
            v='2.0',
            preventFallback='true',
            type='jsonp',
            dataType='jsonp',
            callback='mtopjsonp1',
            # data=parse.quote_plus(data),
            data=data
        )


    def md5decode(self):
        print(self.cookies['_m_h5_tk'].split('_')[0]) 
        print(self.parameters['t'])
        con = '%s&%s&%s&%s' % (
                self.cookies['_m_h5_tk'].split('_')[0], 
                self.parameters['t'],
                self.parameters['appkey'],
                self.parameters['data'])

        return hashlib.md5(con.encode('utf-8')).hexdigest()

    def request_url(self):
        self.parameters['sign'] = self.md5decode()
        print(self.parameters['sign'])
        self.parameters['data'] = parse.quote_plus(self.parameters['data'])
        new_url = self.url + '&'.join(['{}={}'.format(i, self.parameters[i]) for i in self.parameters])
        res = requests.get(new_url, headers=self.headers)
        return res.content.decode()


    def run(self):
        content = self.request_url()
        content_json = re.findall(r'mtopjsonp1\((.*?)\)',content)[0]
        with open('./responseJson/res.json', 'w') as f:
            f.write(content_json)


if __name__ == "__main__":
    tb = TbSpider()
    tb.run()