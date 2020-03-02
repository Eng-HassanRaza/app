import datetime
import logging
from multiprocessing import Process

import isodate
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

from web.api.YoutubeApi import YoutubeApi
from web.models import Account, YoutubeInfo, YoutubeToken

logger = logging.getLogger("update_yt")


class YoutubeUpdateService:
    def __init__(self):
        try:
            app = SocialApp.objects.get_current("google")
            site = Site.objects.get_current()
            self.api = YoutubeApi(app.client_id, app.secret, site.domain)
        except Exception as e:
            logger.error("not google app")

    def update_all(self):
        accounts = Account.objects.order_by("-id").all()

        for account in accounts:
            # Process(target=self.update_by_account, args=(account,)).start()
            self.update_by_account(account)

    def update_by_account(self, account):
        try:
            logger.info("update_by_account: account_id=%s" % account.id)

            user = account.user
            token = account.youtube_token
            if token is None:
                logger.warning("Token is None: account_id={}".format(account.id))
                return

            # トークンの更新
            if not token.is_valid():
                logger.info("Update token: account={}".format(account.id))
                new_token = self.api.refresh_token(token.refresh)
                token.token = new_token.access_token
                token.expire = new_token.expires_in
                token.save()

            channels = self.api.get_channels(token.token)

            for channel in channels:

                # 最新のIDを取得
                chanel_id = channel.chanel_id
                latest_info = YoutubeInfo.objects.filter(user=user, chanel_id=chanel_id).order_by("-publish_at").first()
                latest_info_id = latest_info.info_id if latest_info is not None else "none"
                logger.info("account.id={}, user.id={}, chanel_id={}, latest_info.id={}".format(
                    account.id, user.id, chanel_id, latest_info_id))

                has_next = True
                next_token = None

                while has_next:
                    video_result = self.api.get_videos(token.token, channel.playlist_id, next_token)

                    for video in video_result.videos:
                        logger.info("account_id={}, video={}".format(account.id, video))

                        if latest_info is not None and latest_info.info_id == video.video_id:
                            # 最新のIDと一致していたら終わり
                            msg = "FINISH: account_id={}, video.videoId={}, latest_info.info_id={}"
                            logger.info(msg.format(account.id, video.video_id, latest_info.info_id))
                            return

                        exist = YoutubeInfo.objects.filter(user=user, info_id=video.video_id).first()
                        if exist is not None:
                            logger.info("Exists: account_id={}, video_id={}".format(account.id, video.video_id))
                            continue

                        info = YoutubeInfo(
                            info_id=video.video_id,
                            chanel_id=chanel_id,
                            url=video.url,
                            thumbnail=video.thumbnail,
                            time=video.time,
                            title=video.title,
                            details=video.details,
                            publish_at=isodate.parse_datetime(video.publishedAt.replace('Z', '+00:00')),
                            user=user
                        )
                        info.save()

                    has_next = video_result.next_token is not None
                    next_token = video_result.next_token

        except Exception as e:
            logger.warning("Error: account_id={}: {}".format(account.id, str(e)), exc_info=True)
