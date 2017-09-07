# -*- coding: utf-8 -*-
import meutil
import pymysql
import traceback


# 连接数据库
class Mesql(object):
    __singleTon = None

    '''
        本类的配置文件
    '''
    _host = None
    _user = None
    _password = None
    _database = None
    _port = 3306



    '''构造函数
    :arg host 主机
    :arg user 数据库用户名
    :arg password 数据库密码
    :arg database 数据库
    '''
    def __init__(self, host= _host, user = _user, password = _password, database = _database, port = _port):
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        conn.set_charset(charset='utf8')
        self._conn = conn
        self._cursor = conn.cursor()
        self.__singleTon = self

    '''
        单例模式
    '''
    def __new__(cls, *args, **kwargs):
        if cls.__singleTon is None:
            orig = super(Mesql, cls)
            cls.__singleTon = orig.__new__(cls)
        return cls.__singleTon


    '''析构函数
    :arg 无
    '''
    def __del__(self):
        self._cursor.close()
        self._conn.close()

    def baseConfig(self,host = None, user= None, password = None, database = None, port = 3306):
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._port = port


    '''
        获取cursor
        
        返回_cursor
    '''
    def getCursor(self):
        return self._cursor


    '''
        添加小说的，直接添加到数据库
        :arg list是一个元组，因为但是添加是一条一条的添加  所以就没有加入executemany（方便每一次添加的调试）
    '''
    def addbooks(self, list):
        try:
            addSql = "INSERT INTO books(catid, title, introduce, thumb, author, wordcount," \
                     " hits, source, fromurl, fromhash, created_at, updated_at)  VALUES (%s," \
                     " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
            self._cursor.execute(addSql, list)
            self._conn.commit()
            lasdid = self._cursor.lastrowid
            return True, lasdid
        except Exception as e:
            self._conn.rollback()
            print('e.message:\t', e.args)#显示在本机
            print('traceback.print_exc():', traceback.print_exc())#显示在本机
            meutil.logmsg('e.message:\t', e.args)
            meutil.logmsg('traceback.print_exc():', traceback.print_exc())
            return False


    '''
        添加内容（有的人喜欢把小说数据存在数据库，但是我是打算把小说直接存在本地磁盘，然后把路径存在内容数据库）
        :arg list   是一个元组  顺序是id，content 
                id是和books_detail中id相同
                content是内容（每一个章节的/这里添加的是文件路径）
    '''
    def addcontent(self,list):
        try:
            addsql = "INSERT INTO books_content(id,content) VALUES (%s,%s)"
            self._cursor.execute(addsql, list)
            self._conn.commit()
            lasdid = self._cursor.lastrowid
            return True, lasdid
        except Exception as e:
            self._conn.rollback()
            print('e.message:\t', e.args)#显示在本机
            print('traceback.print_exc():',traceback.print_exc())#显示在本机
            meutil.logmsg('e.message:\t', e.args)
            meutil.logmsg('traceback.print_exc():', traceback.print_exc())
            return False

    '''
        加入某一章节的详细信息
        :arg list 是一个元组  
            pid 是小说的id
            chapterid是章节序号
            title  章节名
            hits
            status
            fromurl
            fromhash
            created_at
            updated_at
            
        :return 如果插入成功，返回一个元组（正确，插入id）
                如果失败 返回false
    '''
    def adddetail(self, list):
        try:
            pid = list[0]
            zhangjie = list[2]
            updated_at = list[-1]
            update_list = (zhangjie, updated_at, pid)
            updatesql = "UPDATE books SET zhangjie= %s , updated_at = %s WHERE id = %s"
            self._cursor.execute(updatesql, update_list)
            addsql = "INSERT INTO books_detail(pid,chapterid,title,fromurl,fromhash,created_at," \
                     "updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            self._cursor.execute(addsql, list)
            self._conn.commit()
            lastid = self._cursor.lastrowid
            return True, lastid
        except Exception as e:
            self._conn.rollback()
            print('e.message:\t', e.args)#显示在本机
            print('traceback.print_exc():',traceback.print_exc())#显示在本机
            meutil.logmsg('e.message:\t', e.args)
            meutil.logmsg('traceback.print_exc():', traceback.print_exc())
            return False

    '''
        检测是否采集过
    '''
    def testhash(self, fromhash, table="books"):
        if table == "books_detail":
            return self.testdetail(fromhash)
        else:
            return self.testbooks(fromhash)

    '''
        检测章节是否采集过
    '''
    def testdetail(self, fromhash):
        sql = "SELECT id FROM books_detail WHERE fromhash = %s "
        self._cursor.execute(sql, fromhash)
        if self._cursor.fetchall().__len__() ==1:
            return True
        else:
            return False
    '''
        检测小说是否采集过
    '''
    def testbooks(self, fromhash):
        sql = "SELECT id FROM books WHERE fromhash = %s "
        self._cursor.execute(sql, fromhash)
        if self._cursor.fetchall().__len__() == 1:
            return True
        else:
            return False