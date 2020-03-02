import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from web.models import Account

logger = logging.getLogger("main")


@require_GET
def login(request):
    """ログイン画面"""
    if request.user.is_authenticated:
        return redirect("/admin" if request.user.is_staff else "/")

    request.session['auth_page'] = "login"
    return render(request, 'login.html')


@require_GET
def signup(request):
    """新規登録画面"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("/admin")
        else:
            return render(request, 'signup_re.html')
        # return redirect("/admin" if request.user.is_staff else "/")

    request.session['auth_page'] = "signup"
    return render(request, 'signup.html')


@require_GET
def leave(request):
    """退会画面"""
    if not request.user.is_authenticated:
        return redirect("/")

    return render(request, 'new_leave.html')


@require_GET
def thanks(request):
    """新規登録後画面"""
    if not request.user.is_authenticated:
        return redirect("/")

    if request.user.is_staff:
        return redirect("/admin")

    try:
        account = request.user.account
        if account.display_name == "" or account.display_name is None:
            return render(request, 'thanks.html')
        else:
            return redirect("/")
    except ObjectDoesNotExist:
        parent_id = request.session['parent'] if "parent" in request.session else None

        account = Account(user=request.user, parent_id=parent_id)
        account.save()
        if parent_id is not None:
            del request.session['parent']

        return render(request, 'thanks.html')


@require_GET
def invite(request, parent_id=None):
    """登録者ページ"""
    if request.user.is_authenticated:
        return redirect("/admin" if request.user.is_staff else "/")

    print("parent_id={}".format(parent_id))
    account = Account.objects.filter(page_id=parent_id).first()

    if account is None or account.is_private or not account.user.is_active:
        raise Http404

    request.session['parent'] = parent_id
    print("request.session['parent']=" + request.session['parent'])
    return redirect("/signup")


@require_GET
def canceled(request):
    """キャンセル時の画面"""
    logger.info("Login Cancel")

    if request.user.is_authenticated:
        return redirect("/admin" if request.user.is_staff else "/")

    auth_page = request.session['auth_page'] if "auth_page" in request.session else None
    if auth_page == "login":
        return redirect('/login')
    else:
        return redirect('/signup')


@require_GET
def error(request):
    """エラー時の画面"""
    logger.info("Login Error")

    if request.user.is_authenticated:
        return redirect("/admin" if request.user.is_staff else "/")

    auth_page = request.session['auth_page'] if "auth_page" in request.session else None
    if auth_page == "login":
        return redirect('/login')
    else:
        return redirect('/signup')
