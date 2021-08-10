from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

href_list, title_list, summary_list ,image_list = [], [], [], []
ectimes = requests.get("https://economictimes.indiatimes.com/news/economy/agriculture")
ec_soup = BeautifulSoup(ectimes.content, 'html.parser')
ec_stories = ec_soup.find_all("div", {"class": "eachStory"})
count=0
for story in ec_stories:
    if(count==0):
        print(story)
        count=1
    title = story.h3.a
    image = story.a.span.img
    href_list.append('https://economictimes.indiatimes.com' + title['href'])
    title_list.append(title.text)
    summary_list.append(story.text)
    image_list.append(image['data-original'])
    
range = range(len(href_list))

context = {'href_list': href_list, 'title_list': title_list, 'summary_list': summary_list, 'range': range}

def index(req):
    return render(req, 'news/index.html', context)
