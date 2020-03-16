import logging

from django.contrib import messages
from django.shortcuts import redirect
from web.forms import AccountForm
from web.usecase.YoutubeService import YoutubeService

logger = logging.getLogger("main")

yt_service = YoutubeService()


def login(request):
    logger.info("youtube login")
    if request.method == 'POST':
        try:
            account = request.user.account
        except:
            account = None

        form = AccountForm(data=request.POST, files=request.FILES, instance=account)
        if form.is_valid():
            form.save()
        logger.info("youtube login: save form data")
        request.session['form_data'] = request.POST

    url = yt_service.get_auth_url()
    return redirect(url)


def logout(request):
    try:
        if request.method == 'POST':
            logger.info("youtube logout: save form data")
            request.session['form_data'] = request.POST

        yt_service.delete_token(request.user)
    except Exception as e:
        messages.error(request, 'Youtubeの認証解除でエラーが発生しました')
        logger.error("Error: user.id={}: {}".format(request.user, str(e)), exc_info=True)

    return redirect("/profile/edit/")

from web.usecase import YoutubeUpdateService
from web.models import Account
youtube_update_service = YoutubeUpdateService.YoutubeUpdateService()
def callback(request):
    try:
        logger.info("youtube callback: uid={}, param={}".format(request.user, request.GET))
        if "code" in request.GET:
            code = request.GET["code"]
            # DBに保存
            yt_service.save_token(request.user, code)
            account_id = Account.objects.filter(user=request.user).first()
            youtube_update_service.update_by_account(account_id)
    except Exception as e:
        messages.error(request, 'Youtubeの認証でエラーが発生しました')
        logger.error("Error: user.id={}: {}".format(request.user, str(e)), exc_info=True)

    return redirect("/profile/edit/")
