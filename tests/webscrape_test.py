import pytest
import requests
from bs4 import BeautifulSoup
import lxml


class TestWebscraper:
    base_url = "https://mangakakalot.com/search/story/"

    def test_webscraper_one(self, user_search="Kaguya sama"):
        r = requests.get(self.base_url + user_search.replace(" ", "_"))
        soup = BeautifulSoup(r.text, 'lxml')
        body = soup.body
        links = body.find(class_="story_item")
        link = links.a['href']

        assert link == "https://readmanganato.com/manga-nc952011"

    def test_webscraper_two(self, user_search="One punch man"):
        r = requests.get(self.base_url + user_search.replace(" ", "_"))
        soup = BeautifulSoup(r.text, 'lxml')
        body = soup.body
        links = body.find(class_="story_item")
        link = links.a['href']

        assert link == "https://readmanganato.com/manga-wd951838"

    def test_webscraper_three(self, user_search="ahaguesgubseg"):
        with pytest.raises(Exception):
            r = requests.get(self.base_url + user_search.replace(" ", "_"))
            soup = BeautifulSoup(r.text, 'lxml')
            body = soup.body
            links = body.find(class_="story_item")
            link = links.a['href']

