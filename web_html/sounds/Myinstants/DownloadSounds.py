import os
from time import sleep
import re
import shutil
import requests
import bs4


class DownloadSounds:
    # Class to read news from diffrent places in net
    #
    def __init__(self):
        self.soundsweb = 'https://www.myinstants.com/search/'    
        self.starting_page = 1
        self.base_web = 'https://www.myinstants.com'  # this does not work
        self.base_web_PL = 'https://www.myinstants.com/index/pl'
        self.sound_dir = 'sounds_from_myinstants'
        os.makedirs(self.sound_dir, exist_ok=True)

    def get_sounds_urls(self, soup):
        # Filtering soupt to find interesting items
        # IN Soup, {Keys}
        # OUT {key:[items], 'url':[href_links]}
        #

        urls_out = []
        results = soup.find_all('a')

        for element in results:
            if element.get('class', None) == ["instant-link"]:
                # print(element)
                # print(element.text)
                # print(element['href'])
                urls_out.append({'url': self.base_web+element.get('href', None), 'name': element.text})
        return urls_out

    def filter_name(self, unfiltered):
        regex = re.compile(r'[^a-zA-Z0-9\(\) _!]')
        name = regex.sub('', unfiltered)
        return name

    def download_song(self, url, name):
        url = self.base_web + url    
        req = requests.get(url)
        req.raw.decode_content = True

        name = self.filter_name(name)
        try:
            file_path = os.path.join(self.sound_dir , name + '.mp3')
            with open(file_path, 'wb') as file:
                file.write(req.content)
        except PermissionError:
            input('Downlaod Failed! Close file:', name)
        except OSError:
            print('OSError:', name)
            # for something in req.raw.read():
            #     file.write(something)
            # shutil.copyfileobj(req.raw, file)
        pass

    def find_play_button(self, soup):
        new_urls = [None]

        results = soup.find_all('div')
        for element in  results:
            play_button = element.get('onmousedown', None)
            if play_button:
                play_button = play_button[6:-2]
                return  play_button
            # print(element)
            # input()
            # if 'onmousedown' in  element.text.lower():
            #     print(element)

        return new_urls

    def find_next_page(self, soup):
        results = soup.find_all('a')
        for element in results:
            text = element.text.lower()
            if 'page' in text and 'next' in text:
                next_page = self.base_web_PL + str("/") + element['href']
                # print('next page=', next_page)
                return next_page

    def grab_correct_soups(self, urls):
        if type(urls) is str:
            urls = [urls]
        soups = []
        for url in urls:
            try:
                req = requests.get(url)
            except:
                # print('Type Error:', url)
                continue

            if req.status_code != 200:
                print('Status code incorrect:', req.status_code, url)
                continue

            # print('\t', url)
            req.raw.decode_content = True
            soup = bs4.BeautifulSoup(req.text, "html.parser")  # as ebook says r.text !
            soups.append(soup)

        return soups

    def start(self):
        soup = self.grab_correct_soups(self.soundsweb)[0]
        page = self.starting_page - 1
        next_page = None
        while True:
            page += 1
            print('\nThis page is {}'.format(page))
            # print(next_page)

            urls_dicts = self.get_sounds_urls(soup)

            for i,music in enumerate(urls_dicts):

                name = self.filter_name(music['name'])

                flag_found = os.path.isfile(self.sound_dir + '\\' + name + '.mp3')
                if flag_found:
                    continue
                print('\tDownloading {}#, {}'.format((page - 1) * 42 + i + 1, i + 1).ljust(25)
                      + ' {}'.format(music['name']))
                music_soup = self.grab_correct_soups(music['url'])[0]
                button = self.find_play_button(music_soup)
                self.download_song(button, music['name'])


                # print(this_url)
                # print(name)
                # self.download(music['url'], music['name'])
            # print(i)

            next_page = self.find_next_page(soup)
            if next_page is None or page >= 200:
                print('Last page is', page)
                break
            else:
                soup = self.grab_correct_soups(next_page)[0]



app = DownloadSounds()
app.start()


input('End of excecution...')
