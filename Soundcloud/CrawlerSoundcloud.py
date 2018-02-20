# Felix Marsault CBD1
# TP Scrapping

import json
import csv
import requests


def json_request(url):
    """ Scrapper return the html page"""
    rq = requests.get(url)
    print(rq.status_code)  # 200 : ok , 500 : erreur serveur interne, 403 : pb permission, 404
    # print(rq.headers)

    req_json = json.loads(rq.text)

    return req_json


def write_json(data_dict):
    """Write the whole resulting data dictionary in a Json file."""
    with open('scraped_data/followers_cigarettesaftersex.json', 'w+') as outfile:
        json.dump(data_dict, outfile)


def init_csv(filename):
    """Initialize the csv file"""
    file = filename + '.csv'
    with open('scraped_data/' + file, 'w+') as file:
        writer = csv.writer(file)
        # Write a header if the file is empty
        writer.writerow('Username')


def write_csv(filename, data_list):
    """Write data list in a csv file."""
    file = filename + '.csv'
    with open('scraped_data/' + file, 'a') as file:
        writer = csv.writer(file)
        for follower in data_list:
            writer.writerow(follower)


page_url = "https://soudcloud.com/cigarettesaftersex/followers"

# First GET request found arriving on the page_url
base_url = "https://api-v2.soundcloud.com/users/19710656/followers?limit=200&offset=0"

param_url = "&client_id=iIj5dLn8zOk9MleA8FuQTe3bgdNTLG4s&linked_partitioning=1&app_version=1518689071&app_locale=en"
url = base_url + param_url

filename = 'followers_name'
init_csv(filename)

c = 0
dict_followers = {}

while True:

    req_json = json_request(url)
    # time.sleep(0.5)

    list_followers_name = []
    for idx, follower in enumerate(req_json['collection']):
        list_followers_name.append(req_json['collection'][idx]['username'])
        dict_followers[idx + c] = req_json['collection'][idx]

    c += 200
    write_csv(filename, list_followers_name)
    next_href = req_json['next_href']
    try:
        url = next_href + param_url
    except TypeError:
        break


write_json(dict_followers)




# https://api-v2.soundcloud.com/users/121682411/followers?client_id=iIj5dLn8zOk9MleA8FuQTe3bgdNTLG4s&limit=12&offset=0&linked_partitioning=1&app_version=1518689071&app_locale=en