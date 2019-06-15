# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json

from novalReptile.items import BookInfoItem, ChapterInfoItem
from scrapy import log

dir_name = '/home/speng/DISK/book'


class NovalreptilePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, BookInfoItem):
            title = item['title']
            author = item['author']
            detail = item['detail']
            book_path = os.path.join(dir_name, title)
            if not os.path.exists(book_path):
                os.mkdir(book_path)
                log.msg("new book path ==>:" + book_path, level=log.INFO)

            indexName = os.path.join(book_path, 'index')
            aaa = {}
            aaa['title'] = title
            aaa['author'] = author
            aaa['detail'] = detail
            try:
                output = json.dumps(aaa, indent=4)
            except:
                output = str(aaa)

            f = open(indexName, "w", encoding='utf-8')
            f.write(output)
            f.close()
            print(title + " index write success!")
            return item

        if isinstance(item, ChapterInfoItem):
            name = item['name']
            content = item['content']
            title = item['title']
            index = item['index']

            book_path = os.path.join(dir_name, title)
            if not os.path.exists(book_path):
                raise Exception("书路径不存在,请检查!")

            chapter_name = os.path.join(book_path, index)
            if content:
                f = open(chapter_name, "w", encoding='utf-8')
                f.write(content)
                f.close()
                print("<<%s>> " % title + name)
            else:
                # print("error download:[%s]" % name)
                log.msg("章节内容写入失败", level=log.ERROR)

            return item
