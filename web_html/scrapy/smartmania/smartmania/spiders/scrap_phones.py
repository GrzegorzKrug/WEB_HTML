import logging
import scrapy
import os
import re

ALLOWED_COMPANIES = ['google', 'samsung', 'lg', 'xiaomi']


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

    return custom_logger


class GSMArenaSpider(scrapy.Spider):
    name = "smartmania"
    main_url = r'https://smartmania.cz/zarizeni/telefony/'
    my_logger = define_logger("logs")

    # starts
    def start_requests(self):
        url = GSMArenaSpider.main_url
        self.my_logger.debug(f"Starting Scrapy @ {url}")
        yield scrapy.Request(url=url, callback=self.parse_pages, errback=self.errback_httpbin)

    def parse_companies(self, response):
        """This finds every link to company products, smartwatches also!!!"""

        self.my_logger.debug(f"Parsing companies from: {response.url}")

        find_class = r"aps-brands-list aps-brands-v-list"
        results = response.xpath(f"//ul[@class='{find_class}']//a").css("::attr(href)").extract()

        for full_url in results:
            skip = True
            for company in ALLOWED_COMPANIES:
                if company in full_url:
                    skip = False
                    break
            if skip:
                continue

            self.my_logger.info(f"Found matching company: {full_url}")
            yield scrapy.Request(url=full_url, dont_filter=True,
                                 callback=self.parse_pages, errback=self.errback_httpbin)

    def parse_pages(self, response):
        self.my_logger.debug(f"Searching pages: {response.url}")

        class_name = "aps-pagination"
        try:
            result = response.xpath(f"//div[@class='{class_name}']/a").css("::attr(href)").extract()
        except IndexError:
            self.my_logger.error(f"Index error when searching for pages: {response.url}")
            return None

        result = list(set(result))
        for url in result:
            self.my_logger.info(f"Found pages: {url}")
            yield scrapy.Request(url=url, callback=self.parse_phone_links, errback=self.errback_httpbin,
                                 dont_filter=True)

            yield scrapy.Request(url=url, callback=self.parse_pages, errback=self.errback_httpbin, dont_filter=False)

    def parse_phone_links(self, response):
        self.my_logger.debug(f"Searching links: {response.url}")
        phones_grid = "aps-products aps-row clearfix aps-products-grid"
        phone_class = "aps-product-title"
        results = response.xpath(f"//ul[@class='{phones_grid}']//h2[@class='{phone_class}']").css(
                "::attr(href)").extract()

        for url in results:
            self.my_logger.info(f"Found phone url: {url}")
            allow = False
            for cmp in ALLOWED_COMPANIES:
                if cmp in url.lower():
                    allow = True
                    break
            if not allow:
                continue

            yield scrapy.Request(url=url, callback=self.parse_phone_specs, errback=self.errback_httpbin)

    def parse_phone_specs(self, response):
        tag_name = "aps-main-title"
        tag_table = "aps-features-iconic"

        phone = response.xpath(f"//h1[@class='{tag_name}']").css("::text").extract()[0]
        table = response.xpath(f"//ul[@class='{tag_table}']//strong[@class='aps-feature-vl']").css("::text").extract()

        screen_size = table[0]
        resolution = table[1]
        cpu = table[1]
        camera = table[2]
        mems = table[3].split(',')

        if len(mems) == 2:
            ram, memory = mems
        else:
            ram, memory, _ = mems

        battery = table[4]
        os_sys = table[5]

        with open(f"all_phones.csv", 'at') as file:
            file.write(f"{phone};")
            file.write(f"{response.url};")
            file.write(f"{screen_size};")
            file.write(f"{resolution};")
            file.write(f"{cpu};")
            file.write(f"{camera};")
            file.write(f"{ram};")
            file.write(f"{memory};")
            file.write(f"{battery};")
            file.write(f"{os_sys};")
            file.write('\n')

        self.my_logger.debug(f"Found phone: {phone}")

    def errback_httpbin(self, failure):
        url = failure.request.url
        callback = failure.request.callback
        errback = failure.request.errback  # should work same way as callback... ?
        status = failure.value.response.status
        self.my_logger.error(f"Fail status: {status} @: {url}")

        # Do some stuff
