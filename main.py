from dotenv import dotenv_values
env_values = dotenv_values()

import requests
from bs4 import BeautifulSoup

import schedule
import time

def act_on_litter_status():
    page = requests.get("https://www.mijnafvalwijzer.nl/nl/4823ma/202/")
    soup = BeautifulSoup(page.text)

    def tag_check_generator(classValue):
        def tag_check(tag):
            return tag.has_attr("class") and classValue in tag["class"]

        return tag_check

    firstTag = soup.find(tag_check_generator("firstDate"))

    todaysLitter = None
    if firstTag.string == "Vandaag":
        firstLitter = soup.find(tag_check_generator("firstWasteType"))

        todaysLitter = firstLitter.string

    requests.post("https://api.telegram.org/bot" + env_values["TELEGRAM_TOKEN"] + "/sendMessage", json={
        "chat_id": env_values["TELEGRAM_CHAT_ID"],
        "text": todaysLitter
    })

schedule.every().day.at("01:00", "Europe/Amsterdam").do(act_on_litter_status)

while True:
    schedule.run_pending()
    time.sleep(1)