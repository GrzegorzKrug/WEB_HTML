import numpy as np
import shutil
import os
import re
import json
import requests
import bs4
from SteamMarketAPI import grab_image

class FindNews():
    def __init__(self):
        self.duckduck_search = 'https://duckduckgo.com/?q='

    # def download_pictures(self):
    #     results = thisSoup.find_all("img", src=re.compile("((https)|(www)).*((\.bmp)|(\.jpg)|(\.png))$"))
    #     for element in results:
    #         new_url = element.get('src')
    #         name = os.path.basename(new_url)
    #
    #         this_image = grab_image(new_url)
    #         width, height = this_image.size
    #         if width > 150 and height > 150:
    #             with open('pics\\' + name, 'wb') as file:
    #                 this_image.save(file)
    #                 print('Saved picture:', file.name)
    #
    # def download_a_pictures(self):
    #     results = thisSoup.find_all("a")
    #     for element in results:
    #         # new_url = element.get('src')

        # for child in element.children:
        #     if type(child) == bs4.element.Tag:
        #         if child.get('src'):
        #             new_url = child.get('src')
        #             name = os.path.basename(new_url)
        #             name = name.replace('?', '')
        #
        #             this_image = grab_image(new_url)
        #             width, height = this_image.size
        #
        #             if width > 150 and height > 150:
        #                 this_type = name[-3:]
        #                 if not('png' in this_type or 'bmp' in this_type or 'jpg' in this_type or 'png' in this_type):
        #                     name += '.png'
        #
        #                 with open('pics\\' + name, 'wb') as file:
        #                     this_image.save(file)
        #                     print('Saved picture:', file.name)

    def search_in_google(self, soup):

        results = soup.find_all('a')  # Google class
        out = []
        for element in results:
            for child in element.children:
                if type(child) == bs4.element.Tag and child.get('href'):
                    out.append(child['href'])
                pass


        return out

    def search_web(self, query):
        url = self.duckduck_search + query
        url = 'https://duckduckgo.com/?q=usa&t=ffab&atb=v131-1&ia=news'
        url = 'https://www.google.com/search?source=hp&ei=Y3z9XKLfM5GOrwTjjK_wCA&q=wiadomo%C5%9Bci&oq=wiad&gs_l=psy-ab.3.0.0i67j0i131i67j0i131l5j0l3.197.1046..1492...0.0..0.144.571.0j5......0....1..gws-wiz.....0..35i39j35i39i19.r1K-4RCuSk8'


        req = requests.get(url, True)
        req.raise_for_status()
        req.raw.decode_content = True
        soup = bs4.BeautifulSoup(req.text, "html.parser")  # as ebook says r.text !
        return soup

    def start(self):
        query = 'wiadomosci'
        soup = self.search_web('None')
        yield

        result = self.search_in_google(soup)
        print(result)



# link_market = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730'
# link2 = 'https://steamcommunity.com/market/listings/730/Gamma%20Case%20Key'
# link3 = 'https://memy.jeja.pl/'



# thisSoup = bs4.BeautifulSoup(r.text, "html.parser")  # as ebook says r.text !



# price_sell_table = thisSoup.select('#market_commodity_forsale_table')
# table = thisSoup.find(lambda tag: tag.name=='market_commodity_forsale_table' and tag.has_attr('id') and tag['id']=="market_commodity_forsale_table")
# rows = table.findAll(lambda tag: tag.name=='tr')


app = FindNews()

for _ in app.start():
    pass

print('Done!')