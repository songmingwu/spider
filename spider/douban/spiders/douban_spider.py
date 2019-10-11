# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'  # 爬虫名，不能和项目名重复
    allowed_domains = ['movie.douban.com']  # 允许的域名
    start_urls = ['http://movie.douban.com/top250/']   # 入口url, 扔到调度器里面去

    def parse(self, response):
        # 将下载的文件进行解析
        # print(response.text)
        # 循环电影条目：
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            # 导入item 文件
            douban_item = DoubanItem()
            # 写详细的xpath，进行数据解析
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em//text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]//text()").extract()
            # 数据的处理
            for i_content in content:
                douban_item['introduce'] = ''.join(i_content.split())
            douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]//text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']//span//text()").extract_first()
            # 需要将数据yield到pipelines里面去（进行数据的清洗，数据的存储）
            yield douban_item
        # 解析下一页规则，取的后一页的xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250/" + next_link, callback=self.parse)
