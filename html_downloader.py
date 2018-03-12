from urllib import request

class HtmlDownload(object):
    def download(self,url,header,data):
        if url is None:
            return None
        if header is None:
            return None
        re = request.Request(url,data=data,headers=header)
        response = request.urlopen(re)
        if response.getcode()!=200:
            print(response.getcode())
            return None
        print("craw:%s" % response.geturl())
        return response.read()
        
        