# -*- coding: utf-8 -*-
import urlparse
import scrapy
from sbiao_find.items import SbiaoItemLoader, SbiaoFindItem


class SbcxSpider(scrapy.Spider):
    name = 'sbcx'
    allowed_domains = ['www.sbcx.com']
    start_urls = ['http://www.sbcx.com/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    # 需要登录才能爬取数据
    def start_requests(self):
        post_data = { # value值不能包含int类型
            "username": "18610379194",
            "pwd": "tuyue7208562",
            "reurl": "%2F",
            "func": "0"
        }
        yield scrapy.FormRequest(
            url="http://sbcx.com/?m=Mod&mod=Sys_Login&act=in&reurl=&mid=log_1",
            formdata=post_data,
            headers=self.headers,
            callback=self.get_detail_url
        )

    def get_detail_url(self, response):
        # 需要加上 dont_filter=True，不然会过滤掉待爬取的 url
        yield scrapy.Request("http://sbcx.com/sbcx/知呱呱", headers=self.headers,  dont_filter=True)

    def parse(self, response):
        # 提取详情 url
        post_nodes = response.xpath('//table[@class="jsjieguo"]/tr')
        if post_nodes:
            for post_node in post_nodes:
                detail_url = post_node.xpath('td[5]/a/@href').extract_first()
                image_url = post_node.xpath('td[1]/a/img/@src').extract_first()
                if detail_url:  # post_nodes 包含了不需要的 tr ，因此含有详情 url 的 tr 标签才进行解析
                    yield scrapy.Request(url=urlparse.urljoin(response.url, detail_url), headers=self.headers, callback=self.parse_detail, dont_filter=True,
                                         meta={"image_url": urlparse.urljoin(response.url, image_url)})
        # 提取下一页并交给 Scrapy 进行下载
        next_url = response.xpath("//a[@class ='pagedownval']/@href").extract_first()
        if next_url:
            yield scrapy.Request(url=urlparse.urljoin(response.url, next_url), callback=self.parse, headers=self.headers, dont_filter=True)

    def parse_detail(self, response):
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


