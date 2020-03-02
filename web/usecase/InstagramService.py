import logging

from django.contrib.sites.models import Site

from web.api.InstagramApi import InstagramApi
from web.models import InstagramToken, Account, InstagramInfo

from allauth.socialaccount.models import SocialApp

logger = logging.getLogger("main")


class InstagramService:
    def __init__(self):
        try:
            app = SocialApp.objects.get_current("instagram")
            site = Site.objects.get_current()
            self.api = InstagramApi(app.client_id, app.secret, site.domain)
        except Exception as e:
            logger.error("not instagram app")

    def get_auth_url(self):
        return self.api.get_auth_url()

    def save_token(self, user, code):
        token_result = self.api.get_access_token(code)
        token = InstagramToken(
            token=token_result.access_token,
            name=token_result.user_id,
            type=token_result.token_type,
            expire=token_result.expires_in,
        )
        token.save()

        account = Account.objects.filter(user=user).first()
        if account is not None:
            account.instagram_token = token
            account.save()

    def delete_token(self, user):
        account = Account.objects.filter(user=user).first()
        if account is not None:
            InstagramInfo.objects.filter(user=user).delete()
            account.instagram_token = None
            account.save()
