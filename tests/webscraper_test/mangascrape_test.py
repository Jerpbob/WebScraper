import pytest
import requests
from bs4 import BeautifulSoup
import lxml
import json


def grab_chap_info(manga_id):
    manga_info_dict = dict()
    author_s = list()
    tags = list()

    base_url = "https://chapmanganato.com/manga-"
    link_url = base_url + manga_id
    link = requests.get(link_url)
    soup = BeautifulSoup(link.text, "lxml")
    soup = soup.body.find(class_="body-site") \
        .find(class_="container-main").find(class_="panel-story-info").find(class_="story-info-right")
    manga_info = soup.tbody.find_all(class_="table-value")
    name = soup.h1.text
    authors = manga_info[1].find_all("a")
    for a in authors:
        author_s.append(a.text)
    status = manga_info[2].text
    tag = manga_info[3].find_all("a")
    for t in tag:
        tags.append(t.text)

    manga_info_dict["Name"] = name
    manga_info_dict["Author/s"] = author_s
    manga_info_dict["Status"] = status
    manga_info_dict["Tag/s"] = tags
    manga_json = json.dumps(manga_info_dict)
    return manga_json


class TestMangascraper:

    def test1(self):
        assert grab_chap_info("nc952011") == \
               '{"Name": "Kaguya-Sama Wa Kokurasetai - Tensai-Tachi No Renai Zunousen",' \
               ' "Author/s": ["Akasaka Aka"],' \
               ' "Status": "Ongoing",' \
               ' "Tag/s": ["Comedy", "Drama", "Romance", "School life", "Seinen"]}'

    def test2(self):
        assert grab_chap_info("wd951838") == \
               '{"Name": "Onepunch-Man",' \
               ' "Author/s": ["One", "Murata Yuusuke"],' \
               ' "Status": "Ongoing",' \
               ' "Tag/s": ["Action", "Comedy", "Fantasy", "Mature", "Mystery", "Psychological", "Sci fi", "Seinen",' \
               ' "Supernatural"]}'

    def test3(self):
        assert grab_chap_info("nu990877") == \
               '{"Name": "Kaoru Hana Wa Rin To Saku",' \
               ' "Author/s": ["Mikami Saka"],' \
               ' "Status": "Ongoing",' \
               ' "Tag/s": ["Comedy", "Drama", "Romance", "School life", "Shounen"]}'
