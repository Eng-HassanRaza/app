import datetime
import logging
from multiprocessing import Process

import isodate
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

from web.api.InstagramApi import InstagramApi
from web.models import Account, InstagramInfo, InstagramToken

logger = logging.getLogger("update_in")


class InstagramUpdateService:
    def __init__(self):
        try:
            app = SocialApp.objects.get_current("instagram")
            site = Site.objects.get_current()
            self.api = InstagramApi(app.client_id, app.secret, site.domain)
        except Exception as e:
            logger.error("not instagram app")

    def update_all(self):
        accounts = Account.objects.order_by("-id").all()

        for account in accounts:
            # Process(target=self.update_by_account, args=(account,)).start()
            self.update_by_account(account)

    def update_by_account(self, account):
        try:
            logger.info("update_by_account: account_id=%s" % account.id)

            user = account.user
            token = account.instagram_token
            if token is None:
                logger.warning("Token is None: account_id={}".format(account.id))
                return

                # トークンの更新
            if not token.is_valid():
                logger.info("Update token: account={}".format(account.id))
                new_token = self.api.refresh_access_token(token.token)
                token.token = new_token.access_token
                token.expire = new_token.expires_in
                token.save()

            # 最新のIDを取得
            latest_info = InstagramInfo.objects.filter(user=user).order_by("-publish_at").first()
            latest_info_id = latest_info.info_id if latest_info is not None else "none"
            logger.info("account.id={}, user.id={}, latest_info.id={}".format(account.id, user.id, latest_info_id))

            has_next = True
            next_url = None

            while has_next:
                result = self.api.get_medias(token.token, next_url)
                logger.info("account_id={}, item.size={}".format(account.id, len(result.data)))

                for item in result.data:
                    if latest_info is not None and latest_info.info_id == item.id:
                        # 最新のIDと一致していたら終わり
                        logger.info("FINISHED: account_id={}, item.id={}".format(account.id, item.id))
                        return

                    exist = InstagramInfo.objects.filter(user=user, info_id=item.id).first()
                    if exist is not None:
                        logger.info("Exists: account_id={}, info_id={}".format(account.id, item.id))
                        continue

                    logger.info("account_id={}, item={}".format(account.id, item))
                    InstagramInfo(
                        info_id=item.id,
                        url=item.permalink,
                        type=item.media_type,
                        thumbnail=item.media_url,
                        publish_at=isodate.parse_datetime(item.timestamp.replace('+0000', '+00:00')),
                        user=user
                    ).save()

                has_next = result.next_url is not None
                next_url = result.next_url
        except Exception as e:
            logger.warning("Error: account_id={}: {}".format(account.id, str(e)), exc_info=True)
