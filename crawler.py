# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup as bs
import requests
import re
import time
import meutil
from mesql import Mesql
import traceback


class Crawler(object):
    '''
        这是类别，方便list.index()
    '''
    _category = [None, "玄幻", "奇幻", "武侠", "仙侠", "都市", "现实", "军事", "历史", "游戏", "体育", "科幻", "灵异", "二次元"
        , "短篇"]

    # 每一网站所对应的规则不一样，暂且写在这里，以后是可以弄到加载文件的（我并没有实现，我直接在方法中一步步去实现了）
    _rule = {
        "qidian": {
            'catid': "",
            'title': "",
            'introduce': "",
            'thumb': "",
            'author': "",
            'wordcount': "",
            'follow': "",
            'hits': ""
        },
        "17k": {
            'catid': "",
            'title': "",
            'introduce': "",
            'thumb': "",
            'author': "",
            'wordcount': "",
            'follow': "",
            'hits': ""
        }

    }
    # 起点  17K 纵横 红袖添香
    _goals = []

    '''
        构造函数
        :arg 要采集的小说网站
    '''
    def __init__(self, goals):
        self._goals = goals

    '''
        析构函数
    '''
    def __del__(self):
        pass

    '''
        统一的爬取入口，方便调用
    '''
    def getAll(self, num=10):
        # 获取所有要抓取的网站
        if '起点' in self._goals:
            self.getQiDian(num)
        if '17k' in self._goals:
            self.get17k(num)
        #自行添加

    '''
        更新所有已经采集过的小说（暂时没有实现）
    '''
    def updateAll(self):
        pass

    '''
        内置爬取的起点网站写法
        只采集了免费小说（付费小说的采集自己参考网上）
        :arg num 是想采集的小说的小说本数（）
    '''
    def getQiDian(self, num=10):
        liis = []
        mesql = Mesql(host='localhost', user='root', password='', database='test')
        try:
            url = "http://a.qidian.com/"
            while liis.__len__() < num:
                res = requests.get(url).text
                html = bs(res, "lxml")
                rule = self._rule["qidian"]
                lis = html.find_all("li", attrs={"data-rid": re.compile('[\d]+')})
                # ul = html.find_all("li", data-rid="all-img-list")
                #  count = lis.__len__()
                liis.extend(lis)
                url = "http:" + html.find("a", class_="lbf-pagination-next")["href"]
        except Exception as e:
            print('e.message:\t', e.args)  # 显示在本机
            print('traceback.print_exc():', traceback.print_exc())  # 显示在本机
            meutil.logmsg('e.message:\t', e.args)
            meutil.logmsg('traceback.print_exc():', traceback.print_exc())

        liis = liis[:num]
        try:
            for i in liis:
                img_info = i.find_all("div",class_="book-img-box")[0]
                thumb = img_info.img["src"]# 获取封面相册

                book_info = i.find_all("div",class_="book-mid-info")[0]
                title = book_info.h4.text# 获取小说名
                fromurl = "http:" + book_info.h4.a["href"]# 获取小说来源
                # 获取信息模块
                ppps = book_info.find_all("p")
                authortag = ppps[0].a
                cattag = authortag.next_sibling.next_sibling
                introtag = ppps[1]
                wordcounttag = ppps[2]
                author = authortag.text# 获取作者
                cat = cattag.text
                catid = self._category.index(cat)# 获取类别
                intro = introtag.text# 获取介绍
                wordcount = wordcounttag.text[:-4]# 获取字数
                created_at = int(time.time())# 创建时间
                updated_at = int(time.time())# 创建更新时间
                # 构建hash元组(暂且只有title和author)
                hashlist = (title, author)
                fromhash = meutil.md5(hashlist)
                if mesql.testhash(fromhash, 'books'):
                    continue
                # print(type(fromhash))
                # exit()
                # 组装插入元组
                bookres = requests.get(fromurl).text
                bookhtml = bs(bookres, "lxml")
                hits = bookhtml.find("div", class_="book-info").find_all("p")[2].find_all("em")[1].text
                book = (catid, title, intro, thumb, author,  wordcount, hits, "起点中文网", fromurl, fromhash,
                        created_at, updated_at)
                ids = mesql.addbooks(book)
                pid = ids[1]
                # pid = 1
                # 获取章节
                lilis = bookhtml.find("div", class_="volume").ul.find_all('li')
                for li in lilis:
                    chapterid = li["data-rid"]# 获取章节id
                    cha_fromurl = li.a["href"]# 获取章节来源网址
                    cha_title = li.text# 获取章节标题
                    cha_fromhash_list = (pid, cha_title) # 获取章节的fromhash 元组
                    cha_fromhash = meutil.md5(cha_fromhash_list)
                    if mesql.testhash(fromhash, 'books_detail'):
                        continue
                    cha_created_at = int(time.time())
                    cha_updated_at = int(time.time())
                    cha_list = (pid, chapterid, cha_title, cha_fromurl, cha_fromhash, cha_created_at, cha_updated_at)
                    cha_id = mesql.adddetail(cha_list)[1]
                    content_html = bs(requests.get("http:"+cha_fromurl).text, "lxml")
                    content = content_html.find("div", class_="read-content").text
                    content = content.replace("　　", "\r\n")
                    file = open(str(cha_id)+cha_title+".txt", "w", encoding="utf-8")
                    file.write(content)
                    file.close()
                    con_list = (cha_id, str(cha_id)+cha_title+".txt")
                    mesql.addcontent(con_list)


        except Exception as e:
            print('e.message:\t', e.args)  # 显示在本机
            print('traceback.print_exc():', traceback.print_exc())  # 显示在本机
            meutil.logmsg('e.message:\t', e.args)
            meutil.logmsg('traceback.print_exc():', traceback.print_exc())

    '''
        采集的17k  没写
    '''
    def get17k(self, num=10):
        pass
