import scrapy
import re
import time
import sys
from time import sleep


class OlxAutoSpider(scrapy.Spider):
    name = 'olx_auto'
    allowed_domains = ['olx.ro']
    # start_urls = ['https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/?page=2']
    # start_urls = ['https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/']
    # start_urls = ['https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/bmw/?search%5Bfilter_float_price%3Ato%5D=10000&search%5Bfilter_float_year%3Afrom%5D=2013']
    start_urls= ['https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/bmw/?search%5Bfilter_float_price%3Ato%5D=10000&search%5Bfilter_float_year%3Afrom%5D=2013&search%5Bfilter_float_rulaj_pana%3Ato%5D=175000']
    
    def parse(self, response):

        urls_prom1 = response.css("a.marginright5.link.linkWithHash.detailsLinkPromoted.linkWithHashPromoted").css('a::attr(href)').getall()
        urls_prom2 = response.css("a.marginright5.link.linkWithHash.detailsLinkPromoted").css('a::attr(href)').getall()
        urls_reg = response.css("a.marginright5.link.linkWithHash.detailsLink").css('a::attr(href)').getall()
        urls = urls_prom1+ urls_prom2 + urls_reg

        for url in urls:
            if url is not None:
                yield scrapy.Request(url=url, callback=self.parse_details)
            else:
                break
            time.sleep(0.10)

            try:
                next_url = response.css("span.fbold.next.abs.large").xpath('//a[span = "Urmatoarele anunturi »"]/@href').extract_first()
            except:
                sys.exit(1)

            # if next_page or next_check is not None:

            if next_url is not None:
                yield next_url
                try:
                    yield scrapy.Request(url=next_url, callback=self.parse)
                except:
                    pass
    
    def parse_details(self, response):

        desc = response.css("div#textContent").extract()
        rep = {"*":"","~~<br>":"","<br>":"","~~":"","~":""}
        rep = dict((re.escape(k), v) for k, v in rep.items()) 
        pattern = re.compile("|".join(rep.keys()))
        content = pattern.sub(lambda m: rep[re.escape(m.group(0))], desc[0])
        content = re.sub(r'<(.*)+>', "", content)

        ext_number = response.css("li.offer-bottombar__item").extract()[2]
        number = re.findall('<strong>(.*)</strong>', ext_number)

        print(content)
        print("!!**Response URL**", response.url)
        yield {
            'content': content,
            '**!!URL_LINK**': response.url,
            'Add_Number' : number

        }
