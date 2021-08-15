import requests
from news.models import Article
from bs4 import BeautifulSoup

href_list, title_list, summary_list ,image_list = [], [], [], []
ectimes = requests.get("https://economictimes.indiatimes.com/news/economy/agriculture")
ec_soup = BeautifulSoup(ectimes.content, 'html.parser')
ec_stories = ec_soup.find_all("div", {"class": "eachStory"})
count=0
allArticles = Article.objects.all()
for story in ec_stories:
    if(count==0):
        count=1
    title = story.h3.a
    image = story.a.span.img
    href_list.append('https://economictimes.indiatimes.com' + title['href'])
    title_list.append(title.text)
    summary_list.append(story.text)
    image_list.append(image['data-original'])
    try:
        obj = Article.objects.get(url='https://economictimes.indiatimes.com' + title['href'])
    except Article.DoesNotExist:
        obj = Article(title = title.text, summary = story.text)
        obj.save()
