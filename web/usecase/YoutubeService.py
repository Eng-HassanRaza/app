import logging

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

from web.api.YoutubeApi import YoutubeApi
from web.models import YoutubeToken, Account, YoutubeInfo

logger = logging.getLogger("main")


class YoutubeService:
    def __init__(self):
        try:
            app = SocialApp.objects.get_current("google")
            site = Site.objects.get_current()
            self.api = YoutubeApi(app.client_id, app.secret, site.domain)
        except Exception as e:
            logger.error("not google app")

    def get_auth_url(self):
        return self.api.get_auth_url()

    def save_token(self, user, code):
        res = self.api.get_access_token(code)
        token = YoutubeToken.objects.filter(user_id=res.user_id).first()

        if token is None:
            logger.info("ADD TOKEN: uid={}, token={}".format(res.user_id, token))
            token = YoutubeToken(
                user_id=res.user_id,
                email=res.email,
                user_name=res.user_name,
                token=res.access_token,
                refresh=res.refresh_token,
                type=res.token_type,
                expire=res.expires_in,
            )
            token.save()
        else:
            logger.info("UPDATE YOUTUBE TOKEN: uid={}, token={}".format(res.user_id, token))
            token.token = res.access_token
            token.expire = res.expires_in
            token.save()

        account = Account.objects.filter(user=user).first()
        if account is not None:
            if not account.is_private:
                account.is_private = False
            account.youtube_token = token
            account.save()

    def delete_token(self, user):
        account = Account.objects.filter(user=user).first()
        if account is not None:
            YoutubeInfo.objects.filter(user=user).delete()
            account.youtube_token = None
            account.save()
