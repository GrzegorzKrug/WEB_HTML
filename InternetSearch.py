# from time import time
# now = time()

import numpy as np
# import shutil
# import os
import re
# import json
import requests
import bs4
# from SteamMarketAPI import grab_image  # why it imports so long?
# after = time()-now
# print('Import time = ', after)


class FindNews():
    def __init__(self):
        self.duckduck_search = 'https://duckduckgo.com/?q='

    def get_items_by_key(self, soup, excact_len=False, *args, **keys):
        # Grabing items by keys
        #
        # returns [items^n, href_link]
        key_n = len(keys)
        this_keys = [key.split() for key in keys.values()]
        # print(this_keys)
        results = soup.find_all('a')

        items_out = []
        for element in results:
            my_tuple = []

            for child in element.children:
                try:
                    url = element['href']
                except KeyError:
                    url = 'Not Found in element'

                if type(child) == bs4.element.Tag:
                    try:
                        # abc = [child.text for key in this_keys if child['class'] == key]
                        for key in this_keys:
                            if child['class'] == key:
                                my_tuple.append(child.text)

                    except KeyError:
                        pass
                    pass
            # print(len(my_tuple), key_n)
            if (len(my_tuple) == key_n and excact_len) \
            or (len(my_tuple) >= 1 and not excact_len):
                my_tuple.append(url[7:])  # cuting prefix "/url?q="
                items_out.append(tuple(my_tuple))
        return items_out

    def search_in_google_html(self, soup):


        google_title = 'BNeawe vvjwJb AP7Wnd'  # Google Title
        # google_adres = 'BNeawe UPmit AP7Wnd'  # Google URL

        items = self.get_items_by_key(soup, **{'google_title':google_title})

        return items

    def search_web(self, urls):

        if type(urls) is str:
            urls = [urls]

        for url in urls:
            print('Requesting: {0}'.format(url))
            req = requests.get(url, True)
            req.raise_for_status()
            req.raw.decode_content = True
            soup = bs4.BeautifulSoup(req.text, "html.parser")  # as ebook says r.text !
            yield soup

    def start_searching(self):
        #0 Grabing Google search results
        urls = 'https://www.google.com/search?source=hp&ei=Y3z9XKLfM5GOrwTjjK_wCA&q=wiadomo%C5%9Bci&oq=wiad&gs_l' \
               '=psy-ab.3.0.0i67j0i131i67j0i131l5j0l3.197.1046..1492...0.0..0.144.571.0j5......0....1..gws-wiz.....0..' \
               '35i39j35i39i19.r1K-4RCuSk8'
        soup_list = [*self.search_web(urls)]
        print('Got soup!')
        yield True

        #1 Filtering First Soup
        result = self.search_in_google_html(soup_list[0])
        print('Got links!')
        yield

        #2
        while True:
            print('Select web to grab news')
            for i, item in enumerate(result):
                print(' {0}#'.format(i).ljust(5), item[0])
            choice = input("Give separate numbers or '*' to read all.\n")

            if 'all' in choice.lower() or choice == '*':
                choice = range(len(result))
                break
            else:
                choice = re.findall('\d+', choice)
                if choice != []:
                    choice = [int(num) for num in choice]
                    break

        for ch in  choice:
            try:
                print(result[ch][1])
            except IndexError:
                print('IndexError: invalid index ', ch)
                continue

# price_sell_table = thisSoup.select('#market_commodity_forsale_table')
# table = thisSoup.find(lambda tag: tag.name=='market_commodity_forsale_table' and tag.has_attr('id') and tag['id']=="market_commodity_forsale_table")
# rows = table.findAll(lambda tag: tag.name=='tr')


app = FindNews()

# app = FindNews.start_searching()
end_flag = False

while True:
    for status_is_ok in app.start_searching():
        if not status_is_ok:
            end_flag = True

    if end_flag:
        break

    input('Loop again...')

print('End of excecution...')