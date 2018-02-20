
import re
import time
import json
import csv
from bs4 import BeautifulSoup
import requests

HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36'}

# PROXY = {"https": "https//59.110.7.190:1080"}

url = "https://soudcloud.com/cigarettesaftersex/followers"
# url = "https://api-v2.soundcloud.com/users/19710656/followers?client_id=iIj5dLn8zOk9MleA8FuQTe3bgdNTLG4s&limit=12&offset=0&linked_partitioning=1&app_version=1518689071&app_locale=en"

page = requests.get(url,  headers=HEADER)
print(page.status_code)  # 200 : ok , 500 : erreur serveur interne, 403 : pb permission, 404
print(page.text)
print(page.headers)



# page_url = ["https://soudcloud.com/cigarettesaftersex/followers"]

# First GET request found arriving on the page_url
# req_url = "https://api-v2.soundcloud.com/users/19710656/followers?client_id=iIj5dLn8zOk9MleA8FuQTe3bgdNTLG4s&limit=12&offset=0&linked_partitioning=1&app_version=1518689071&app_locale=en"


# followers = followers_list(soup)

# print(followers)
