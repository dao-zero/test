# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class QiantuPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='qiantu',
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # item = LiepspiderItem()
        industry = item['industry']
        job_name = item['job_name']
        address = item['address']
        salary = item['salary']
        company_name = item['company_name']
        company_type = item['company_type']
        education = item['education']
        experience = item['experience']
        welfare = item['welfare']
        print(job_name)
        insert_sql = "INSERT INTO job_second(industry, job_name, address,salary, company_name, company_type" \
                     ",education, experience, welfare) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                                                                    industry, job_name, address,
                                                                                    salary, company_name, company_type,
                                                                                    education, experience, welfare)
        # insert_sql = "INSERT INTO job_second(industry, job_name, address,salary, company_name, company_type" \
        #              ",education, experience, welfare) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
        #                  item['industry'], item['job_name'], item['address'],
        #                  item['salary'], item['company_name'], item['company_type'],
        #                  item['education'], item['experience'], item['welfare'])

        self.cursor.execute(insert_sql)
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
