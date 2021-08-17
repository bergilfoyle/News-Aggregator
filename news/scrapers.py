from news.models import Article, Source, Topic
from django.utils.timezone import make_aware
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def scrapenews():
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
        date = story.time.text
        image = story.a.span.img
        title = titletag.text
        url = source + titletag['href']
        imageurl = image['data-original']
        title_list.append(titletag.text)
        summary_list.append(story.text)
        href_list.append(url)
        image_list.append(imageurl)
        obj, created = Article.objects.get_or_create(title = title)
        obj.title = title
        obj.published = make_aware(datetime.strptime(date[:-4], '%b %d, %Y, %I:%M %p'))
        obj.url = url
        obj.source = sourceobject
        obj.summary = story.text
        obj.imageurl = imageurl
        obj.save()
        topicobject.article_set.add(obj)

    source = "https://timesofindia.indiatimes.com"
    sourceobject, created = Source.objects.get_or_create(url=source)
    sourceobject.name = 'Times of India'
    sourceobject.save()

    topicobject, created = Topic.objects.get_or_create(name='News')
    toi = requests.get("https://timesofindia.indiatimes.com/topic/Agriculture/news")
    toi_soup = BeautifulSoup(toi.content, 'html.parser')
    toi_section= toi_soup.find_all("li", {"class": "article"})
    for article in toi_section:
        titletag = article.div.a
        url = source + titletag['href']
        title = titletag.span.text.strip()
        date = titletag.span.next_sibling.next_sibling.text
        summary = titletag.p.text.strip()
        try:
            imagepage = requests.get(url)
            image_soup = BeautifulSoup(imagepage.content, 'html.parser')
            image_section= image_soup.find("div", {"class": "_3gupn"})
            imageurl = image_section.img['src']
        except:
            imageurl = ''
        #imageurl = ''
        obj, created = Article.objects.get_or_create(title = title)
        obj.title = title
        obj.url = url
        obj.published = make_aware(datetime.strptime(date, '%d %b %Y, %H:%M'))
        obj.source = sourceobject
        obj.summary = summary
        obj.imageurl = imageurl
        obj.save()
        if imageurl != '':
            topicobject.article_set.add(obj)

    r = range(len(href_list))
    context = {'href_list': href_list, 'title_list': title_list, 'summary_list': summary_list, 'range': r, 'image_list': image_list}
    return r, context

def scrapeworldnews():
    source = "https://www.reuters.com"
    sourceobject, created = Source.objects.get_or_create(url=source)
    sourceobject.name = 'Reuters'
    sourceobject.save()

    topicobject, created = Topic.objects.get_or_create(name='World')
    reu = requests.get("https://www.reuters.com/news/archive/agriculture-news")
    reu_soup = BeautifulSoup(reu.content, 'html.parser')
    reu_section= reu_soup.find("section", {"class": "module-content"})
    reu_section = reu_section.div
    for story in reu_section.find_all("article"):
        content = story.find("div", {"class": "story-content"})
        photo = story.find("div", {"class": "story-photo"})
        title = content.a.h3.text.strip()
        url = source + content.a['href']
        summary = content.p.text
        try:
            imageurl = photo.a.img['org-src']
        except:
            imageurl = "data:image/png;base64,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"

        obj, created = Article.objects.get_or_create(title = title)
        obj.title = title
        obj.url = url
        obj.source = sourceobject
        obj.summary = summary
        obj.imageurl = imageurl
        obj.save()
        topicobject.article_set.add(obj)