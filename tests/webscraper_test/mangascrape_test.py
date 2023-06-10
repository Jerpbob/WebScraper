import pytest
import requests
from bs4 import BeautifulSoup
import lxml
import json


class TestMangascraper:
    manga_info_dict = dict()
    name = ''
    author_s = list()
    status = ''
    tags = list()

    def __init__(self, manga_id):
        base_url = "https://chapmanganato.com/manga-"
        link_url = base_url + manga_id
        link = requests.get(link_url)
        soup = BeautifulSoup(link.text, "lxml")
        soup = soup.body.find(class_="body-site")\
            .find(class_="container-main").find(class_="panel-story-info").find(class_="story-info-right")
        manga_info = soup.tbody.find_all(class_="table-value")
        self.name = soup.h1.text
        authors = manga_info[1].a.contents
        for a in authors:
            self.author_s.append(a)
        self.status = manga_info[2].text
        tag = manga_info[3].find_all("a")
        for t in tag:
            self.tags.append(t.text)

        self.manga_info_dict["Name"] = self.name
        self.manga_info_dict["Author/s"] = self.author_s
        self.manga_info_dict["Status"] = self.status
        self.manga_info_dict["Tag/s"] = self.tags
        manga_json = json.dumps(self.manga_info_dict)
        print(manga_json)


test = TestMangascraper("nc952011")

