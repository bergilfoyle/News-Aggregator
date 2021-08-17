from django.views import generic
from django.urls import reverse
from news.models import Source, Article, Saved, Topic
import news.scrapers as scrapers
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomUserCreationForm

scrapers.scrapeworldnews()
r, context = scrapers.scrapenews()

def index(req):
    return render(req, 'news/index.html', context)

def about(req):
    return render(req, 'news/about.html', context)

def contact(req):
    return render(req, 'news/contact.html', context)

def userdetails(req):
    return render(req, 'news/userdetails.html', context)

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
    else:
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
        context['article_list'] = topic.article_set.order_by('published').reverse()
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

