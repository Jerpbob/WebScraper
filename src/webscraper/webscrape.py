from bs4 import BeautifulSoup
import requests

#TODO: implement a way so that the script scrapes from several websites
baseUrl = "https://mangakakalot.com/search/story/"

#FUTURETODO: Find a way to implement a frontend that takes input from the user
#and then sends that input into this script (or a future backend)
# userSearch = input()

userSearch = 'kaguya sama'
link_list = list()
r = requests.get(baseUrl + userSearch.replace(" ", "_"))
soup = BeautifulSoup(r.text, 'html.parser')
print("Grabbing from " + baseUrl + userSearch.replace(" ", "_"))
# head = soup.head
# title = soup.title
body = soup.body

links_in_body = body.find_all(class_="story_item")


for links in links_in_body:
    #print(links.a.prettify())
    # print(links.a.img.prettify())
    link_dict = {}
    link = links.a['href']
    link_name = links.a.img['alt']
    author = links.div.span.text
    author = author[author.index(':') + len(': '):]
    manga_id = ''
    manga_site = ''
    if 'manganato' in link:
        manga_id = link[link.index('manga-') + len('manga-'):]
        manga_site = 'manganato'
    elif 'mangakakalot' in link:
        manga_id = link[link.index('manga/') + len('manga/'):]
        manga_site = 'mangakakalot'
    # manga_id = links[links.index('')]
    link_dict["site"] = manga_site
    link_dict["id"] = manga_id
    link_dict["name"] = link_name
    link_dict["author"] = author
    link_dict["link"] = link
    link_list.append(link_dict)

for di in link_list:
    for data in di:
        print(f"{data} : {di[data]}")
    print()


#TODO: Put the title, link, and other info (author, num of chapters) into variables
#TODO: And then put them into a dictionary, to then transform it into JSON to send to the frontend
#TODO: Find a way to customize that transformed JSON to also include whether the user has saved that manga into their favorites

#FUTURETODO: Learn to create a database for the user's saved searches/manga