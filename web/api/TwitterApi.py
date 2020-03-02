from urllib.parse import parse_qsl

import httplib2
from requests_oauthlib import OAuth1Session


class TwitterApi:
    def __init__(self, app_id, app_secret, domain):
        self.TW_CONSUMER_KEY = app_id
        self.TW_CONSUMER_SECRET = app_secret
        self.TW_CALLBACK = "https://{}/auth/tw/login/callback/".format(domain)
        self.client = httplib2.Http()

    def get_auth_url(self):
        twitter = OAuth1Session(self.TW_CONSUMER_KEY, self.TW_CONSUMER_SECRET)

        request_token_url = "https://api.twitter.com/oauth/request_token"
        response = twitter.post(
            request_token_url,
            params={'oauth_callback': self.TW_CALLBACK}
        )

        # responseからリクエストトークンを取り出す
        res_data = response.content.decode("utf-8")
        # logger.debug(urlencode(res_data))
        request_token = dict(parse_qsl(res_data))

        # リクエストトークンから連携画面のURLを生成
        authenticate_url = "https://api.twitter.com/oauth/authenticate"
        authenticate_endpoint = '%s?oauth_token=%s' % (authenticate_url, request_token['oauth_token'])

        return authenticate_endpoint

    def get_access_token(self, oauth_token, oauth_verifier):
        twitter = OAuth1Session(
            self.TW_CONSUMER_KEY,
            self.TW_CONSUMER_SECRET,
            oauth_token,
            oauth_verifier,
        )

        access_token_url = "https://api.twitter.com/oauth/access_token"
        response = twitter.post(
            access_token_url,
            params={'oauth_verifier': oauth_verifier}
        )

        return dict(parse_qsl(response.content.decode("utf-8")))
