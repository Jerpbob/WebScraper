from bs4 import BeautifulSoup
import requests
import json
import lxml


# TODO: implement a way so that the script scrapes from several websites
# --- OLD CODE JUST TO HELP ME STRUCTURE THE LAYOUT OF THE PROJECT AND DEVELOPMENT OF FUNCTIONS --- #
# def mangakakalot_manga_search_webscraper(user_search = "kaguya sama"):
#     base_url = "https://mangakakalot.com/search/story/"
#
#     # FUTURETODO: Find a way to implement a frontend that takes input from the user
#     # and then sends that input into this script (or a future backend)
#     # userSearch = input()
#
#     # list of the search results with their respective data (title, author, link to manga, tags, and id)
#     link_list = list()
#
#     # simply using the request library to send a request to the url in order to start extracting data
#     # with beautifulsoup
#     r = requests.get(base_url + user_search.replace(" ", "_"))
#     soup = BeautifulSoup(r.text, 'lxml')
#     print("Grabbing from " + base_url + user_search.replace(" ", "_"))
#     body = soup.body
#     links_in_body = body.find_all(class_="story_item")
#
#     for links in links_in_body:
#         try:
#             # print(links.a.prettify())
#             # print(links.a.img.prettify())
#
#             # create a dictionary to put the extracted data into
#             # and also create a list for the tags to then put into the list under one value: 'tags'
#             link_dict = dict()
#             tag_list = list()
#
#             # simply navigating through the html
#             link = links.a['href']
#             link_name = links.a.img['alt']
#             author = links.div.span.text
#             author = author[author.index(':') + len(': '):]
#             manga_id = ''
#             manga_site = ''
#
#             # Since mangakakalot makes their manga search results have links that apply either the mangakakalot site
#             # or the manganato site, separate processes were created to extract certain elements(such as tags) as
#             # the html templates were constructed differently
#             if 'manganato' in link:
#                 try:
#                     link_url = requests.get(link)
#                     soup2 = BeautifulSoup(link_url.text, "lxml")
#                     manga_id = link[link.index('manga-') + len('manga-'):]
#                     manga_site = 'manganato'
#                     tags = soup2.body.find(class_='body-site').find(class_='container-main') \
#                         .find(class_='container-main-left').find(class_='panel-story-info') \
#                         .tbody.contents[7].contents[3].find_all('a')
#                     for tag in tags:
#                         tag_list.append(tag.text)
#                 except IndexError:
#                     continue
#                 except ValueError:
#                     continue
#             elif 'mangakakalot' in link:
#                 try:
#                     link_url = requests.get(link)
#                     soup2 = BeautifulSoup(link_url.text, "lxml")
#                     manga_id = link[link.index('manga/') + len('manga/'):]
#                     manga_site = 'mangakakalot'
#                     tags = soup2.body.contents[3].find(class_='leftCol').ul.contents[13].find_all('a')
#                     for tag in tags:
#                         tag_list.append(tag.text)
#                 except IndexError:
#                     continue
#                 except ValueError:
#                     continue
#             # manga_id = links[links.index('')]
#             # putting extracted html elements into dictionary keys
#             link_dict["site"] = manga_site
#             link_dict["id"] = manga_id
#             link_dict["name"] = link_name
#             link_dict["author"] = author
#             link_dict["link"] = link
#             link_dict["tags"] = tag_list
#             link_list.append(link_dict)
#         except ValueError:
#             continue
#
#     for di in link_list:
#         json_object = json.dumps(di, indent=4)
#         print(json_object)
#
#
# if __name__ == "__main__":
#     mangakakalot_manga_search_webscraper()
# --- THIS CODE IS ONLY USED TO HELP PUT THE IDEA OF THE FUNCTIONS INTO SOMETHING TANGIBLE --- #

def grab_chap_info(manga_id):
    manga_info_dict = dict()
    author_s = list()
    tags = list()

    # request from url with id input
    base_url = "https://chapmanganato.com/manga-"
    link_url = base_url + manga_id
    link = requests.get(link_url)
    soup = BeautifulSoup(link.text, "lxml")

    # traverse through scraped html and add scraped info into the corresponding lists
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

    # add all scraped info into dictionary and turn into json
    manga_info_dict["Name"] = name
    manga_info_dict["Author/s"] = author_s
    manga_info_dict["Status"] = status
    manga_info_dict["Tag/s"] = tags
    manga_json = json.dumps(manga_info_dict)
    return manga_json


def search_scraper(user_search):
    base_url = "https://mangakakalot.com/search/story/"

    # list to hold info for the links
    link_list = list()

    # request from url to scrape the html to grab links and corresponding info
    r = requests.get(base_url + user_search.replace(" ", "_"))
    soup = BeautifulSoup(r.text, 'lxml')
    body = soup.body
    links = body.find_all(class_="story_item")

    # limit the search results to 8 because in reality, the user really only looks at the
    # top results, usually the top 8
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

# TODO: And then put them into a dictionary, to then transform it into JSON to send to the frontend
# TODO: Find way to customize transformed JSON to include whether the user has saved that manga into their favorites

# FUTURETODO: Learn to create a database for the user's saved searches/manga
