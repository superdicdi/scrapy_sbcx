# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from sbiao_find.items import SbiaoItemLoader, SbiaoFindItem


class SbcxCrawlSpider(CrawlSpider):
    name = 'sbcx_crawl'
    allowed_domains = ['sbcx.com']
    start_urls = ['http://sbcx.com/sbcx/知呱呱']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//table[@class="jsjieguo"]/tr/td[5]/a'), callback='parse_item', follow=False),  # 提取详情页
        Rule(LinkExtractor(restrict_xpaths='//a[@class ="pagedownval"]'), follow=True),  # 提取下一页
        # Rule(LinkExtractor(), callback='parse_item', follow=False), # LinkExtractor 无法提取到需要的详情 url，目前还不知道原因，猜测是 Scrapy的问题
    )

    def parse_item(self, response):
        item_loader = SbiaoItemLoader(item=SbiaoFindItem(), response=response)
        item_loader.add_xpath("title", '//div[@class="mingchen"]/text()')
        item_loader.add_xpath("apply_num", '//div[@class="xxnrxq_zuob"]/div[1]/div[2]/text()')
        item_loader.add_xpath("sbiao_category", '//div[@class="xxnrxq_zuob"]/div[2]/div[2]/text()')
        item_loader.add_xpath("apply_date", '//div[@class="xxnrxq_zuob"]/div[3]/div[2]/text()')
        item_loader.add_xpath("reg_date", '//div[@class="xxnrxq_zuob"]/div[4]/div[2]/text()')
        item_loader.add_xpath("special_date", '//div[@class="xxnrxq_zuob"]/div[5]/div[2]/text()')
        item_loader.add_xpath("present_status", '//div[@class="xxnrxq_zuob"]/div[6]/div[2]/text()')
        item_loader.add_xpath("apply_name", '//div[@class="xxnrxq_zuob"]/div[7]/div[2]/a[1]/text()')
        item_loader.add_xpath("apply_addr", '//div[@class="xxnrxq_zuob"]/div[8]/div[2]/span/text()')
        item_loader.add_value("image_url", response.meta.get("image_url", ""))
        item_loader.add_xpath("service_list", '//div[@class="xxnrxqsplb_leftDiv"]/text()')
        item_loader.add_xpath("trial_ann_num", '//div[@class="xxnrxqcsrq"]/div[1]/div[2]/text()')
        item_loader.add_xpath("trial_ann_date", '//div[@class="xxnrxqcsrq"]/div[1]/div[4]/text()')
        item_loader.add_xpath("reg_ann_num", '//div[@class="xxnrxqcsrq"]/div[2]/div[2]/text()')
        item_loader.add_xpath("reg_ann_date", '//div[@class="xxnrxqcsrq"]/div[2]/div[4]/text()')
        item_loader.add_xpath("late_date", '//div[@class="xxnrxqcsrq"]/div[3]/div[2]/text()')
        item_loader.add_xpath("inter_reg_date", '//div[@class="xxnrxqcsrq"]/div[3]/div[4]/text()')
        item_loader.add_xpath("priority_date", '//div[@class="xxnrxqcsrq"]/div[4]/div[2]/text()')
        item_loader.add_xpath("agent_name", '//div[@class="xxnrxqcsrq"]/div[4]/div[4]/text()')
        item_loader.add_xpath("sbiao_type", '//div[@class="xxnrxqcsrq"]/div[5]/div[2]/text()')
        item_loader.add_xpath("if_comm_sbiao", '//div[@class="xxnrxqcsrq"]/div[5]/div[4]/text()')
        item_loader.add_xpath("status_record", '//div[@class="xxnrxqspzt_left01"]/div/text()')
        item_loader.add_value("url", response.url)
        sbiao_item = item_loader.load_item()
        yield sbiao_item

    def start_requests(self):
        post_data = {  # value值不能包含int类型
            "username": "18610379194",
            "pwd": "tuyue7208562",
            "reurl": "%2F",
            "func": "0"
        }
        yield scrapy.FormRequest(
            url="http://sbcx.com/?m=Mod&mod=Sys_Login&act=in&reurl=&mid=log_1",
            formdata=post_data,
            callback=self.get_detail_url
        )

    def get_detail_url(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
