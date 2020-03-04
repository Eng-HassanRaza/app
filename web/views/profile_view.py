import logging

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET

from web.forms import AccountForm
from web.models import Account, InstagramInfo, YoutubeInfo

logger = logging.getLogger("main")


def profile(request):
    """プロフィール編集"""
    if not request.user.is_authenticated:
        return redirect("/")

    if request.user.is_staff:
        return redirect("/admin")

    try:
        account = request.user.account
    except:
        account = None

    if request.method == 'POST':
        # logger.info("profile:POST: request={}".format(request.POST))
        form = AccountForm(data=request.POST, files=request.FILES, instance=account)
        if form.is_valid():
            form.save()
            return redirect('/profile/{}/'.format(request.user.account.id))
        else:
            logger.warning("Error: {}".format(form.errors))
    else:
        if "form_data" in request.session:
            form = AccountForm(data=request.session["form_data"], instance=account)
            # logger.info("hasData: {}".format(request.session["form_data"]))
            del request.session['form_data']
        else:
            form = AccountForm(instance=account)

    return render(request, 'new_profile.html', {
        'form': form,
        "account": account
    })


def get_paginator(query_set):
    return Paginator(query_set, 11)


@require_GET
def profile_long(request, account_id):
    """プロフィールページ"""
    account = get_object_or_404(Account, pk=account_id)

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


@require_GET
def instagram_list(request, account_id):
    """プロフィールページ"""
    account = get_object_or_404(Account, pk=account_id)

    if not account.user.is_active:
        raise Http404

    if account.is_private and not request.user.is_authenticated:
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

    # logger.info("instagram_list={}, youtube_list={}".format(instagram_list.has_next(), youtube_list.has_next()))

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
    return render(request, 'parts/new_instagram_list.html', params)


@require_GET
def twitter_list(request, account_id):
    """プロフィールページ"""
    account = get_object_or_404(Account, pk=account_id)

    if not account.user.is_active:
        raise Http404

    if account.is_private and not request.user.is_authenticated:
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

    # logger.info("instagram_list={}, youtube_list={}".format(instagram_list.has_next(), youtube_list.has_next()))

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
    return render(request, 'parts/twitter_page.html', params)

@require_GET
def youtube_list(request, account_id):
    """プロフィールページ"""
    account = get_object_or_404(Account, pk=account_id)

    if not account.user.is_active:
        raise Http404

    if account.is_private and not request.user.is_authenticated:
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

    # logger.info("instagram_list={}, youtube_list={}".format(instagram_list.has_next(), youtube_list.has_next()))

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
    return render(request, 'parts/new_youtube_list.html', params)


@require_GET
def profile_ig(request, account_id):
    """ Instagramのmore """
    account = get_object_or_404(Account, pk=account_id)

    if account.is_private or not account.user.is_active or "last_id" not in request.GET:
        raise Http404

    last_id = request.GET.get("last_id")
    last_item = get_object_or_404(InstagramInfo, pk=last_id)

    # instagram
    query = InstagramInfo.objects.filter(user=account.user, publish_at__lt=last_item.publish_at).order_by("-publish_at")
    ig_paginator = get_paginator(query)
    instagram_list = ig_paginator.get_page(1)

    # set parameter
    params = {
        "account": account,
        "instagram_list": instagram_list,
    }
    if account.ssp_landscape is not None:
        params["SSP_TAG_LAND"] = account.ssp_landscape
    if account.ssp_post is not None:
        params["SSP_TAG_POST"] = account.ssp_post
    return render(request, 'parts/new_instagram_list.html', params)


@require_GET
def profile_yt(request, account_id):
    """ YouTubeのmore """
    account = get_object_or_404(Account, pk=account_id)

    if account.is_private or not account.user.is_active or "last_id" not in request.GET:
        raise Http404

    last_id = request.GET.get("last_id")
    last_item = get_object_or_404(YoutubeInfo, pk=last_id)

    # youtubes
    query = YoutubeInfo.objects.filter(user=account.user, publish_at__lt=last_item.publish_at).order_by("-publish_at")
    paginator = get_paginator(query)
    item_list = paginator.get_page(1)
    logger.debug("item_list={}".format(query.count()))

    # set parameter
    params = {
        "account": account,
        "youtube_list": item_list,
    }
    if account.ssp_landscape is not None:
        params["SSP_TAG_LAND"] = account.ssp_landscape
    if account.ssp_post is not None:
        params["SSP_TAG_POST"] = account.ssp_post
    return render(request, 'parts/youtube_list.html', params)
