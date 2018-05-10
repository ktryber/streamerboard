from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, UpdateView, CreateView,
                                DeleteView, FormView, View)
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.views.generic import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from decouple import config
import requests
import json
from . models import StreamPost
from . forms import StreamPostForm

from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def streams_list(request):
    streams_ranked = StreamPost.objects.annotate(q_count=Count('upvotes')) \
                                    .order_by('-q_count')
    context = {
        'streams_ranked' : streams_ranked,
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
        response_data['upvotes'] = post.upvotes.count()
        response_data['downvotes'] = post.downvotes.count()

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

class StreamUpvoteAPIToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        # pk = self.kwargs.get("pk")
        obj = get_object_or_404(StreamPost, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        upvoted = False

        if user.is_authenticated:
            if user in obj.upvotes.all():
                upvoted = False
                obj.upvotes.remove(user)
            else:
                upvoted = True
                obj.upvotes.add(user)
            updated = True
        data = {
            "updated": updated,
            "upvoted": upvoted,
        }
        return Response(data)

class StreamUpvoteToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(StreamPost, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.upvotes.all():
                obj.upvotes.remove(user)
            else:
                obj.upvotes.add(user)
        return url_

class StreamDownvoteAPIToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        # pk = self.kwargs.get("pk")
        obj = get_object_or_404(StreamPost, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        downvoted = False

        if user.is_authenticated:
            if user in obj.downvotes.all():
                downvoted = False
                obj.downvotes.remove(user)
            else:
                downvoted = True
                obj.downvotes.add(user)
            updated = True
        data = {
            "updated": updated,
            "downvoted": downvoted,
        }
        return Response(data)

class StreamDownvoteToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(StreamPost, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.downvotes.all():
                obj.downvotes.remove(user)
            else:
                obj.downvotes.add(user)
        return url_

class StreamUpvoteDownvoteCountAPIView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        # pk = self.kwargs.get("pk")
        obj = get_object_or_404(StreamPost, pk=pk)
        upvote_count = obj.upvotes.count()
        downvote_count = obj.downvotes.count()
        data = {
            "upvotes" : upvote_count,
            "downvotes" : downvote_count,
        }
        return Response(data)

from collections import OrderedDict
from operator import itemgetter

class StreamListRankedAPIView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        # streams_ranked = StreamPost.objects.annotate(q_count=Count('upvotes')) \
        #                                     .order_by('-q_count')


        streams_list = StreamPost.objects.all()
        streams_ranked = [{'id':stream.pk, 'upvotes': stream.upvotes.count(), \
                            'title':stream.title, 'description': stream.description} \
                                                    for stream in streams_list]

        sorted_list = sorted(streams_ranked, key=itemgetter('upvotes'), reverse=True)
        data = {
            "sorted_list": sorted_list
                    }
        return Response(data)
