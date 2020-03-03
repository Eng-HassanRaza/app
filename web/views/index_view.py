import logging
from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET
from web.forms import AccountForm
from web.models import Account, InstagramInfo, YoutubeInfo

from web.models import Account

logger = logging.getLogger("main")

def get_paginator(query_set):
    return Paginator(query_set, 11)
@require_GET
def index(request):
    """トップ画面"""

    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('/profile/'+str(request.user.id))
    user_count = Account.objects.filter(user__is_active=True).order_by("-id").count()

    query = Account.objects.filter(user__is_active=True, is_private=False).exclude(display_name="").order_by("-id")
    first_users = query[:9]
    users = query[9:21]  # first(9)+size(12) = 21
    return render(request, 'new_index.html', {
        "user_count": '{:,}'.format(user_count),
        "first_users": first_users,
        "users": users,
        "hasNext": user_count > 21
    })


@require_GET
def more_users(request):
    """more users"""

    if "last_id" not in request.GET:
        raise Http404
    last_id = request.GET.get("last_id")

    query = Account.objects.filter(user__is_active=True, is_private=False, id__lt=last_id).exclude(
        display_name="").order_by("-id")
    paginator = Paginator(query, 12)
    users = paginator.get_page(1)

    return render(request, 'parts/user_list.html', {
        "users": users,
        "hasNext": users.has_next()
    })
