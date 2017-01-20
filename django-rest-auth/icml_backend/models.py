from __future__ import unicode_literals

from django.contrib.auth import models as auth_models
from django.db import models

def _high_level_json(item):
    return {'id' : item.id}

# Create your models here.

class Topic(models.Model):
    code = models.CharField(max_length = 20, primary_key = True)
    name = models.CharField(max_length = 100, null = True)

    def jsonize(self, detailed = True):
        return {
            'code' : self.code,
            'name' : self.name
        }

    def __unicode__(self):
        return self.code

class Author(models.Model):
    full_name = models.CharField(max_length = 300)
    university = models.CharField(max_length = 300)

    def jsonize(self, detailed = True):
        output = _high_level_json(self)
        if not detailed:
            return output

        output.update({
            'full_name' : self.full_name,
            'university' : self.university
        })

        return output

    def __unicode__(self):
        return self.full_name

class Paper(models.Model):
    title = models.CharField(max_length = 400)
    authors = models.ManyToManyField(Author)

    #Commma separated list of author ids
    ordered_authors = models.TextField(null = False, default = "")

    topics = models.ManyToManyField(Topic, related_name = 'paper_topics')
    abstract = models.TextField()

    def jsonize(self, detailed = True):
        output = _high_level_json(self)
        if not detailed:
            return output

        output.update({
            'title' : self.title,
            'topics' : [topic.jsonize() for topic in self.topics.all()],
            'authors' : [author.jsonize() for author in self.authors.all()],
            'abstract' : self.abstract
        })

        return output

    def __unicode__(self):
        return self.title

class Session(models.Model):
    start_time = models.DateTimeField()
    location = models.CharField(max_length = 200)

class SessionPaper(models.Model):
    """
        Paper with index to indcate some ordering.
    """
    session = models.ForeignKey(Session)
    paper = models.ForeignKey(Paper)
    index = models.IntegerField()
    time = models.DateTimeField()

class Comment(models.Model):
    """
        Public comments on a particular paper
    """
    paper = models.ForeignKey(Paper)
    user = models.ForeignKey(auth_models.User)

    text = models.TextField()
    time = models.DateTimeField(auto_now_add = True)

    def jsonize(self, detailed = True):
        output = _high_level_json(self)
        if not detailed:
            return output

        output.update({
            'paper' : self.paper.jsonize(),
            'user' : self.user.get_username(),
            'text' : self.text,
            'time' : self.time # Default ISO format
        })

        return output

class Like(models.Model):
    """
        User like for a particular paper
    """
    paper = models.ForeignKey(Paper)
    user = models.ForeignKey(auth_models.User)
    time = models.DateTimeField(auto_now_add = True)

    def jsonize(self, detailed = True):
        output = _high_level_json(self)
        if not detailed:
            return output

        output.update({
            'paper' : self.paper.jsonize(),
            'user' : self.user.get_username(),
            'time' : self.time # Default ISO format
        })

        return output