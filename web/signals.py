import logging

from allauth.socialaccount.signals import pre_social_login, social_account_added, social_account_updated
from django.dispatch import receiver

logger = logging.getLogger("main")


@receiver(pre_social_login)
def pre_social_login(request, sociallogin, **kwargs):
    logger.info("pre_social_login: name={}, token={}, process={}".format(request.user.username, sociallogin.token,
                                                                         sociallogin.state['process']))

    if sociallogin.state['process'] != 'connect':
        return

    user = request.user
    token = sociallogin.token

    logger.info("pre_social_login: provider={}".format(token.app.provider))
    if token.app.provider == "twitter":
        user.account.twitter_info = token
        user.account.save()
    elif token.app.provider == "instagram":
        user.account.instagram_info = token
        user.account.save()
    elif token.app.provider == "youtube":
        user.account.youtube_info = token
        user.account.save()


# @receiver(social_account_added)
# def social_account_added(request, sociallogin, **kwargs):
#     logger.info("pre_social_login: name={}, token={}, process={}".format(request.user.username, sociallogin.token,
#                                                                          sociallogin.state['process']))
#
#     if sociallogin.state['process'] != 'connect':
#         return
#
#     user = request.user
#     token = sociallogin.token
#
#     logger.info("pre_social_login: provider={}".format(token.app.provider))
#     if token.app.provider == "twitter":
#         user.account.twitter_info = token
#         user.account.save()
#     elif token.app.provider == "instagram":
#         user.account.instagram_info = token
#         user.account.save()
#     elif token.app.provider == "youtube":
#         user.account.youtube_info = token
#         user.account.save()
