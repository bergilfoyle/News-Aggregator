from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse
from django.contrib.auth import authenticate, login
from news.models import Source, Article, Saved, Topic, UserSource
import news.scrapers as scrapers
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomUserCreationForm, UserDetailsForm, SourcesForm

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
            user, created = User.objects.get_or_create(username = request.POST.get('username'))
            UserSource.setinitialsources(current_user = user)
            return redirect('register')
    else:
        f = CustomUserCreationForm()

    return render(request, 'news/register.html', {'form': f})

def userdetails(request):
    initialvalues = {'username': request.user.username, 'email': request.user.email}
    if request.method == 'POST':
        if request.POST.get('changedetails'):
            f = UserDetailsForm(request.POST, initialvalues, user=request.user)
            if f.is_valid():
                f.save()
                messages.success(request, 'Details Changed Successfully')
                return redirect('userdetails')
            else:
                sourcesform = SourcesForm()
                obj, created = UserSource.objects.get_or_create(current_user = request.user)
                initial = [i.pk for i in obj.sources.all()]
                sourcesform.fields['sources'].initial = initial
    
        elif request.POST.get('changesources'):
            checked = request.POST.getlist('sources')
            sourcesform = SourcesForm(request.POST, checked = checked, user=request.user)
            obj, created = UserSource.objects.get_or_create(current_user = request.user)
            initial = [i.pk for i in obj.sources.all()]
            sourcesform.fields['sources'].initial = initial
            if sourcesform.is_valid():
                sourcesform.save()
                messages.success(request, 'Details Changed Successfully')
                return redirect('userdetails')
    else:
        f = UserDetailsForm(initialvalues, user=request.user)
        sourcesform = SourcesForm()
        obj, created = UserSource.objects.get_or_create(current_user = request.user)
        initial = [i.pk for i in obj.sources.all()]
        sourcesform.fields['sources'].initial = initial
    
    return render(request, 'news/userdetails.html', {'form': f, 'sourcesform': sourcesform})


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
        usersource, created = UserSource.objects.get_or_create(current_user = self.request.user)
        context['article_list'] = topic.article_set.filter(source__in = usersource.sources.all()).order_by('published').reverse()
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

