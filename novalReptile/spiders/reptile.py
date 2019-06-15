# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import os
import scrapy
import re
import hashlib

from novalReptile.items import BookInfoItem, ChapterInfoItem

dir_name = '/home/speng/DISK/book'


class BookSpider(scrapy.spiders.Spider):
    name = "reptile"

    base_book_url = ''
    base_chapter_url = 'https://www.sanjiangge.com/book/51/51161/'

    # book_id_list = ['17834322']

    start_urls = ['https://www.sanjiangge.com/book/51/51161/index.html']

    # for id in book_id_list:
    #     start_urls.append(base_book_url + id)

    def parse(self, response):

        item = BookInfoItem()

        head_list = response.xpath('//*[@id="info"]')

        # for each in head_list:
        item['title'] = head_list.xpath('./h1/text()').extract()[0]
        item['author'] = head_list.xpath('./p[1]/text()').extract()[0]
        item['author'] = self.get_author(item['author'])

        book_chapter_list = response.xpath('//*[@id="list"]/dl/dd')
        chapter_list = []
        detail = []

        for each in book_chapter_list:
            # each_chapter_list = each.xpath('./li')
            # for each_chapter in each_chapter_list:
            chapter_name = self.format_name(each.xpath('./a/text()').extract()[0])
            chapter_url = each.xpath('./a/@href').extract()[0]

            if chapter_name in chapter_list:
                print('Duplication ' + item['title'] + ' : ' + chapter_name)
                continue
            else:
                chapter_detial = {'name': chapter_name, 'url': self.base_chapter_url + chapter_url,
                                  'index': self.md5_chapter_index(chapter_name + chapter_url)}
                chapter_list.append(chapter_name)
                detail.append(chapter_detial)

                file_name = os.path.join(dir_name, item['title'], chapter_detial['index'])
                if not os.path.exists(file_name):
                    request = scrapy.Request(chapter_detial['url'], callback=self.parse_content)
                    request.meta['url'] = chapter_detial['url']
                    request.meta['name'] = chapter_detial['name']
                    request.meta['title'] = item['title']
                    request.meta['index'] = chapter_detial['index']
                    yield request
                else:
                    print(file_name + " ==> is exist")

        item['detail'] = detail
        yield item

    @staticmethod
    def parse_content(response):
        item = ChapterInfoItem()
        url = response.meta['url']
        name = response.meta['name']
        title = response.meta['title']
        index = response.meta['index']

        # tree = html.etree.HTML(response.body)
        tree = response.xpath('//*[@id="content"]/text()').extract()

        content = ""
        for each in tree:
            content = content + '\n' + each

        if content:
            item['content'] = content
            item['name'] = name
            item['title'] = title
            item['index'] = index
            yield item
        else:
            # print("error download:[%s]" % name + url)
            print("error download:[%s]" % name + url)

    @staticmethod
    def get_author(author):
        return author.split('：')[1:][0]

    @staticmethod
    def format_name(name):
        a1 = re.compile('（\d*/\d*）')
        name = a1.sub('', name)

        a2 = re.compile('\(\d*/\d*\)')
        name = a2.sub('', name)

        a3 = re.compile('\d*/\d*')
        name = a3.sub('', name)

        a4 = re.compile('\x7f')
        name = a4.sub('', name)

        name = re.sub('~!@#$%^&*()_\-+=<>?:"{}|,.\/;\\[\]·~！@#￥%……&*（）——\-+={}|《》？：“”【】、；‘’，。、', '', name)
        name = name.strip()
        return name.lower()

    @staticmethod
    def md5_chapter_index(str):
        obj = hashlib.md5(str.encode("utf-8"))  # 加盐
        obj.update(str.encode("utf-8"))  # 把要加密的内容给md5
        return obj.hexdigest()
