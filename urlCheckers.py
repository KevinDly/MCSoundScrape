#Builds the minecraft wiki url for the given mob name.
from bs4 import BeautifulSoup
import requests, re

def buildURL(name):
    return "https://minecraft.fandom.com/wiki/Special:Search?query={query}".replace("{query}", name)


#Returns false if the url is not a valid page, returns true otherwise.
def checkURL(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    dne = soup.find("p", class_="mw-search-createlink")

    if dne is None:
        return True
    else:
        return False