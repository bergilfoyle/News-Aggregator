from django.views import generic
from news.models import Source, Article, Saved
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomUserCreationForm
import requests
from bs4 import BeautifulSoup

href_list, title_list, summary_list, image_list = [], [], [], []
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

range = range(len(href_list))

context = {'href_list': href_list, 'title_list': title_list, 'summary_list': summary_list, 'range': range, 'image_list': image_list}

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
    if(source == "userindex"):
        return redirect('index')
    else:
        return redirect('saved')

class ArticleListView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'news/userindex.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        obj, created = Saved.objects.get_or_create(
            current_user=self.request.user)
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
