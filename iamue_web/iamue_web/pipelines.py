# -*- coding: utf-8 -*-
from iamue_web.items import IamueWebItem
from iamue_web import settings
import json ,requests
import os, re, MySQLdb, MySQLdb.cursors
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


#保存成json格式的文件
class IamueWebPipeline(object):
    def __init__(self):
        #打开文件
        self.file = open('data.json','w',encoding='utf-8')
    #该方法用于处理数据
    def process_item(self, item, spider):
        #读取item中的数据
        #匹配A标签，并去除，得到不带连接的文字
        re_content = re.compile('<[\s*a|/a][^>]*>', re.I)
        item['content'] = re_content.sub('',item['content'])
        #去除图片的srcset属性。
        re_content = re.compile('srcset=["|\'][^"|^\']*"')
        item['content'] = re_content.sub('',item['content'])
        #将匹配的图片连接改成本地图片连接
        for index,image_url in enumerate(item['image_urls']):
            item['content'] = item['content'].replace(image_url[0], item['images'][index])
        line = json.dumps(dict(item),ensure_ascii=False)+"\n"
        #写入文件
        self.file.write(line)
        #返回item
        return item

    def open_spider(self,spider):
        pass

    def close_spider(self,spider):
        self.file.close()


##下载图片
class ImageDownloadPipeline(object):
    def process_item(self,item,spider):
        if 'image_urls' in item:  #如果图片地址在项目中
            images = []  #定义图片集
            dir_path = '%s/%s'%(settings.IMAGE_STORE, spider.name)  #创建目录("./iamue")
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['image_urls']:
                us = image_url[0].split('/')[3:]  #切割并获取图片地址的相对地址("***")
                image_file_name = '_'.join(us)  #用_将us列表连接起来
                file_path = '%s/%s' % (dir_path,image_file_name)  #连接成新地址("./iamue/***")
                images.append(file_path)  #图片地址追加到images列表中
                if os.path.exists(file_path):
                    continue
                with open(file_path,'wb') as handle: #用二进制写入file_path
                    response = requests.get(image_url[0], stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
            item['images']  = images  #将遍历的图片地址保存到item的images
        return item


## 保存到数据库
class MysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod #类方法（相当于静态方法），而平常的则叫做实例方法，实例方法第一个参数是self。
    def from_settings(cls,settings):
        dbparams = dict( #获取settings的参数，并将参数以字典的形式写到dbparams
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = False
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',**dbparams)  #标示将字段扩展为关键字参数，相当于host=xxx，db=yyy...
        return cls(dbpool)  #将dbpool付给了这个类，self中可以得到
    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self._conditional_insert,item)  #调用插入方法
        query.addErrback(self._handle_error,item,spider)  #调用异常处理方法
        return item
    def _conditional_insert(self,tx,item):
        sql = "insert into iamue_article(title,content,spider_url) values(%s,%s,%s)"
        params = (item['title'],item['content'],item['spider_url'])
        print(tx.execute(sql,params))
        last_id = tx.lastrowid
        print(tx)
        for index,image in enumerate(item['images']):
            print(index)
            sql = "insert into iamue_images(article_id,images,image_urls) values(%s,%s,%s)"
            params = (last_id, image , item['image_urls'][index])
            tx.execute(sql,params)
    def _handle_error(self, failure, item, spider):
        print(failure)