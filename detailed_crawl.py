import scrapy
import re


class OlxAutoMetaSpider(scrapy.Spider):
    name = 'olx_auto_meta_v2'
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
                try:
                   yield scrapy.Request(url=url, callback=self.parse_meta)
                except:
                    pass

            next_url = response.css("span.fbold.next.abs.large").xpath('//a[span = "Urmatoarele anunturi »"]/@href').extract_first()

            #if next_page is not None:
            if next_url is not None:
                yield next_url
                try:
                    yield scrapy.Request(url=next_url, callback=self.parse)
                except:
                    pass
        
    def parse_meta(self, response):

        content = response.css("li.offer-details__item")

        ext_number = response.css("li.offer-bottombar__item").extract()[2]
        number = re.findall('<strong>(.*)</strong>', ext_number)
        next_add = "#"*25 + " Next Add " + "#"*25
        meta_dict = {}
        meta_str = ""
        count=0
        for c in content:
            name = c.css("span.offer-details__name").extract_first()
            value = c.css("strong.offer-details__value").extract_first()
            name = re.findall(r'>(.+?)<', name)[0]
            value = re.findall(r'>(.+?)<', value)[0]
            # meta_dict[name] = value
            meta_str = meta_str + " " + name + " " + value


        print('{0}, {1}, {2}'.format(str(number[0]), response.url, meta_str))
        yield {
            'Add Number': str(number[0]),
            'href': response.url,
            'Description': meta_str
        }
