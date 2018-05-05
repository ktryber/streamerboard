#STREAMS urls.py
from django.conf.urls import url, include
from .views import streams_list, api_view

app_name = 'streams'

urlpatterns = [
    url(r'^$', streams_list, name='all-streams'),
    url(r'^api/', api_view, name='api')


]
