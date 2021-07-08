from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

href_list, title_list, summary_list = [], [], []
ectimes = requests.get("https://economictimes.indiatimes.com/news/economy/agriculture")
ec_soup = BeautifulSoup(ectimes.content, 'html.parser')
ec_stories = ec_soup.find_all("div", {"class": "eachStory"})
for story in ec_stories:
    title = story.h3.a
    href_list.append('https://economictimes.indiatimes.com' + title['href'])
    title_list.append(title.text)
    summary_list.append(story.text)
range = range(len(href_list))

def index(req):
    return render(req, 'news/index.html', {'href_list': href_list, 'title_list': title_list, 'summary_list': summary_list, 'range': range})