from bs4 import BeautifulSoup
from gov_spider import html_downloader
import json
from urllib import parse
import re
import time

class HtmlParser(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownload()
        
    def get_other_urls(self,html_cont,type):
        html_cont = html_cont.decode('utf-8')
        patternLice = re.compile(r'otherLicenceDetailInfoUrl\s=\s"(.+)"', re.I | re.M)
        patterPunish = re.compile(r'punishmentDetailInfoUrl\s=\s"(.+)"', re.I | re.M)
        patterExcept = re.compile(r'indBusExcepUrl\s=\s"(.+)"', re.I | re.M)
        patterIll = re.compile(r'IllInfoUrl\s=\s"(.+)"', re.I | re.M)
        url = None
        if type is "liceInfo":
            url = patternLice.search(html_cont)
        elif type is "punishInfo":
            url = patterPunish.search(html_cont)
        elif type is "exceptInfo":
            url = patterExcept.search(html_cont)
        elif type is "illInfo":
            url = patterIll.search(html_cont)
        if url is None:
            return None
        else:
            return url.group(1)
        
    def dateFormat(self,stamp):
        if stamp is None:
            return ""
        timeArray = time.localtime(stamp/1000)
        year = str(timeArray.tm_year)
        month = str(timeArray.tm_mon)
        day = str(timeArray.tm_mday)
        return year+'年'+month+'月'+day+'日'
    
    def parser(self,html_cont):
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        data = []
        
        name = soup.find("h1",class_="fullName").get_text().strip()
        
        for item in soup.find_all(class_="content-i"):
            content = {}
            item_data = []
            item_head = []
            item_cont = []
            if item['id'] == 'content1':
                classify = item.find(id="wrap-base").find(class_="classify").get_text()
                content['classify'] = classify
                for dl in item.find_all("dl"):
                    item_name = dl.find("dt").get_text()
                    item_cont = dl.find("dd").get_text()
                    dic = {"name":item_name,"cont":item_cont}
                    item_data.append(dic)
                content['content'] = item_data
            elif item['id'] == 'content2':
                classify = item.find(class_="classify").get_text()
                content['classify'] = classify
                for th in item.find(class_="specialfuckth").find_all("th"):
                    tr_name = th.get_text()
                    item_head.append(tr_name)
                content['item_head'] = item_head
                content['item_type'] = 'lice'
                otherLicenceDetailInfoUrl = self.get_other_urls(html_cont,"liceInfo")
                if otherLicenceDetailInfoUrl is None:
                    print("no otherLicenceDetailInfoUrl was found")
                    break
                otherLicenceDetailInfoUrl = "http://www.gsxt.gov.cn"+otherLicenceDetailInfoUrl
                print(otherLicenceDetailInfoUrl)
                header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}
#                 req2 = request.Request(url,headers=header)
#                 response2 = request.urlopen(req2)
#                 new_datas = response2.read().decode('utf-8')
                get_datas = self.downloader.download(otherLicenceDetailInfoUrl,header,None).decode('utf-8')
                new_datas = json.loads(get_datas)
                other_data = new_datas.get("data")
                totalPage = new_datas.get("totalPage")
                perPage = new_datas.get("perPage")
                draw = 1
                while draw<totalPage:
                    draw = draw + 1
                    values = {"draw":draw,"start":(draw-1)*perPage,"length":perPage}
                    parse_data = parse.urlencode(values).encode(encoding='UTF8')
                    new_draw_datas_old = self.downloader.download(otherLicenceDetailInfoUrl,header,parse_data).decode('utf-8')
                    new_draw_datas = json.loads(new_draw_datas_old).get("data")
                    other_data.extend(new_draw_datas)
#                 i = 1
                for other in other_data:
                    info = []
#                     info.append(i)
                    info.append(other['licNo'])
                    info.append(other['licName_CN'])
                    info.append(self.dateFormat(other['valFrom']))#格式化时间戳
                    info.append(self.dateFormat(other['valTo']))#格式化时间戳
                    info.append(other['licAnth'])
                    info.append(other['licItem'])
                    item_cont.append(info)
#                     i=i+1
                content['item_cont'] = item_cont    
            elif item['id'] == 'content3':
                classify = item.find(id="punishMentAll").get_text()
                content['classify'] = classify
                for th in item.find(class_="specialfuckth").find_all("th"):
                    tr_name = th.get_text()
                    item_head.append(tr_name)
                content['item_head'] = item_head
                content['item_type'] = 'punish'
                punishmentDetailInfoUrl = self.get_other_urls(html_cont,"punishInfo")
                if punishmentDetailInfoUrl is None:
                    print("no punishmentDetailInfoUrl was found")
                    break
                punishmentDetailInfoUrl = "http://www.gsxt.gov.cn"+punishmentDetailInfoUrl
                print(punishmentDetailInfoUrl)
                header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}
                get_datas = self.downloader.download(punishmentDetailInfoUrl,header,None).decode('utf-8')
                new_datas = json.loads(get_datas)
                other_data = new_datas.get("data")
                totalPage = new_datas.get("totalPage")
                perPage = new_datas.get("perPage")
                draw = 1
                if draw<totalPage:
                    draw = draw + 1
                    values = {"draw":draw,"start":(draw-1)*perPage,"length":perPage}
                    data = parse.urlencode(values).encode(encoding='UTF8')
                    new_draw_datas_old = self.downloader.download(punishmentDetailInfoUrl,header,data).decode('utf-8')
                    new_draw_datas = json.loads(new_draw_datas_old).get("data")
                    other_data.extend(new_draw_datas)
#                 i = 1
                for other in other_data:
                    info = []
#                     info.append(i)
                    info.append(other['penDecNo'])
                    info.append(other['illegActType'])
                    info.append(other['penContent'])
                    info.append(other['penAuth_CN'])
                    info.append(other['penDecIssDate'])
                    info.append(other['publicDate'])
                content['item_cont'] = item_cont
            elif item['id'] == 'content4':
                classify = item.find(class_="classify").get_text()
                content['classify'] = classify
                for th in item.find(id="needPaging_abnormal").find_all("th"):
                    tr_name = th.get_text()
                    item_head.append(tr_name)
                content['item_head'] = item_head
                content['item_type'] = 'except'
                indBusExcepUrl = self.get_other_urls(html_cont,"exceptInfo")
                if indBusExcepUrl is None:
                    print("no indBusExcepUrl was found")
                    break
                indBusExcepUrl = "http://www.gsxt.gov.cn"+indBusExcepUrl
                print(indBusExcepUrl)
                header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}
                get_datas = self.downloader.download(indBusExcepUrl,header,None).decode('utf-8')
                new_datas = json.loads(get_datas)
                other_data = new_datas.get("data")
                totalPage = new_datas.get("totalPage")
                perPage = new_datas.get("perPage")
                draw = 1
                if draw<totalPage:
                    draw = draw + 1
                    values = {"draw":draw,"start":(draw-1)*perPage,"length":perPage}
                    data = parse.urlencode(values).encode(encoding='UTF8')
                    new_draw_datas_old = self.downloader.download(indBusExcepUrl,header,data).decode('utf-8')
                    new_draw_datas = json.loads(new_draw_datas_old).get("data")
                    other_data.extend(new_draw_datas)
#                 i = 1
                for other in other_data:
                    info = []
#                     info.append(i)
                    info.append(other['speCause_CN'])
                    info.append(other['abntime'])
                    info.append(other['decOrg_CN'])
                    info.append(other['remExcpRes_CN'])
                    info.append(other['remDate'])
                    info.append(other['reDecOrg_CN'])
                    item_cont.append(info)
#                     i = i+1
                content['item_cont'] = item_cont
            elif item['id'] == 'content5':
                classify = item.find(class_="classify").get_text()
                content['classify'] = classify
                for th in item.find(id="needPaging_illegal").find_all("th"):
                    tr_name = th.get_text()
                    item_head.append(tr_name)
                content['item_head'] = item_head
                content['item_type'] = 'ill'
                IllInfoUrl = self.get_other_urls(html_cont,"illInfo")
                if IllInfoUrl is None:
                    print("no IllInfoUrl was found")
                    break
                IllInfoUrl = "http://www.gsxt.gov.cn"+IllInfoUrl
                print(IllInfoUrl)
                header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}
                get_datas = self.downloader.download(IllInfoUrl,header,None).decode('utf-8')
                new_datas = json.loads(get_datas)
                other_data = new_datas.get("data")
                totalPage = new_datas.get("totalPage")
                perPage = new_datas.get("perPage")
                draw = 1
                if draw<totalPage:
                    draw = draw + 1
                    values = {"draw":draw,"start":(draw-1)*perPage,"length":perPage}
                    data = parse.urlencode(values).encode(encoding='UTF8')
                    new_draw_datas_old = self.downloader.download(IllInfoUrl,header,data).decode('utf-8')
                    new_draw_datas = json.loads(new_draw_datas_old).get("data")
                    other_data.extend(new_draw_datas)
#                 i = 1
                for other in other_data:
                    info = []
#                     info.append(i)
                    info.append(other['type'])
                    info.append(other['serILLRea_CN'])
                    info.append(other['abntime'])
                    info.append(other['decOrg_CN'])
                    info.append(other['remExcpRes_CN'])
                    info.append(other['remDate'])
                    info.append(other['reDecOrg_CN'])
                    item_cont.append(info)
#                     i = i+1
                content['item_cont'] = item_cont
            data.append(content)
        return data,name