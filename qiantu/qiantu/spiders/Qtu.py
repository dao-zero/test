import scrapy


class QtuSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['51job.com']
    start_urls = ['https://51job.com/']

    def parse(self, response):
        items = []
        with open(f'D:\\PycharmProjects\\增量式爬虫\\JobGet\\JobGet\\job_list.txt', 'r', encoding='utf8') as f:
            for line in f:
                items.append(line)
        items = [x.strip() for x in items]
        for j_n in items:
            j_n = urllib.parse.quote(j_n)
            s_url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{j_n},2,1.html?'
            yield scrapy.Request(url=s_url, callback=self.parse_detail, meta={'type': j_n,
                                                                              'dont_redirect': True,
                                                                              'handle_httpstatus_list': [302]})

    def parse_detail(self, response):
        html = response.xpath("/html/body/script[2]/text()").extract()
        job = re.sub(r'window.__SEARCH_RESULT__ = ', '', html[0])
        # print(re.findall('"workarea_text":"(.*?)"',job))
        job_url = re.findall(r'"job_href":"(.*?)"', job)
        job_name = re.findall('"job_name":"(.*?)"', job)
        job_salary = re.findall('"providesalary_text":"(.*?)"', job)
        job_welf = re.findall('"jobwelf":"(.*?)"', job)
        job_attribute = re.findall('"attribute_text":\\[.*?\\]', job)
        # jobs = eval(job_attribute[0])

        # print(len(job_attribute))
        for i in range(len(job_attribute)):
            item = JobgetItem()
            job_attribute[i] = "{"+job_attribute[i]+"}"
            job_attribute[i] = json.loads(job_attribute[i])
            add = job_attribute[i]['attribute_text'][0]
            # add1 = add
            # add2 = add
            if job_attribute[i]["attribute_text"][1] != "":
                item['job_exp'] = job_attribute[i]["attribute_text"][1]
            else:
                item['job_exp'] = "面议"
            if re.findall("-", add):
                item['address'] = re.findall("(.*?)-", add)[0]
                # item['small'] = re.findall("-(.+)", add)[0]
                # print(re.findall("(.*?)-", add)[0])
            else:
                item['address'] = add

            if len(job_attribute[i]["attribute_text"]) == 4:
                item['edu'] = job_attribute[i]["attribute_text"][2]
            else:
                item['edu'] = "不限"
            item['people_num'] = job_attribute[i]["attribute_text"][-1]
            url = job_url[i]
            item['job_name'] = job_name[i]
            item['job_salary'] = re.sub('\\\\', '', job_salary[i])
            # 工资处理
            item['job_welfare'] = job_welf[i]

            # print(job_welf[i])
            url = re.sub("\\\\", "", url)
            ex = conn.sadd('job_url', url)
            if ex == 1:
                print("该连接没被爬过")
                yield item
            else:
                print("数据未更新")
        # 翻页
        page = int(re.findall('"total_page":"(.*?)"', job)[0])
        j_name = response.meta['type']
        for i in range(2, page + 1):
            s_url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{j_name},2,{i}.html?'
            yield scrapy.Request(url=s_url, callback=self.parse_detail, meta={'type': j_name,
                                                                              'dont_redirect': True,
                                                                              'handle_httpstatus_list': [302]})
