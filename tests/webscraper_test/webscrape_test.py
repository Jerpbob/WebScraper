import pytest
import requests
from bs4 import BeautifulSoup
import lxml

base_url = "https://mangakakalot.com/search/story/"


def webscraper(user_search):
    r = requests.get(base_url + user_search.replace(" ", "_"))
    soup = BeautifulSoup(r.text, 'lxml')
    body = soup.body
    links = body.find(class_="story_item")
    link = links.a['href']
    return link


def webscrape_counter(user_search):
    r = requests.get(base_url + user_search.replace(" ", "_"))
    soup = BeautifulSoup(r.text, 'lxml')
    body = soup.body
    links = body.find_all(class_="story_item")
    return len(links)


def webscraper_with_counter(user_search):
    r = requests.get(base_url + user_search.replace(" ", "_"))
    soup = BeautifulSoup(r.text, 'lxml')
    body = soup.body
    links = body.find(class_="story_item")
    link = links.a['href']
    num_links = len(body.find_all(class_="story_item"))
    manga_id = link[-8:]
    return link, num_links, manga_id


def webscraper_with_limit_8(user_search):
    link_list = list()
    r = requests.get(base_url + user_search.replace(" ", "_"))
    soup = BeautifulSoup(r.text, 'lxml')
    body = soup.body
    links = body.find_all(class_="story_item")
    num_links = len(links)
    if num_links > 8:
        for link in links[:7]:
            link_url = link.a['href']
            manga_id = link_url[-8:]
            link_list.append([link_url, manga_id])
    else:
        for link in links:
            link_url = link.a['href']
            manga_id = link_url[-8:]
            link_list.append([link_url, manga_id])
    return link_list


class TestWebscraper:

    # Following tests for webscraper function
    def test_webscraper_one(self, user_search="Kaguya sama"):
        link = webscraper(user_search=user_search)

        assert link == "https://readmanganato.com/manga-nc952011"

    def test_webscraper_two(self, user_search="One punch man"):
        link = webscraper(user_search=user_search)

        assert link == "https://readmanganato.com/manga-wd951838"

    def test_webscraper_three(self, user_search="ahaguesgubseg"):
        with pytest.raises(Exception):
            link = webscraper(user_search=user_search)

    # Following tests for webscrape_counter function
    def test_webscraper_four(self, user_search="Kaguya sama"):
        num_link = webscrape_counter(user_search=user_search)

        assert num_link == 4

    def test_webscraper_five(self, user_search="one punch man"):
        num_link = webscrape_counter(user_search=user_search)

        assert num_link == 3

    def test_webscraper_five(self, user_search="grand"):
        num_link = webscrape_counter(user_search=user_search)

        assert num_link == 20

    # Following tests for webscraper_with_counter function
    def test_webscraper_six(self, user_search="ouesgosubgsegoub"):
        with pytest.raises(Exception):
            num_link = webscraper_with_counter(user_search=user_search)

    def test_webscraper_seven(self, user_search="Kaguya sama"):
        link, num_link, manga_id = webscraper_with_counter(user_search=user_search)

        assert link == "https://readmanganato.com/manga-nc952011"
        assert num_link == 4
        assert manga_id == "nc952011"

    def test_webscraper_eight(self, user_search="one punch man"):
        link, num_link, manga_id = webscraper_with_counter(user_search=user_search)

        assert link == "https://readmanganato.com/manga-wd951838"
        assert num_link == 3
        assert manga_id == "wd951838"

    # Following tests for webscraper_with_limit_8
    def test_webscraper_nine(self, user_search="Kaguya sama"):
        link_list = list()
        link, num_link, manga_id = webscraper_with_counter(user_search=user_search)
        link_list.append(link)
        link_list.append(manga_id)
        assert webscraper_with_limit_8(user_search=user_search)[0] == link_list

    def test_webscraper_ten(self, user_search="one punch man"):
        link_list = list()
        link, num_link, manga_id = webscraper_with_counter(user_search=user_search)
        link_list.append(link)
        link_list.append(manga_id)
        assert webscraper_with_limit_8(user_search=user_search)[0] == link_list
