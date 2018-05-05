from django.shortcuts import render
from decouple import config
import requests
import json
# Create your views here.


def streams_list(request):
    
    return render(request, 'streams/index.html',
                                            {})

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
                                                    "top":top,

                                                    })


# GET https://id.twitch.tv/oauth2/authorize
#     ?client_id=<your client ID>
#     &redirect_uri=<your registered redirect URI>
#     &response_type=<type>
#     &scope=<space-separated list of scopes>
