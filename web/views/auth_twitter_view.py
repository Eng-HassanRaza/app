import logging

from django.contrib import messages
from django.shortcuts import redirect

from web.usecase.TwitterService import TwitterService

logger = logging.getLogger("main")

tw_service = TwitterService()


def login(request):
    logger.info("twitter login")

    if request.method == 'POST':
        logger.info("twitter login: save form data")
        request.session['form_data'] = request.POST

    url = tw_service.get_auth_url()
    return redirect(url)


def logout(request):
    try:
        if request.method == 'POST':
            logger.info("twitter logout: save form data")
            request.session['form_data'] = request.POST

        tw_service.delete_token(request.user)
    except Exception as e:
        messages.error(request, 'Twitterの認証解除でエラーが発生しました')
        logger.error("Error: user.id={}: {}".format(request.user, str(e)), exc_info=True)

    return redirect("/profile/edit/")


def callback(request):
    try:
        logger.info("twitter callback: uid={}, param={}".format(request.user, request.GET))
        logger.debug(request.GET)
        oauth_token = request.GET["oauth_token"]
        oauth_verifier = request.GET["oauth_verifier"]

        if oauth_token is not None and oauth_verifier is not None:
            # DBに保存
            tw_service.save_token(request.user, oauth_token, oauth_verifier)
    except Exception as e:
        messages.error(request, 'Twitterの認証でエラーが発生しました')
        logger.error("Error: user.id={}: {}".format(request.user, str(e)), exc_info=True)

    return redirect("/profile/edit/")
