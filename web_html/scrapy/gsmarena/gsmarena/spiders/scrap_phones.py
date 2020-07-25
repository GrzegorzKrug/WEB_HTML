import scrapy
import time
import bs4
import re


class GSMArenaSpider(scrapy.Spider):
    name = "gsmarena"
    main_url = r'https://www.gsmarena.com/'

    def start_requests(self):
        url = GSMArenaSpider.main_url
        yield scrapy.Request(url=url, callback=self.parse_companies, errback=self.errback_httpbin)

    def phone_models(self):
        pass
        r'https://www.gsmarena.com/samsung-phones-9.php'

    def parse_companies(self, response):
        body = response.text
        self.logger.error(f"Parsing companies")

        with open("last.txt", 'wt') as file:
            file.write("pipe broken")

        soup = bs4.BeautifulSoup(body, parser='html-parser')
        find_class = r"brandmenu-v2 light l-box clearfix"
        results = soup.find_all(attrs={'class': find_class}).find_all('li')
        with open("last.txt", 'wt') as file:
            for res in results:
                text = str(res)
                try:
                    url_postfix = re.findall(f'"(.*)"', text)[0]
                    if 'samsung' in url_postfix or 'xiaomi' in url_postfix:
                        pass
                    else:
                        continue
                    full_url = self.main_url + url_postfix
                    file.write(full_url)
                    scrapy.Request(url=full_url, callback=self.parse_phone_links, errback=self.errback_httpbin)
                    scrapy.Request(url=full_url, callback=self.parse_pages, errback=self.errback_httpbin)
                    file.write("\n")
                except IndexError:
                    continue

    def parse_phone_specs(self, response):
        pass

    def parse_pages(self, response):
        text = response.text
        soup = bs4.BeautifulSoup(text, parser='html-parser')
        result = soup.find_all(attrs={'class': 'nav-pages'})

        soup = bs4.BeautifulSoup(str(result), parser='html-parser')
        result = soup.find_all(attrs={'class': 'nav-pages'})

        # with open()

    def parse_phone_links(self, response):
        pass

    def errback_httpbin(self, failure):
        # log all failures
        url = failure.request
        callback = failure.request.callback
        status = failure.value.response.status

        self.logger.error(f'Status code: {status}')

        #
        # # in case you want to do something special for some errors,
        # # you may need the failure's type:
        #
        # if failure.check(HttpError):
        #     # these exceptions come from HttpError spider middleware
        #     # you can get the non-200 response
        #     response = failure.value.response
        #     self.logger.error('HttpError on %s', response.url)
        #
        # elif failure.check(DNSLookupError):
        #     # this is the original request
        #     request = failure.request
        #     self.logger.error('DNSLookupError on %s', request.url)
        #
        # elif failure.check(TimeoutError, TCPTimedOutError):
        #     request = failure.request
        #     self.logger.error('TimeoutError on %s', request.url)
