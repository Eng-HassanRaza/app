import json
import logging
from urllib.parse import urlencode

import httplib2

from web.domain.enums import IgMediaType

logger = logging.getLogger("main")


class InstagramTokenResult:
    def __init__(self, user_id: str, access_token: str, token_type: str, expires_in: int):
        self.user_id = user_id
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in


class MediaInfo:

    def __init__(self, id: str, media_url: str, media_type: IgMediaType, permalink: str, timestamp: str):
        self.id = id
        self.media_url = media_url
        self.media_type = media_type
        self.permalink = permalink
        self.timestamp = timestamp


class InstagramResult:
    def __init__(self, data: [MediaInfo], next_url: str):
        self.data = data
        self.next_url = next_url


class InstagramApi:
    def __init__(self, app_id, app_secret, domain):
        self.client = httplib2.Http()
        self.IG_APP_ID = app_id
        self.IG_APP_SECRET = app_secret
        self.IG_REDIRECT_URL = "https://{}/auth/ig/login/callback/".format(domain)

    def get_auth_url(self):
        entry_point = "https://api.instagram.com/oauth/authorize"
        url_format = "{}?app_id={}&redirect_uri={}&scope=user_profile,user_media&response_type=code&hl=en"
        url = url_format.format(entry_point, self.IG_APP_ID, self.IG_REDIRECT_URL)
        logger.debug("URL: {}".format(url))
        return url

    def get_access_token(self, code):
        # 認証コードから1時間のアクセストークンを取得
        short_token = self.__get_short_access_token__(code)
        if "error_type" in short_token:
            raise Exception(short_token)

        # 1時間のアクセストークンを60日の長期間トークンに変換
        long_token = self.__get_long_access_token__(short_token["access_token"])
        if "error_type" in long_token:
            raise Exception(short_token)

        return InstagramTokenResult(
            user_id=short_token["user_id"],
            access_token=long_token["access_token"],
            token_type=long_token["token_type"],
            expires_in=long_token["expires_in"]
        )

    def __get_short_access_token__(self, code):
        """
        認証コードから1時間のアクセストークンを取得
        """
        url = "https://api.instagram.com/oauth/access_token"
        params = {
            "client_id": self.IG_APP_ID,
            "app_id": self.IG_APP_ID,
            "app_secret": self.IG_APP_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": self.IG_REDIRECT_URL,
            "code": code
        }
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        _, content = self.client.request(
            url,
            method='POST',
            headers=headers,
            body=urlencode(params),
        )
        return json.loads(content.decode('utf-8'))

    def __get_long_access_token__(self, short_token):
        """
        1時間のアクセストークンを60日のトークンに変換
        """
        url = "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={}&access_token={}"
        _, content = self.client.request(url.format(self.IG_APP_SECRET, short_token))
        return json.loads(content.decode('utf-8'))

    def refresh_access_token(self, long_token):
        """
        リフレッシュトークンの取得
        """
        endpoint = "https://graph.instagram.com/refresh_access_token"
        url = "{}?grant_type=ig_refresh_token&access_token={}"
        _, content = self.client.request(url.format(endpoint, long_token))
        res = json.loads(content.decode('utf-8'))
        return InstagramTokenResult(
            user_id="",
            access_token=res["access_token"],
            token_type=res["token_type"],
            expires_in=res["expires_in"],
        )

    def get_medias(self, token, next_url=None):
        """
        IGのmediaを取得
        """
        if next_url is None:
            entry_point = "https://graph.instagram.com/me/media"
            url_format = "{}?fields=id,media_url,media_type,thumbnail_url,permalink,timestamp&access_token={}"
            url = url_format.format(entry_point, token)
        else:
            url = next_url
        _, content = self.client.request(url)
        res = json.loads(content.decode('utf-8'))

        if "data" not in res:
            logger.error("Error: get_medias: {}".format(json.dumps(res, indent=2)))

        return InstagramResult(
            data=list(map(lambda x: self.__to_info__(x), res["data"])) if "data" in res else [],
            next_url=res["paging"]["next"] if "next" in res["paging"] else None
        )

    def __to_info__(self, item):
        media_type = IgMediaType.value_of(item["media_type"])
        # logger.info("media_type={}, raw={}".format(media_type, item["media_type"]))
        if media_type == IgMediaType.VIDEO:
            return MediaInfo(
                id=item["id"],
                media_url=item["thumbnail_url"],
                media_type=item["media_type"],
                permalink=item["permalink"],
                timestamp=item["timestamp"],
            )
        else:
            return MediaInfo(
                id=item["id"],
                media_url=item["media_url"],
                media_type=item["media_type"],
                permalink=item["permalink"],
                timestamp=item["timestamp"],
            )
