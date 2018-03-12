from gov_spider import html_downloader,html_parser,html_outputer

class Spider(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownload()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
    
    def craw(self,url,header):
        html_cont = self.downloader.download(url,header,None)
        datas,name = self.parser.parser(html_cont)
        self.outputer.output(datas,name)
    
if __name__ == '__main__':
    root_url = 'http://www.gsxt.gov.cn/%7BEe9a1k8ExBpXwR2_udAjBugwLI6n3jOGGkmUjAgtELieSX9gkIpRJxBnpHLTBOExepvRPH7rru-7wc_iQ86wQ7rnLl-f8XX5GkfuJurnWL7Y-D1uoE6k9cAP18gXvAWYaYos0CJABbs5_QYkchVseA-1504165803953%7D'
    root_header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Host":"www.gsxt.gov.cn",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        }
    spider = Spider()
    spider.craw(root_url,root_header)