import bs4
from PIL import Image
import requests
from googlesearch import search, search_images
import os
import time
import re  # Docker won't build with slim version


def grab_image_from_url(url, minimal_size=(100, 100)):
    url, valid = validate_url(url)
    if not valid:
        return None

    try:
        req = requests.get(url, stream=True)
        req.raise_for_status()
        req.raw.decode_content = True
        img = Image.open(req.raw)
        width, height = img.size

        if width < minimal_size[0] or height < minimal_size[1]:  # Picture too small
            return None
        return img

    except (ValueError, TypeError, IOError) as e:
        print('Exception, image url invalid:', url)


def validate_url(url):
    out = re.match(r'^//upload.wikimedia.org', url)
    if out is not None:
        # print('Found wikipedia', url)
        url = 'http:' + url
        return url, True

    regex = re.compile(
        r'^(http|www)'\
        r'(?!profile)'\
        r'.*$')

    return url, re.match(regex, url) is not None


def search_images_with_google(query='None', stop_page=5):
    # print('searching', query, stop)
    data = [{'url': url, 'query': query, 'type': 'image'} for url in search_images(query, stop=stop_page)]
    return data


def search_urls_with_google(query='None', stop_page=5):
    # print('searching', query, stop)
    data = [{'url': url, 'query': query, 'type': 'image'} for url in search(query, stop=stop_page)]
    return data


def find_images_on_site(web_url, name='None'):
    req = requests.get(web_url)
    if req.status_code != 200:
        print('Request error: ', req.status_code, web_url)

    soup4 = bs4.BeautifulSoup(req.text, "html.parser")
    A = soup4.find_all('img')

    for element in A:
        if element.get('data-src', None):
            im = grab_image_from_url(element['data-src'])
        elif element.get('src', None):
            im = grab_image_from_url(element['src'])
        else:
            continue

        if im is None:
            continue
        yield im


def save_pic_in_folder(im, dir, name=None):
    if not name:
        name = str(time.time())
    # path = os.path.join(os.path.dirname(__file__), '..', 'pictures', dir)
    path = os.path.join(os.path.dirname(__file__), 'pictures', dir)
    os.makedirs(path, exist_ok=True)
    with open(path + '\\' + name + '.png', 'wb') as file:
        im.save(file)

def run():
    print('What u want to search? ')
    query = input()
    data = search_images_with_google(query)
    for x in data:
        for im in find_images_on_site(x['url'], x['query']):
            save_pic_in_folder(im, x['query'])

if __name__ == '__main__':
    run()

