# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, MapCompose


def remove_char(value):
    return value.replace('\n', "").replace('\r', "").replace('\t', "").replace(" ", "")


class SbiaoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(remove_char)


class SbiaoFindItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    apply_num = scrapy.Field()  # 申请/注册号
    sbiao_category = scrapy.Field()  # 商标类别
    apply_date = scrapy.Field()  # 申请日期
    reg_date = scrapy.Field()  # 注册日期
    special_date = scrapy.Field()  # 专用权期限
    present_status = scrapy.Field()  # 当前状态
    apply_name = scrapy.Field()  # 申请人名称
    apply_addr = scrapy.Field()  # 申请人地址
    image_url = scrapy.Field()  # 商标logo的url
    service_list = scrapy.Field()  # 商品/服务列表
    trial_ann_num = scrapy.Field()  # 初审公告期号
    trial_ann_date = scrapy.Field()  # 初审公告日期
    reg_ann_num = scrapy.Field()  # 注册公告期号
    reg_ann_date = scrapy.Field()  # 注册公告日期
    late_date = scrapy.Field()  # 后期指定日期
    inter_reg_date = scrapy.Field()  # 国际注册日期
    priority_date = scrapy.Field()  # 优先权日期
    agent_name = scrapy.Field()  # 代理人名称
    sbiao_type = scrapy.Field()  # 商标类型
    if_comm_sbiao = scrapy.Field()  # 是否共有商标
    status_record = scrapy.Field(
        output_processor=Join(",")
    )  # 状态记录
    url = scrapy.Field()  # 详情页的url
