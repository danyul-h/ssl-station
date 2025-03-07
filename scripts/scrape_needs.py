import json
from bs4 import BeautifulSoup
import requests
import urllib.parse
import concurrent.futures
from itertools import repeat, chain
import re
import time

def clean_text(text):
    cleaned_text = text.replace("\u00a0", " ").replace("\t", " ").replace("\r", "").replace("\n", " ").replace("\xa0", " ").replace("\u2019", "'").replace('\"', '"').strip()
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text

#function to use with multi-threading later, fetching multiple pages simulatenously and processing with beautiful soup in parallel
def fetch_page(session, url):
    html = session.get(url).text
    cleaned_html = re.sub(r'<script.*?</script>', '', html)
    cleaned_html = re.sub(r'<! - .*? →', '', cleaned_html)
    return BeautifulSoup(html, "lxml")

#create the urls of all id lists based off the main page
def generate_list_urls(session, url, params):
    soup = fetch_page(session, f"{url}/?{urllib.parse.urlencode(params)}") #fetch main page
    last_index = int(soup.find("li", class_="last next").find("a").get("href").split("/")[3]) #parse main page to find last index
    count_per_page = 12 #num ids per page
    urls = [f"{url}{i}/?{urllib.parse.urlencode(params)}" for i in range(last_index+1) if i % count_per_page == 0] #create list of urls
    return urls

#parse a list of needs to get need urls
def parse_list(soup):
    ids = [i.get("href") for i in soup.find_all("a", class_="card-body")] #parse list to find all need urls
    return ids

#fetch all need urls from a collection of urls of need lists
def generate_need_urls(session, urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        soups = executor.map(fetch_page, repeat(session), urls)
        id_groups = executor.map(parse_list, soups)
        ids = list(chain(*id_groups))
    return ids

def parse_opportunity(soup, id):
    title = soup.find("h1", class_="panel-title").get_text()
    
    remaining_element = soup.find("div", class_="spots-remaining")
    remaining = remaining_element.find(string=True, recursive=False) if remaining_element else ""

    date_element = soup.find("td", class_="info-block date")
    date = date_element.find("div", class_="info").get_text().replace("Get Connected Icon", "").title() if date_element else ""

    time_element = soup.find("td", class_="info-block time")
    time = time_element.find("div", class_="info").get_text() if time_element else ""

    description = []
    description_element = soup.find("div", class_="section-content jodit-content")
    for child in description_element.children:
        description.append(child.get_text())

    location_element = soup.find("tr", class_="address")
    location = location_element.find("td", class_="text").get_text() if location_element else ""

    organization_element = soup.find("div", class_="agency")
    organization = organization_element.find("div", class_="title").get_text() if organization_element else ""

    interests = []
    interests_element = soup.find("ul", class_="interests-list")
    if interests_element:
        for li in interests_element.find_all("li"):
            interests.append(li.find("svg").get("title"))

    requirements = []
    requirements_element = soup.find("section", class_="requirements")
    if requirements_element:
        for td in requirements_element.find_all("td", class_="text"):
            requirements.append(td.get_text())

    shifts = []
    shifts_element = soup.find("table", id="shifts-table")
    if shifts_element:
        for tr in shifts_element.find_all("tr"):
            shift = {}
            for i in range(len(tr.find_all("td"))):
                text = tr.find_all("td")[i].get_text()
                match i:
                    case 0:
                        text = text.split("@")
                        shift["date"] = text[0]
                        text = text[1].split("to")
                        shift["start_time"] = text[0]
                        shift["end_time"] = text[1]
                    case 1:
                        text = text.split("hours")
                        shift["duration"] = text[0]
                    case 2:
                        text = text.split("of")
                        shift["vacant_spots"] = text[0]
                        shift["total_spots"] = text[1]
            shifts.append(shift)

    json = {
        "id" : id,
        "title" : title, #h1.panel-title.get_text()
        "remaining_spots" : remaining, #may not exist, div.spots-remaining .get_text()
        "date" : date, # td,info-block date -> div.info .get_text()
        "time" : time, # td.info-block time -> div.info .get_text()
        # "description" : " ".join(description), #append all p.get_text() in div.section-content jodit-content
        "description" : description,
        "shifts" : shifts,
        "location" : location, #tr.address -> td.text .get_text()
        "organization" : organization, #div.agency -> div.title .get_text()
        "interests" : interests, #svg.icon interest-icon 044e89 . get (data-original-title)
        "requirements" : requirements, # section.requirements -> td.text . get_text()
    }
    for i in json:
        if not isinstance(json[i], list):
            json[i] = clean_text(json[i])
            continue
        temp_list = []
        for j in json[i]:
            if j and isinstance(j, dict):
                for k in j:
                    j[k] = clean_text(j[k])
                temp_list.append(j)
            elif j and clean_text(j): temp_list.append(clean_text(j))
            json[i] = temp_list
    return json

#fetch all opportunities from a collection of urls (based off of opportunity id)
def fetch_opportunities(session, urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        soups = executor.map(fetch_page, repeat(session), urls)
        opportunities = executor.map(parse_opportunity, soups, [url.split("need_id=")[1] for url in urls])
    return list(opportunities)

session = requests.Session() #using a session object for optimization; prevents establishing a new connection every call

request_headers = { #request headers, provide information about the request context for the requested server
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' #user-agent indentifies app, os, vendor, version, makes scraper look like a person
}
session.headers = request_headers

url = 'https://montgomerycountymd.galaxydigital.com/need/index/' #moco website with opportunities

params = {
    "need_init_id" : "144"
}

# opportunities = fetch_opportunities(session, generate_need_urls(session, generate_list_urls(session, url, params)))
# opportunities = fetch_opportunities(session, generate_need_urls(session, ["https://montgomerycountymd.galaxydigital.com/need/index/144/?need_init_id=144"]))
opportunities = fetch_opportunities(session, ["https://montgomerycountymd.galaxydigital.com/need/detail/?need_id=1061622", "https://montgomerycountymd.galaxydigital.com/need/detail/?need_id=1030293", "https://montgomerycountymd.galaxydigital.com/need/detail/?need_id=911309", "https://montgomerycountymd.galaxydigital.com/need/detail/?need_id=1026190"])

for i in opportunities:
    print(json.dumps(i, indent=4))

# filename = "scraped.json"
# with open(filename, "w") as file:
#     json.dump(opportunities, file, indent=4)