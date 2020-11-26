import requests
import random
import os
import re

from multiprocessing import Process
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


def start_scraping():
    URLS = [r"https://emojipedia.org/google/", r"https://emojipedia.org/apple/",
            r"https://emojipedia.org/facebook/", r"https://emojipedia.org/twitter/",
            r"https://emojipedia.org/openmoji/", r'https://emojipedia.org/emojidex/',
            r'https://emojipedia.org/whatsapp/', r'https://emojipedia.org/microsoft/',
            r'https://emojipedia.org/samsung/', r'https://emojipedia.org/lg/',
            r'https://emojipedia.org/joypixels/', r"https://emojipedia.org/messenger/"
            ]
    for url in URLS:
        outPath = [elements for elements in url.split("/") if len(elements) > 0][-1] + "_emotes"
        os.makedirs(outPath, exist_ok=True)

        req = requests.get(url)
        if req.status_code == 200:
            print("Valid")
        else:
            raise ValueError(f"Status code is invalid: {req.status_code}")
        req.raw.decode_content = True
        soup = BeautifulSoup(req.text, "html.parser")
        table = soup.find_all(attrs={"class": "emoji-grid"})[0]

        PROCS = []
        for i, row in enumerate(table):
            proc = Process(target=save_image, args=(row, outPath))
            proc.start()
            PROCS.append(proc)

            if not i % 50:
                [proc.join() for proc in PROCS]
                PROCS = []


def save_image(row_tag, outPath):
    soup_on_row = BeautifulSoup(str(row_tag), "html.parser")
    links = soup_on_row.find_all("a")  # ['href']
    img_tags = soup_on_row.find_all("img")  # ['href']
    # name = name.get("href")

    try:
        if len(links) == 0:
            return None
        # el_a = link[0]
        name = links[0].get("href")
        name = re.sub(r"\W", "", name)
        url = img_tags[0].get('data-src')
        if not url:
            url = img_tags[0].get('src')

        print(f"{outPath} - {name}, {url}")
        im_file_path = os.path.join(outPath, f"{name}.png")

        im_req = requests.get(url, stream=True)
        im_req.raw.decode_content = True
        image = Image.open(im_req.raw)
        if os.path.isfile(im_file_path):
            im_file_path = os.path.join(outPath, f"{name}-{int(random.random() * 100)}")
            print(f"Duplicate!: {im_file_path}")

        image.save(im_file_path)

    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    start_scraping()
