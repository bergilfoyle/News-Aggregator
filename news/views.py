from typing import overload
from django.views import generic
from django.urls import reverse
from news.models import Source, Article, Saved, Topic
from news.scrapers import LiveNewsScraper
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomUserCreationForm
import requests
from bs4 import BeautifulSoup

#World News

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
        imageurl = photo.a.img['src']

    obj, created = Article.objects.get_or_create(title = title)
    obj.title = title
    obj.url = url
    obj.source = sourceobject
    obj.summary = summary
    obj.imageurl = imageurl
    obj.save()

    topicobject.article_set.add(obj)
    print(url)

r, context = LiveNewsScraper.scrape()

def index(req):
    return render(req, 'news/index.html', context)

def about(req):
    return render(req, 'news/about.html', context)


def contact(req):
    return render(req, 'news/contact.html', context)

def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')
    else:
        f = CustomUserCreationForm()

    return render(request, 'news/register.html', {'form': f})

def changesaved(request, operation, pk, source):
    article = Article.objects.get(pk=pk)
    if operation == 'addtosaved':
        Saved.addtosaved(request.user, article)
    elif operation == 'removefromsaved':
        Saved.removefromsaved(request.user, article)
    if source == "userindex":
        return redirect('index')
    elif source == "saved":
        return redirect('saved')
    elif source == "world":
        return redirect(reverse('viewtopic', args=(source, )))


def viewtopic(request, topicname):
    context = {}
    context_object_name = '{}_list'.format(topicname)

    topic, created = Topic.objects.get_or_create(name='World')
    obj, created = Saved.objects.get_or_create(current_user=request.user)
    context[context_object_name] = topic.article_set.all()

    context['saved_list'] = obj.articles.all()
    template_name = 'topics/{}.html'.format(topicname)

    return render(request, template_name, context)


class ArticleListView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'news/userindex.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        topic, created = Topic.objects.get_or_create(name='News')
        context['article_list'] = topic.article_set.all()
        obj, created = Saved.objects.get_or_create(current_user=self.request.user)
        context['saved_list'] = obj.articles.all()
        return context

class SavedListView(generic.ListView):
    model = Saved
    context_object_name = 'saved_list'
    template_name = 'news/saved.html'

    def get_context_data(self, **kwargs):
        context = super(SavedListView, self).get_context_data(**kwargs)
        obj, created = Saved.objects.get_or_create(
            current_user=self.request.user)
        context['saved_list'] = obj.articles.all()
        return context
