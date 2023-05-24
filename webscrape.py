from bs4 import BeautifulSoup
import requests

baseUrl = "https://mangakakalot.com/search/story/"

userSearch = input()

r = requests.get(baseUrl + userSearch.replace(" ", "_"))
soup = BeautifulSoup(r.text, 'html.parser')
print("Grabbing from " + baseUrl + userSearch.replace(" ", "_"))
# head = soup.head
# title = soup.title
body = soup.body

links_in_body = body.find_all(class_="story_item")

for links in links_in_body:
    # print(links.a.prettify())
    # print(links.a.img.prettify())
    print(links.a.img['alt'])