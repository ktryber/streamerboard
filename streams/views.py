from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, UpdateView, CreateView,
                                DeleteView, FormView, View)
from decouple import config
import requests
import json
from . models import StreamPost
from . forms import StreamPostForm

from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def streams_list(request):
    context = {
        'all_posts': StreamPost.objects.reverse(),
        'form': StreamPostForm()
    }
    return render(request, 'streams/index.html', context)

def api_view(request):
    # https://api.twitch.tv/kraken/videos/top?game=CS:GO
    client_id = '5hfhab54l3d3vx38s59z5i6ek8z2vg'
    secret_key = '6hi3590o5xmv788a09thjxldrevbvx'
    redirect_uri = 'http://127.0.0.1:8000/accounts/twitch/login/callback/'
    response_type = 'token%20id_token'
    scope = 'openid'
    # base_url = 'https://id.twitch.tv/oauth2/authorize'
    # url_token = 'client_id={}&client_secret={}&grant_type=authorization_code&&redirect_uri={}'.format(client_id, secret_key, redirect_uri)
    # full_url = '{}?client_id={}&redirect_uri={}&response_type=code&scope={}'.format(base_url, client_id, redirect_uri, scope)

    r = requests.get('https://api.twitch.tv/kraken/games/top?client_id={}'.format(client_id))
    content = r.json()
    result = content['_total']
    top = content['top'][0]['game']['name']

    return render(request, 'streams/api_view.html', {
                                                    "top":top,})
@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        author = request.user
        stream_title = request.POST.get('stream_title')
        stream_description = request.POST.get('stream_description')
        response_data = {}

        post = StreamPost(title=stream_title, description=stream_description, author=author)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['title'] = post.title
        response_data['description'] = post.description
        response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.author.username
        response_data['upvotes'] = post.upvotes
        response_data['downvotes'] = post.downvotes

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

class AddStreamModalView(LoginRequiredMixin, CreateView):
    """
    Allows a user to add their stream to the homepage
    """
    model = StreamPost
    form_class = StreamPostForm
    template_name = 'streams/add_stream_form.html'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'streams/add_stream_success.html',
                     {'StreamPost': self.object})

class StreamDetailView(LoginRequiredMixin, DetailView):
    model = StreamPost
    template_name = 'streams/detail.html'

def add_up_vote(request):
    pass
