
class HtmlOutputer(object):
    def output(self,datas,name):
        if datas is None:
            return
        if datas == []:
            return
        fout = open("gov/%s.txt" %name,'w',encoding='utf-8')
        for content in datas:
            fout.write("classify:%s"%content['classify'].strip())
            fout.write("\n")
            if content.get('content') is not None:
                for item in content.get('content'):
                    item_name = item["name"].strip().replace("：",":")
                    fout.write(item_name+item["cont"].strip())
                    fout.write("\n")
            elif content.get('item_head') is not None:
                for item in content.get('item_head'):
                    fout.write(item.strip())
                    fout.write("|")
                if content.get('item_cont') is not None:
                    fout.write("\n")
                    for item in content.get('item_cont'):
                        fout.write(content.get('item_type')+":")
                        for info in item:
                            if info is None or info == "":
                                info = " - "
                            elif info is not str:
                                info = str(info)
                            fout.write(info)
                            fout.write("|")
                        fout.write("\n")
                fout.write("\n")
            fout.write("\n")
        fout.close()