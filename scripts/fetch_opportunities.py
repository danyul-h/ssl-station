import json
from bs4 import BeautifulSoup
import requests

target_website = 'https://montgomerycountymd.galaxydigital.com/need/index?age=&agency_id=&distance=&zip=&need_impact_area=&need_init_id=144&cat_id=&allowTeams=&s=1'

request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Initiate HTTP request
html = requests.get(target_website, headers=request_headers).text
soup = BeautifulSoup(html, features="html.parser")

for need in soup.find_all("a", class_="card-body"):
    print(need.get("href"))