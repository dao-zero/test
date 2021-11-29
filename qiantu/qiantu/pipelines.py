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
        job_name = item['job_name']
        try:
            address = item['address']
            print(address)
        except KeyError:
            address = " "
        salary = item['job_salary']

        # salary = re.sub('\\\\', '', job_salary[i])
        if salary != '':
            j_b = re.split('-|/', salary)
            if len(j_b) > 2:
                if j_b[2] == '年':
                    if j_b[1][-1] == '万':
                        j_b[0] = str(round(float(j_b[0]) * 10 / 12, 2))
                        j_b[1] = str(
                            round(float(j_b[1][:-1]) * 10 / 12, 2)) + 'k'
                    j_b[2] = '月'
                elif j_b[2] == '月':
                    if j_b[1][-1] == '万':
                        j_b[0] = str(float(j_b[0]) * 10)
                        j_b[1] = str(float(j_b[1][:-1]) * 10) + 'k'
                    else:
                        j_b[1] = str(float(j_b[1][:-1])) + 'k'
            else:
                salary = "日结"
            salary = j_b[0]+"-"+j_b[1]+"/"+j_b[2]
        # item['job_salary'] = j_b[0] + "-" + j_b[1] + "/" + j_b[2]

        education = item['edu']
        if education == " ":
            education = "面议"
        p_num = item['people_num']
        experience = item['job_exp']
        welfare = item['job_welfare']
        if welfare == "":
            welfare = "面议"
        # print(job_name)
        insert_sql = "INSERT INTO job_first(job_name, address,salary,p_num" \
                     ",education, experience, welfare) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
                         job_name, address, salary, p_num, education, experience, welfare)
        self.cursor.execute(insert_sql)
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
