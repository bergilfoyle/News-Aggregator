from news.models import Article, Source, Topic
from bs4 import BeautifulSoup
import requests

class LiveNewsScraper:
    @classmethod
    def scrape(cls):
        href_list, title_list, summary_list, image_list = [], [], [], []
        topicobject, created = Topic.objects.get_or_create(name='News')
        ectimes = requests.get("https://economictimes.indiatimes.com/news/economy/agriculture")
        ec_soup = BeautifulSoup(ectimes.content, 'html.parser')
        ec_stories = ec_soup.find_all("div", {"class": "eachStory"})

        source = 'https://economictimes.indiatimes.com'
        sourceobject, created = Source.objects.get_or_create(url=source)
        sourceobject.name = 'Economic Times'
        sourceobject.save()

        for story in ec_stories:
            titletag = story.h3.a
            image = story.a.span.img
            url = source + titletag['href']
            imageurl = image['data-original']

            title_list.append(titletag.text)
            summary_list.append(story.text)
            href_list.append(url)
            image_list.append(imageurl)

            obj, created = Article.objects.get_or_create(url = url)
            obj.title = titletag.text
            obj.source = sourceobject
            obj.summary = story.text
            obj.imageurl = imageurl
            obj.save()
            topicobject.article_set.add(obj)

        r = range(len(href_list))
        context = {'href_list': href_list, 'title_list': title_list, 'summary_list': summary_list, 'range': r, 'image_list': image_list}
        return r, context