from django.db import models
from django.urls import reverse
from streamerboard.users.models import User

# Create your models here.

class StreamPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=300, blank=True)
    upvotes = models.ManyToManyField(User, blank=True, related_name='upvotes')
    downvotes = models.ManyToManyField(User, blank=True, related_name='downvotes')
    # Time is a rhinocerous
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " " + self.title

    def get_absolute_url(self):
        return reverse("streams:detail", kwargs={"pk": self.pk})

    def get_upvote_url(self, request):
        return reverse("streams:upvote-toggle", kwargs={'pk': self.pk})

    def get_downvote_url(self, request):
        return reverse("streams:downvote-toggle", kwargs={'pk': self.pk})

    def get_api_upvote_url(self):
        return reverse("streams:upvote-api-toggle", kwargs={'pk': self.pk})

    def get_api_downvote_url(self):
        return reverse("streams:downvote-api-toggle", kwargs={'pk': self.pk})
