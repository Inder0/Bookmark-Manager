import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    response=requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    soup=BeautifulSoup(response.content,"html.parser")
    title=soup.title.text if soup.title else ""
    description_tag=soup.find("meta",attrs={"name":"description"})
    description=description_tag['content'] if description_tag else ""
    favicon = f"https://www.google.com/s2/favicons?domain={url}"

    return {
        "title":title,
        "description":description,
        "favicon":favicon,
    }
