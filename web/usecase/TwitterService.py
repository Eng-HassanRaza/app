import logging

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

from web.api.TwitterApi import TwitterApi
from web.models import TwitterToken, Account

logger = logging.getLogger("main")


class TwitterService:
    def __init__(self):
        try:
            app = SocialApp.objects.get_current("twitter")
            site = Site.objects.get_current()
            self.api = TwitterApi(app.client_id, app.secret, site.domain)
        except Exception as e:
            logger.error("not twitter app")

    def get_auth_url(self):
        return self.api.get_auth_url()

    def save_token(self, user, oauth_token, oauth_verifier):
        token_result = self.api.get_access_token(oauth_token, oauth_verifier)
        token = TwitterToken.objects.filter(twitter_id=token_result["user_id"]).first()

        if token is None:
            token = TwitterToken(
                twitter_id=token_result["user_id"],
                twitter_name=token_result["screen_name"],
                token=token_result["oauth_token"],
                secret=token_result["oauth_token_secret"],
            )
            token.save()
        else:
            logger.info("UPDATE TWITTER TOKEN: uid={}, token={}".format(token_result["user_id"], token))
            token.twitter_name = token_result["screen_name"]
            token.token = token_result["oauth_token"]
            token.secret = token_result["oauth_token_secret"]
            token.save()

        account = Account.objects.filter(user=user).first()
        if account is not None:
            account.twitter_token = token
            account.save()

    def delete_token(self, user):
        account = Account.objects.filter(user=user).first()
        if account is not None:
            account.twitter_token = None
            account.save()
