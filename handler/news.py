import requests
from bs4 import BeautifulSoup

group_id = -4019357479


def news(message, bot):
    url = "https://baomoi.com/tin-moi.epi"
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, "html.parser")
    data = soup.findAll("h3", class_="font-semibold block")
    title = [title.find("a").attrs["title"] for title in data]
    link = [link.find("a").attrs["href"] for link in data]

    item = ""
    for i in range(0, 10):
        item += f"{i + 1}: " + title[i] + "\nLink: https://baomoi.com" + link[i] + "\n--------------------------------\n"
    bot.send_message(group_id, text=item)
