import pytest
import requests
from bs4 import BeautifulSoup
import lxml


class TestWebscraper:
    base_url = "https://mangakakalot.com/search/story/"

    def webscraper(self, user_search):
        r = requests.get(self.base_url + user_search.replace(" ", "_"))
        soup = BeautifulSoup(r.text, 'lxml')
        body = soup.body
        links = body.find(class_="story_item")
        link = links.a['href']
        return link

    def webscrape_counter(self, user_search):
        r = requests.get(self.base_url + user_search.replace(" ", "_"))
        soup = BeautifulSoup(r.text, 'lxml')
        body = soup.body
        links = body.find_all(class_="story_item")
        return len(links)

    def webscraper_with_counter(self, user_search):
        r = requests.get(self.base_url + user_search.replace(" ", "_"))
        soup = BeautifulSoup(r.text, 'lxml')
        body = soup.body
        links = body.find(class_="story_item")
        link = links.a['href']
        num_links = len(body.find_all(class_="story_item"))
        return link, num_links

    def test_webscraper_one(self, user_search="Kaguya sama"):
        link = self.webscraper(user_search=user_search)

        assert link == "https://readmanganato.com/manga-nc952011"

    def test_webscraper_two(self, user_search="One punch man"):
        link = self.webscraper(user_search=user_search)

        assert link == "https://readmanganato.com/manga-wd951838"

    def test_webscraper_three(self, user_search="ahaguesgubseg"):
        with pytest.raises(Exception):
            link = self.webscraper(user_search=user_search)

    def test_webscraper_four(self, user_search="Kaguya sama"):
        num_link = self.webscrape_counter(user_search=user_search)

        assert num_link == 4

    def test_webscraper_five(self, user_search="one punch man"):
        num_link = self.webscrape_counter(user_search=user_search)

        assert num_link == 3

    def test_webscraper_five(self, user_search="grand"):
        num_link = self.webscrape_counter(user_search=user_search)

        assert num_link == 20

    def test_webscraper_six(self, user_search="segsoughsegobu"):
        with pytest.raises(Exception):
            num_link = self.webscraper_counter(user_search=user_search)

    def test_webscraper_seven(self, user_search="Kaguya sama"):
        link, num_link = self.webscraper_with_counter(user_search=user_search)

        assert link == "https://readmanganato.com/manga-nc952011"
        assert num_link == 4

    def test_webscraper_eight(self, user_search="one punch man"):
        link, num_link = self.webscraper_with_counter(user_search=user_search)

        assert link == "https://readmanganato.com/manga-wd951838"
        assert num_link == 3
