import requests
from bs4 import BeautifulSoup


def news(message, bot):
    url = "https://baomoi.com/tin-moi.epi"
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, "html.parser")
    data = soup.findAll("h3", class_="font-semibold block")
    title = [title.find("a").attrs["title"] for title in data]
    link = [link.find("a").attrs["href"] for link in data]

    print(data)

    item = ""
    for i in range(0, 10):
        item += f"{i + 1}: " + title[i] + "\nLink: https://baomoi.com" + link[i] + "\n--------------------------------\n"
    print(message)
    bot.send_message(message.chat.id, text=item)
