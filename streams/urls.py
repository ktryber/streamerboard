#STREAMS urls.py
from django.conf.urls import url, include
from . views import (streams_list, api_view, AddStreamModalView,
                    StreamDetailView, create_post)

app_name = 'streams'

urlpatterns = [
    url(r'^$', streams_list, name='all-streams'),
    url(r'^api/', api_view, name='api'),
    url(r'^create_post/$', create_post, name='create_post'),
    url(r'^add_stream/$', AddStreamModalView.as_view(), name='add_stream'),
    url(r'^detail/(?P<pk>\d+)/$', StreamDetailView.as_view(), name='detail'),


]
