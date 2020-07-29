import logging
import scrapy
import time
import bs4
import os
import re

PHONES = ['xiaomi', 'samsung', 'lg']


def define_logger(name):
    custom_logger = logging.getLogger(name)
    file_path = name + '.log'

    fh = logging.FileHandler(file_path, mode='w')
    ch = logging.StreamHandler()

    formatter = logging.Formatter(
            f'%(asctime)s - {name} - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # fh.setLevel("INFO")
    ch.setFormatter(formatter)

    # custom_logger.addHandler(ch)
    custom_logger.addHandler(fh)
    # custom_logger.propagate = False

    return custom_logger


class GSMArenaSpider(scrapy.Spider):
    name = "smartmania"
    main_url = r'https://smartmania.cz/zarizeni/telefony/'
    my_logger = define_logger("logs")

    def start_requests(self):
        url = GSMArenaSpider.main_url
        self.my_logger.debug(f"Starting Scrapy @ {url}")
        yield scrapy.Request(url=url, callback=self.parse_companies, errback=self.errback_httpbin)

    def parse_companies(self, response):
        body = response.text
        self.my_logger.debug(f"Parsing companies from: {response.url}")

        # with open("last.txt", 'wt') as file:
        #     file.write("pipe broken")

        soup = bs4.BeautifulSoup(body, parser='html-parser', features="lxml")
        find_class = r"aps-brands-list aps-brands-v-list"
        results = soup.find_all(attrs={'class': find_class})[0].find_all('a')
        for res in results:
            text = str(res)
            try:
                found_url = re.findall(f'href="(.*)"', text)[0]
                skip = True
                for ph in PHONES:
                    if ph in found_url:
                        skip = False
                        break

                if skip:
                    continue
            except IndexError:
                continue

            full_url = found_url
            self.my_logger.info(f"Found url: {full_url}")

            self.my_logger.debug(f"Yielding pages")
            yield scrapy.Request(url=full_url, callback=self.parse_pages, errback=self.errback_httpbin)

            self.my_logger.debug(f"Yielding links")
            yield scrapy.Request(url=full_url, callback=self.parse_phone_links, errback=self.errback_httpbin)

    def parse_pages(self, response):
        self.my_logger.debug(f"Searching pages: {response.url}")
        text = response.text
        soup = bs4.BeautifulSoup(text, parser='html-parser', features='lxml')

        class_name = "aps-pagination"
        try:
            result = soup.find_all(attrs={'class': class_name})[0].find_all('a')
        except IndexError:
            return None

        for page in result:
            # self.my_logger.error(f"{page}")
            if "next page-numbers" in str(page):
                continue
            try:
                found_url = re.findall(f'href="(.*)"', str(page))[0]
                self.my_logger.info(f"Found url: {found_url}")
            except IndexError:
                continue
        # with open()

    def parse_phone_links(self, response):
        self.my_logger.info(f"Searching links: {response.url}")

    def parse_phone_specs(self, response):
        pass

    def errback_httpbin(self, failure):
        # log all failures
        url = failure.request.url
        callback = failure.request.callback
        status = failure.value.response.status
        self.my_logger.error(f"Fail status: {status} to get: {url}")
        # self.logger.error(f'Status code: {status}')

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
