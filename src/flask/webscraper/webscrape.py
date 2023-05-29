from bs4 import BeautifulSoup
import requests
import json


# TODO: implement a way so that the script scrapes from several websites
def manga_webscraper():
    base_url = "https://mangakakalot.com/search/story/"

    # FUTURETODO: Find a way to implement a frontend that takes input from the user
    # and then sends that input into this script (or a future backend)
    # userSearch = input()

    user_search = 'kaguya sama'

    # list of the search results with their respective data (title, author, link to manga, tags, and id)
    link_list = list()

    # simply using the request library to send a request to the url in order to start extracting data
    # with beautifulsoup
    r = requests.get(base_url + user_search.replace(" ", "_"))
    soup = BeautifulSoup(r.text, 'html.parser')
    print("Grabbing from " + base_url + user_search.replace(" ", "_"))
    body = soup.body
    links_in_body = body.find_all(class_="story_item")

    for links in links_in_body:
        # print(links.a.prettify())
        # print(links.a.img.prettify())

        # create a dictionary to put the extracted data into
        # and also create a list for the tags to then put into the list under one value: 'tags'
        link_dict = dict()
        tag_list = list()

        # simply navigating through the html
        link = links.a['href']
        link_name = links.a.img['alt']
        author = links.div.span.text
        author = author[author.index(':') + len(': '):]
        manga_id = ''
        manga_site = ''

        # Since mangakakalot makes their manga search results have links that apply to either the mangakakalot site
        # or the manganato site, separate processes were created to extract certain elements(such as tags) as
        # the html templates were constructed differently
        if 'manganato' in link:
            manga_id = link[link.index('manga-') + len('manga-'):]
            manga_site = 'manganato'
            link_url = requests.get(link)
            print(f"Grabbing from {link}")
            soup2 = BeautifulSoup(link_url.text, "html.parser")
            tags = soup2.body.find(class_='body-site').find(class_='container-main').find(class_='container-main-left') \
                .find(class_='panel-story-info').tbody.contents[7].contents[3].find_all('a')
            for tag in tags:
                tag_list.append(tag.text)
        elif 'mangakakalot' in link:
            manga_id = link[link.index('manga/') + len('manga/'):]
            manga_site = 'mangakakalot'
        # manga_id = links[links.index('')]
        # putting extracted html elements into dictionary keys
        link_dict["site"] = manga_site
        link_dict["id"] = manga_id
        link_dict["name"] = link_name
        link_dict["author"] = author
        link_dict["link"] = link
        link_dict["tags"] = tag_list
        link_list.append(link_dict)

    for di in link_list:
        json_object = json.dumps(di, indent=4)
        print(json_object)


if __name__ == "__main__":
    manga_webscraper()

# TODO: Put the title, link, and other info (author, num of chapters) into variables
# TODO: And then put them into a dictionary, to then transform it into JSON to send to the frontend
# TODO: Find way to customize transformed JSON to include whether the user has saved that manga into their favorites

# FUTURETODO: Learn to create a database for the user's saved searches/manga
