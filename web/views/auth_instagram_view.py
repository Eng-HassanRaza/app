import logging

from django.contrib import messages
from django.shortcuts import redirect
from web.forms import AccountForm
from web.usecase.InstagramService import InstagramService

logger = logging.getLogger("main")

ig_service = InstagramService()


def login(request):
    logger.info("instagram login")

    if request.method == 'POST':
        try:
            account = request.user.account
        except:
            account = None

        form = AccountForm(data=request.POST, files=request.FILES, instance=account)
        if form.is_valid():
            form.save()
        logger.info("instagram login: save form data")
        request.session['form_data'] = request.POST

    url = ig_service.get_auth_url()
    return redirect(url)


def logout(request):
    try:
        if request.method == 'POST':
            logger.info("instagram logout: save form data")
            request.session['form_data'] = request.POST

        ig_service.delete_token(request.user)
    except Exception as e:
        messages.error(request, 'Instagramの認証解除でエラーが発生しました')
        logger.error("Error: user.id={}: {}".format(request.user, str(e)), exc_info=True)

    return redirect("/profile/edit/")


def callback(request):
    try:
        logger.info("instagram callback: uid={}, param={}".format(request.user, request.GET))
        if "code" in request.GET:
            code = request.GET["code"]
            # DBに保存

            ig_service.save_token(request.user, code)
    except Exception as e:
        messages.error(request, 'Instagramの認証でエラーが発生しました')
        logger.error("Error: user.id={}: {}".format(request.user, str(e)), exc_info=True)

    return redirect("/profile/edit/")
