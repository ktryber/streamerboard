from django.db import models
from streamerboard.users.models import User
# Create your models here.

class StreamPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=300, blank=True)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    # Time is a rhinocerous
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.text+' - '+self.author.username
