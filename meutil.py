# -*- coding: utf-8 -*-

import hashlib
import logging

'''
   md5加密
   为的是简化md5的过程避免重复写 
   :arg list 是一个list，也可以是一个元组 。。。
'''
def md5(list):
    data = ""
    for item in list:
        if not isinstance(item, str):
            item = str(item)
        data += item
    return hashlib.md5(data.encode(encoding="utf-8")).hexdigest()


'''
    logmsg 将记录日志的功能进行整合
    :arg msg 需要记录的信息
    :arg mode 信息级别，默认是info
'''
def logmsg(msg,mode="info"):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelno)s %(levelname)s %(pathname)s %(filename)s %(funcName)s %(lineno)d %(asctime)s'
                               ' %(thread)d %(threadName)s %(process)d %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='myapp.log',
                        filemode='w')
    if mode.upper()=="NOTSET":
        logging.warning('This is NOTSET message：'+msg)
    elif mode.upper()=="DEBUG":
        logging.debug('This is DEBUG message：'+msg)
    elif mode.upper()=="WARNING":
        logging.warning('This is WARNING message：'+msg)
    elif mode.upper()=="ERROR":
        logging.error('This is ERROR message：'+msg)
    elif mode.upper()=="CRITICAL":
        logging.error('This is CRITICAL message：'+msg)
    else:
        logging.info('This is info message：'+msg)
