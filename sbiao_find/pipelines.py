# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="123456", db="sbiao_data", charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        def if_key(key):
            if dict(item).has_key(key):
                return item[key]
            return ''
        insert_sql = """
                    insert into sbcx(title, apply_num, sbiao_category, apply_date, reg_date,
                                      special_date, present_status, apply_name, apply_addr, image_url, service_list,
                                      trial_ann_num, trial_ann_date, reg_ann_num, reg_ann_date, late_date,
                                      inter_reg_date, priority_date, agent_name, sbiao_type, if_comm_sbiao, status_record, url)
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        self.cursor.execute(insert_sql,
                            (if_key("title"), if_key("apply_num"), if_key("sbiao_category"), if_key("apply_date"),
                             if_key("reg_date"), if_key("special_date"), if_key("present_status"), if_key("apply_name"),
                             if_key("apply_addr"),if_key("image_url"), if_key("service_list"), if_key("trial_ann_num"),
                             if_key("trial_ann_date"),if_key("reg_ann_num"), if_key("reg_ann_date"), if_key("late_date"),
                             if_key("inter_reg_date"),if_key("priority_date"), if_key("agent_name"), if_key("sbiao_type"),
                             if_key("if_comm_sbiao"),if_key("status_record"), if_key("url")))
        self.conn.commit()
        return item


