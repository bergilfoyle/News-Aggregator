from django.db import models
from django.contrib.auth.models import User

class Source(models.Model):
    name = models.CharField(max_length=200, default='_')
    url = models.CharField(max_length=200, default='_')
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=200, help_text='Enter the topic')
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, default = '_')
    published = models.DateTimeField(null=True)
    url = models.CharField(max_length=200, default = '_')
    imageurl = models.CharField(max_length=200, default='_')
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=200, default='_', help_text='Enter the summary')
    topic = models.ManyToManyField(Topic, help_text='Enter the news topic')

    def __str__(self):
        return self.title

class Saved(models.Model):
    articles = models.ManyToManyField(Article)
    current_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='owner', null=True)

    @classmethod
    def addtosaved(cls, current_user, article):
        obj, created = cls.objects.get_or_create(current_user = current_user)
        obj.articles.add(article)
    
    @classmethod
    def removefromsaved(cls, current_user, article):
        obj, created = cls.objects.get_or_create(current_user = current_user)
        obj.articles.remove(article)

class UserSource(models.Model):
    sources = models.ManyToManyField(Source)
    current_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sourceowner', null=True)

    @classmethod
    def setinitialsources(cls, current_user):
        obj, created = cls.objects.get_or_create(current_user = current_user)
        obj.sources.set(Source.objects.all())
        obj.save()
    @classmethod
    def updatesources(cls, current_user, checked):
        obj, created = cls.objects.get_or_create(current_user = current_user)
        obj.sources.clear()
        obj.save()
        obj.sources.add(*checked)
        return obj



