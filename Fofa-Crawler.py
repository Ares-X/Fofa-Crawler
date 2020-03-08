import requests
import re
import base64
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GetFoFa():
    '''
    @list:存放搜索到的url
    @max_page:最大搜索页数（普通会员只能搜索10000条，每页10条）
    @index:当前第几页
    '''
    list = []
    MAX_PAGE = 197
    domain = 'https://fofa.so'
    index = 1
    cookies = {}
    headers = {}


    def __init__(self, key):
        self.getPage(key)

    def getPage(self, key):
        #regx=re.compile(r"javascript:view\('(.*)'\)")
        regx=re.compile(r"javascript:view\(\\'(.*?)\\'\)")  #<a href=\"javascript:view(\'39.106.45.158:8081\')
        basekey = str(base64.b64encode(key.encode('utf-8')), 'utf-8')
        while (self.index <= self.MAX_PAGE):
            url = self.domain + '/result?full=true&page={}&q={}&qbase64={}'.format(self.index, key, basekey)
            print ("Crawling Page {0}".format(self.index))
            try:
                response = requests.get(url, headers=self.headers, cookies=self.cookies)
            except Exception as err:
                print(err)
            target=regx.findall(response.text)
            for i in target:
                print(i)
                self.list.append(i)
            if len(target)==10:
                self.index = self.index + 1
                time.sleep(3)
                continue
            else:
                if response.text == "Retry later\n":
                    print('请求过于频繁，正在尝试重连-------------------')
                    time.sleep(10)
                    continue
                else:
                    print('end!-----------------------------------')
                    break


if __name__ == '__main__':
    #key = input("FOFA KEY:")
    key = 'app="Apache-Flink"'
    GetFoFa(key)
    fileName = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    with open(key.replace('"','')+fileName + '.txt', 'a+') as f:
        for i in GetFoFa.list:
            f.write(i + '\n')
        f.close()
    print('Writing over-----------------------------------')

