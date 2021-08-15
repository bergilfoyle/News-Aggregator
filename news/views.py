from django.views import generic
from django.http import HttpResponse
from news.models import Article, Saved
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomUserCreationForm
import requests
from bs4 import BeautifulSoup

href_list, title_list, summary_list, image_list = [], [], [], []
ectimes = requests.get(
    "https://economictimes.indiatimes.com/news/economy/agriculture")
ec_soup = BeautifulSoup(ectimes.content, 'html.parser')
ec_stories = ec_soup.find_all("div", {"class": "eachStory"})
count = 0
for story in ec_stories:
    if(count == 0):
        count = 1
    t = story.h3.a
    image = story.a.span.img
    href_list.append('https://economictimes.indiatimes.com' + t['href'])
    title_list.append(t.text)
    summary_list.append(story.text)
    image_list.append(image['data-original'])
    obj, created = Article.objects.get_or_create(
        url='https://economictimes.indiatimes.com'+t['href'])
    obj.title = t.text
    obj.summary = story.text
    obj.save()

range = range(len(href_list))

context = {'href_list': href_list, 'title_list': title_list,
           'summary_list': summary_list, 'range': range, 'image_list': image_list}

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

def changesaved(request, operation, pk):
    article = Article.objects.get(pk=pk)
    if operation=='addtosaved':
        Saved.addtosaved(request.user, article)
    elif operation=='removefromsaved':
        Saved.removefromsaved(request.user, article)
    return redirect('saved')

class ArticleListView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'news/userindex.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        obj, created = Saved.objects.get_or_create(current_user = self.request.user)
        context['saved_list'] = obj.articles.all()
        return context

class SavedListView(generic.ListView):
    model = Saved
    context_object_name = 'saved_list'
    template_name = 'news/saved.html'

    def get_context_data(self, **kwargs):
        context = super(SavedListView, self).get_context_data(**kwargs)
        obj, created = Saved.objects.get_or_create(current_user = self.request.user)
        context['saved_list'] = obj.articles.all()
        return context

