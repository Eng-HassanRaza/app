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
        account = get_object_or_404(Account, pk=request.user.id)

        if not account.user.is_active:
            raise Http404

        if account.is_private:
            return render(request, 'new_profile_long.html', {
                "account": account
            })

        # instagram
        ig_paginator = get_paginator(
            InstagramInfo.objects.filter(user=account.user).order_by("-publish_at"))
        instagram_list = ig_paginator.get_page(1)

        # youtube
        yt_paginator = get_paginator(
            YoutubeInfo.objects.filter(user=account.user).order_by("-publish_at"))
        youtube_list = yt_paginator.get_page(1)

        # twitter
        twitter_token = account.twitter_token
        twitter_id = twitter_token.twitter_name if twitter_token is not None else None

        logger.info("instagram_list={}, youtube_list={}".format(instagram_list.has_next(), youtube_list.has_next()))

        params = {
            "account": account,
            "instagram_list": instagram_list,
            "youtube_list": youtube_list,
            "twitter_id": twitter_id,
        }
        if account.ssp_landscape is not None:
            params["SSP_TAG_LAND"] = account.ssp_landscape
        if account.ssp_post is not None:
            params["SSP_TAG_POST"] = account.ssp_post
        return render(request, 'new_profile_long.html', params)
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
