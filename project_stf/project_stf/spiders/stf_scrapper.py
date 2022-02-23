#web_scrapping
#site_link : https://www.stfrancismedicalcenter.com/find-a-provider/?fbclid=IwAR0Gwi2H4D1uqJTOQnCsPcbGhf8EH8_B7z-ZdbsPr8xsMN-9TbY4E-EoPc4
#Coded by : Anas bin hasan bhuiyan
#Email address : dsrf.anas@gmail.com
#fb : https://www.facebook.com/anasbinhasan.bhuiyan/


'''
You need to install scrapy_cloudflare_middleware by
pip install scrapy_cloudflare_middleware

2. write those code on your settings.py file
DOWNLOADER_MIDDLEWARES = {
    # The priority of 560 is important, because we want this middleware to kick in just before the scrapy built-in `RetryMiddleware`.
    'scrapy_cloudflare_middleware.middlewares.CloudFlareMiddleware': 560
	}

DUPEFILTER_CLASS = "scrapy.dupefilters.BaseDupeFilter"

'''


from ast import parse
import scrapy
from scrapy import FormRequest
from scrapy.exceptions import CloseSpider
from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware
#uncomment this. And press ctrl and click on CloudflareMiddleware
# a file will open. In this file change "response.status == 503" to "response.status == 503 or response.status == 429" and save
#you can't open the middlewares.py file if you are not in the right environment. So make sure this before running this code


class StfSpider(scrapy.Spider):
    name = 'stf_scrapper'
    start = 1
    incremented_by = 1
    allowed_domains = ['www.stfrancismedicalcenter.com']
    start_urls = [
        'https://www.stfrancismedicalcenter.com/find-a-provider/?fbclid=IwAR0Gwi2H4D1uqJTOQnCsPcbGhf8EH8_B7z-ZdbsPr8xsMN-9TbY4E-EoPc4']

    def parse(self, response):

        if self.start <= 36:
            yield FormRequest.from_response(
                response,
                formxpath="//form[@id='Form_FindAPhysician']",
                formdata={

                    '_m_': 'FindAPhysician',
                    'PhysicianSearch$HDR0$PhysicianName': '',
                    'PhysicianSearch$HDR0$SpecialtyIDs': '',
                    'PhysicianSearch$HDR0$Distance': '5',
                    'PhysicianSearch$HDR0$ZipCodeSearch': '',
                    'PhysicianSearch$HDR0$Keywords': '',
                    'PhysicianSearch$HDR0$LanguageIDs': '',
                    'PhysicianSearch$HDR0$Gender': '',
                    'PhysicianSearch$HDR0$InsuranceIDs': '',
                    'PhysicianSearch$HDR0$AffiliationIDs': '',
                    'PhysicianSearch$HDR0$NewPatientsOnly': '',
                    'PhysicianSearch$HDR0$InNetwork': '',
                    'PhysicianSearch$HDR0$HasPhoto': '',
                    'PhysicianSearch$FTR01$PagingID': f"{self.start}"
                },
                callback=self.aftersf
            )
        else:
            raise CloseSpider("End of session")

        self.start += self.incremented_by
        yield scrapy.Request(
            url='https://www.stfrancismedicalcenter.com/find-a-provider/?fbclid=IwAR0Gwi2H4D1uqJTOQnCsPcbGhf8EH8_B7z-ZdbsPr8xsMN-9TbY4E-EoPc4',
            callback=self.parse
        )

    def aftersf(self, response):
        for item in response.xpath("//li[@data-role='tr']"):
            yield {
                "page number": self.start,
                "name": item.xpath(".//a/div[@class='info']/span[@class='title-style-5']/text()").get(),
                "title": item.xpath(".//a/div[@class='info']/span[@class='title-style-5']/span/text()").get(),
                'specality' : item.xpath(".//a/div[@class='info']/div/span/text()").get(),
                'phone': item.xpath(".//a/div/ul/li[@class='inline-svg phone']/child::node()[3]").get().strip(' \n\t')
                
            }
            