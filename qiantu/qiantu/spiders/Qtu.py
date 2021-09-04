import scrapy


class QtuSpider(scrapy.Spider):
    name = 'Qtu'
    # allowed_domains = ['www.qiantu.com']
    start_urls = ['https://www.liepin.com/']

    def parse(self, response):
        industry_urls = response.xpath('//h3/a/@href').extract()
        for url in industry_urls:
            yield scrapy.Request(url, callback=self.parse_detail, meta={'dont_redirect': True,
                                                                        'handle_httpstatus_list': [302]})

    def parse_detail(self, response):
        job_name = response.xpath('//ul/li/dl/dd/a/text()').extract()
        for i in range(len(job_name)):
            job_name[i] = re.sub(r'\s+', '', job_name[i])
        job_name = [i for i in job_name if i != '']
        # print(job_name)
        for j_n in job_name:
            s_url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{j_n},2,1.html?'
            # print(s_url)
            yield scrapy.Request(url=s_url, callback=self.parse_third, meta={'type': j_n,
                                                                              'dont_redirect': True,
                                                                              'handle_httpstatus_list': [302]})

    def parse_third(self, response):
        dic = response.xpath('/html/body/script[2]/text()').extract()
        job = re.sub(r'window.__SEARCH_RESULT__ = ', '', dic[0])
        jobs = eval(job)
        for i in range(len(jobs['engine_search_result'])):
            item = QiantuspiderItem()
            item['job_name'] = re.sub(r'\\', '', jobs['engine_search_result'][i]['job_name'])
            item['company_name'] = jobs['engine_search_result'][i]['company_name']
            item['salary'] = re.sub(r'\\', '',  jobs['engine_search_result'][i]['providesalary_text'])
            item['address'] = jobs['engine_search_result'][i]['workarea_text']
            item['company_type'] = jobs['engine_search_result'][i]['companytype_text']
            item['welfare'] = jobs['engine_search_result'][i]['jobwelf']
            item['industry'] = re.sub(r'\\', '', jobs['engine_search_result'][i]['companyind_text'])
            if len(jobs['engine_search_result'][i]['attribute_text']) == 4:
                item['experience'] = re.sub(r'\\', '', jobs['engine_search_result'][i]['attribute_text'][1])
                item['education'] = jobs['engine_search_result'][i]['attribute_text'][2]
            else:
                item['experience'] = ' '
                item['education'] = ' '
            yield item
        # 翻页
        page = int(jobs['total_page'])
        j_name = response.meta['type']
        for i in range(2, page+1):
            s_url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{j_name},2,{i}.html?'
            yield scrapy.Request(url=s_url, callback=self.parse_third, meta={'dont_redirect': True,
                                                                             'handle_httpstatus_list': [302]})