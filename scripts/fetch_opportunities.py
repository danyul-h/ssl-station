import json
from bs4 import BeautifulSoup
import requests
import urllib.parse
from functools import lru_cache
import concurrent.futures
from itertools import repeat, chain
import re
import time

#caches the results of parsed data, avoids redundant parsing and speeds up repeated operations
@lru_cache(maxsize=100)
def parse_html(html):
    return BeautifulSoup(html, "lxml") #need to pip install lxml, should be more efficient than html parser

#function to use with multi-threading later, fetching multiple pages simulatenously and processing with beautiful soup in parallel
def fetch_page(url, session):
    start = time.time()
    html = session.get(url).text
    cleaned_html = re.sub(r'<script.*?</script>', '', html)
    cleaned_html = re.sub(r'<! - .*? →', '', cleaned_html)
    end = time.time()
    print(f"Time fetching {url}: {round(end-start,2)}")
    return parse_html(cleaned_html)

#create the urls of all id lists
def generate_list_urls(url, params, session):
    start = time.time()
    soup = fetch_page(f"{url}/?{urllib.parse.urlencode(params)}", session) #fetch main page
    last_index = int(soup.find("li", class_="last next").find("a").get("href").split("/")[3]) #parse main page to find last index
    count_per_page = 12 #num ids per page
    end = time.time()
    urls = [f"{url}{i}/?{urllib.parse.urlencode(params)}" for i in range(last_index+1) if i % count_per_page == 0] #create list of urls
    print(f"Time elapsed creating all list urls: {round(end-start, 2)}")
    print(f"Found {len(urls)} urls. \n")
    return urls

#parse an id list to get ids
def parse_list(soup):
    ids = [i.get("href") for i in soup.find_all("a", class_="card-body")] #parse list to find all url ids
    return ids

#fetch all ids from a collection of urls of id lists
def fetch_ids(urls, session):
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        soups = executor.map(fetch_page, urls, repeat(session))
        id_groups = executor.map(parse_list, soups)
        ids = list(chain(*id_groups))
    end = time.time()
    print(f"Time elapsed finding all ids: {round(end-start,2)}")
    print(f"Found {len(ids)} ids. \n")
    # print(ids)
    return ids

def parse_opportunity(soup):
    title = soup.find("h1", class_="panel-title").get_text()
    
    remaining_element = soup.find("div", class_="spots-remaining")
    remaining = remaining_element.get_text() if remaining_element else ""

    date_element = soup.find("td", class_="info-block date")
    date = date_element.find("div", class_="info").get_text() if date_element else ""

    time_element = soup.find("td", class_="info-block time")
    time = time_element.find("div", class_="info").get_text() if time_element else ""

    description = []
    for p in soup.find("div", class_="section-content jodit-content").find_all("p"):
        description.append(p.get_text())

    location_element = soup.find("tr", class_="address")
    location = location_element.find("td", class_="text").get_text() if location_element else "virtual"

    organization = soup.find("div", class_="agency").find("div", class_="title").get_text()

    interests = []
    for li in soup.find("ul", class_="interests-list").find_all("li"):
        interests.append(li.find("svg").get("title"))

    requirements = []
    for td in soup.find("section", class_="requirements").find_all("td", class_="text"):
        requirements.append(td.get_text())

    json = {
        "title" : title, #h1.panel-title.get_text()
        "remaining" : remaining, #may not exist, div.spots-remaining .get_text()
        "date" : date, # td,info-block date -> div.info .get_text()
        "time" : time, # td.info-block time -> div.info .get_text()
        "description" : description, #append all p.get_text() in div.section-content jodit-content
        "location" : location, #tr.address -> td.text .get_text()
        "organization" : organization, #div.agency -> div.title .get_text()
        "interests" : interests, #svg.icon interest-icon 044e89 . get (data-original-title)
        "requirements" : requirements, #
    }
    # for i in json:
    #     if isinstance(json[i], list):
    #         for j in json[i]:
    #             if j:
    #                 j = j.replace("\t", "").replace("\n", "").replace("\r", "").replace("  ", " ").strip()
    #     else: 
    #         json[i] = json[i].replace("\t", "").replace("\n", "").replace("\r", "").replace("\xa0", " ").replace("  ", " ").strip()
    return json

#fetch all opportunities from a collection of urls (based off of opportunity id)
def fetch_opportunities(urls, session):
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        soups = executor.map(fetch_page, urls, repeat(session))
        opportunities = executor.map(parse_opportunity, soups)
    end = time.time()
    print(f"Time elapssed fetching all opportunity data: {round(end-start, 2)}")
    return opportunities

#using a session object for optimization; prevents establishing a new connection every call
session = requests.Session()

#request headers, provide information about the request context for the requested server
request_headers = {
    #a user agent is a computer program representing a person, helps our bot scraper look like a person
    #user-agent indentifies app, os, vendor, version
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}
session.headers = request_headers

#moco website with opportunities
url = 'https://montgomerycountymd.galaxydigital.com/need/index/'

params = {
    "need_init_id" : "144"
}

# opportunities = fetch_opportunities(fetch_ids(generate_list_urls(url, params, session), session), session)
opportunities = fetch_opportunities(fetch_ids(["https://montgomerycountymd.galaxydigital.com/need/index/12/?need_init_id=144"], session), session)
for i in opportunities:
    print(json.dumps(i, indent=4))
#observations...
#parsing is way quicker than fetching a page, arguably no need to optimize it
#fetching the lists takes longer than the opportunites themselves (5-3 secs vs. 0-1 secs)