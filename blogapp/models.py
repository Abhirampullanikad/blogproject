from django.db import models
from django.conf import settings  # Add this import at the top
from datetime import datetime

now = datetime.now()
time = now.strftime("%d %B %Y")

class Post(models.Model):
    postname = models.CharField(max_length=600)
    category = models.CharField(max_length=600)
    image = models.ImageField(upload_to='img/posts', blank=True, null=True)
    content = models.CharField(max_length=100000)
    time = models.CharField(default=time, max_length=100, blank=True)
    likes = models.IntegerField(null=True, blank=True, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.postname)

class Comment(models.Model):
    content = models.CharField(max_length=200)
    time = models.CharField(default=time, max_length=100, blank=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id}.{self.content[:20]}..."

class News(models.Model):
    title=models.CharField(max_length=200,null=True)
    type_of_news=models.CharField(max_length=200)
    description = models.CharField(max_length = 500, default=None)
    date=models.IntegerField(null=True)
    time=models.CharField(default=time,max_length=100000)
    image=models.ImageField(upload_to='img/news')

    def __str__(self):
        return self.title
    