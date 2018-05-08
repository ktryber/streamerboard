#STREAMS urls.py
from django.conf.urls import url, include
from . views import (streams_list, api_view, AddStreamModalView,
                    StreamDetailView, create_post, StreamUpvoteAPIToggle,
                    StreamDownvoteAPIToggle, StreamUpvoteToggle,
                    StreamUpvoteDownvoteCountAPIView)

app_name = 'streams'

urlpatterns = [
    url(r'^$', streams_list, name='all-streams'),
    # url(r'^api/', api_view, name='api'),
    url(r'^create_post/$', create_post, name='create_post'),
    url(r'^add_stream/$', AddStreamModalView.as_view(), name='add_stream'),
    url(r'^detail/(?P<pk>\d+)/$', StreamDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/upvote/$', StreamUpvoteToggle.as_view(), name='upvote-toggle'),
    url(r'^api/(?P<pk>\d+)/upvote/$', StreamUpvoteAPIToggle.as_view(),
                                                    name='upvote-api-toggle'),
    url(r'^api/(?P<pk>\d+)/downvote/$', StreamDownvoteAPIToggle.as_view(),
                                                    name='downvote-api-toggle'),
    url(r'^api/(?P<pk>\d+)/vote_count/$', StreamUpvoteDownvoteCountAPIView.as_view(),
                                                    name='vote-count'),



]
