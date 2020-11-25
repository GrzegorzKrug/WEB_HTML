import requests
import os
import re

from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


def start_scraping():
    outPath = "google_emotes"
    os.makedirs(outPath, exist_ok=True)
    url = r"https://emojipedia.org/google/"
    req = requests.get(url)
    if req.status_code == 200:
        print("Valid")
    else:
        raise ValueError(f"Status code is invalid: {req.status_code}")
    req.raw.decode_content = True
    soup = BeautifulSoup(req.text, "html.parser")
    table = soup.find_all(attrs={"class": "emoji-grid"})[0]
    for i, row in enumerate(table):
        print()
        soup_on_row = BeautifulSoup(str(row), "html.parser")
        links = soup_on_row.find_all("a")  # ['href']
        img_tags = soup_on_row.find_all("img")  # ['href']
        # name = name.get("href")

        try:
            if len(links) == 0:
                continue
            # el_a = link[0]
            name = links[0].get("href")
            name = re.sub(r"\W", "", name)
            url = img_tags[0].get('data-src')
            if not url:
                url = img_tags[0].get('src')

            print(f"{i}, {name}, {url}")
            im_file_path = os.path.join(outPath, f"{name}.png")

            im_req = requests.get(url, stream=True)
            im_req.raw.decode_content = True
            image = Image.open(im_req.raw)
            image.save(im_file_path)

        except Exception as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    start_scraping()
