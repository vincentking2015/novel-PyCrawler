# -*- coding: utf-8 -*-

import pymysql

'''
    创建数据表
    但是首先要在这里配置好自己的主机名称
    （可以利用mesql模块，在里面写一个配置的 ，可以自己动手写一个）
'''
def createtables():
    conn = pymysql.connect(host="", user="", password="", database="")
    cursor = conn.cursor()
    books_detail_sql = '''CREATE TABLE `books_detail` (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `pid` int(10) unsigned NOT NULL COMMENT 'ID',
              `chapterid` int(10) unsigned NOT NULL COMMENT '序号',
              `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '标题',
              `hits` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '浏览次数',
              `status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '状态',
              `fromurl` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '来源链接',
              `fromhash` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '来源链接hash值',
              `created_at` int(10) NOT NULL,
              `updated_at` int(10) NOT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `books_detail_fromhash_unique` (`fromhash`)
              ) ENGINE=MyISAM AUTO_INCREMENT=228 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;'''

    books_sql = '''CREATE TABLE `books` (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `catid` mediumint(8) unsigned NOT NULL DEFAULT '0' COMMENT '分类ID',
              `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '标题',
              `introduce` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '简介',
              `thumb` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '缩略图',
              `zhangjie` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '章节',
              `author` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '作者',
              `wordcount` double(20,0) unsigned NOT NULL DEFAULT '0' COMMENT '字数',
              `level` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '等级',
              `follow` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '关注人数',
              `hits` double(20,0) unsigned NOT NULL DEFAULT '0' COMMENT '浏览次数',
              `status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '状态',
              `source` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0' COMMENT '来源',
              `fromurl` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0' COMMENT '来源网址',
              `fromhash` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0' COMMENT '来源网址hash,用来判断是否插入过',
              `created_at` int(10) unsigned NOT NULL DEFAULT '0',
              `updated_at` int(11) unsigned NOT NULL DEFAULT '0',
              PRIMARY KEY (`id`),
              UNIQUE KEY `books_fromhash_unique` (`fromhash`),
              KEY `books_catid_index` (`catid`),
              KEY `books_status_index` (`status`)
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            '''
    books_content_sql = '''CREATE TABLE `books_content` (
              `id` int(10) unsigned NOT NULL,
              `content` text COLLATE utf8_unicode_ci NOT NULL COMMENT '小说内容'
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            '''
    books_category_sql = '''CREATE TABLE `books_category` (
              `id` tinyint(4) unsigned NOT NULL AUTO_INCREMENT,
              `category` varchar(255) NOT NULL DEFAULT '' COMMENT '类别',
              PRIMARY KEY (`id`)
            ) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;'''
    cursor.execute(books_sql)
    cursor.execute(books_detail_sql)
    cursor.execute(books_category_sql)
    cursor.execute(books_content_sql)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    createtables();