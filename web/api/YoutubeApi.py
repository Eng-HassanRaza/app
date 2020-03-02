import itertools
import json
import logging
from urllib.parse import urlencode

import httplib2
import isodate

logger = logging.getLogger("main")

YOUTUBE_API_ROOT = "https://www.googleapis.com/youtube/v3"


class ChannelInfo(object):
    def __init__(self, chanel_id: str, channel_name: str, playlist_id: str, thumbnail: str):
        self.chanel_id = chanel_id
        self.channel_name = channel_name
        self.playlist_id = playlist_id
        self.thumbnail = thumbnail


class VideoInfo(object):
    def __init__(self, title: str, details: str, time: str, video_id: str, thumbnail: str, url: str, publishedAt: str):
        self.title = title
        self.details = details
        self.time = time
        self.video_id = video_id
        self.thumbnail = thumbnail
        self.url = url  # https://www.youtube.com/watch?v=<video_id>
        self.publishedAt = publishedAt


class VideosResult:
    def __init__(self, total_results: int, results_per_page: int, next_token: str, videos: [VideoInfo]):
        self.total_results = total_results
        self.results_per_page = results_per_page
        self.next_token = next_token
        self.videos = videos


class YoutubeTokenResult:
    def __init__(self, user_id: str, email: str, user_name: str,
                 access_token: str, token_type: str, expires_in: int, refresh_token: str):
        self.user_id = user_id
        self.email = email
        self.user_name = user_name
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.refresh_token = refresh_token


class YoutubeRefreshToken:
    def __init__(self, access_token: str, token_type: str, expires_in: int):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in


def get_format_time(time):
    td = isodate.parse_duration(time)
    s = td.total_seconds()
    # hours = s // 3600
    # s = s - (hours * 3600)
    minutes = s // 60
    seconds = s - (minutes * 60)
    # return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
    return '{:02}:{:02}'.format(int(minutes), int(seconds))


class YoutubeApi:
    def __init__(self, app_id, app_secret, domain):
        self.YT_CLIENT_ID = app_id
        self.YT_CLIENT_SECRET = app_secret
        self.YT_REDIRECT_URL = "https://{}/auth/yt/login/callback/".format(domain)
        self.client = httplib2.Http()

    def __call_api__(self, url, access_token=None):
        """
        API呼び出し
        """

        if access_token is not None:
            headers = {"Authorization": "Bearer {}".format(access_token)}
            _, content = self.client.request("{}{}".format(YOUTUBE_API_ROOT, url), headers=headers)
        else:
            _, content = self.client.request("{}{}&key={}".format(YOUTUBE_API_ROOT, url, self.api_key))
        return json.loads(content.decode('utf-8'))

    def get_auth_url(self):
        entry_point = "https://accounts.google.com/o/oauth2/auth"
        scope = "profile email https://www.googleapis.com/auth/youtube.readonly"
        url_format = "{}?client_id={}&redirect_uri={}&scope={}&response_type=code&access_type=offline"
        url = url_format.format(entry_point, self.YT_CLIENT_ID, self.YT_REDIRECT_URL, scope)
        logger.debug("URL: {}".format(url))
        return url

    def get_access_token(self, code):
        # 認証コードからアクセストークンを取得
        access_token = self.__get_short_access_token__(code)
        logger.info("access_token={}".format(json.dumps(access_token)))
        # print(access_token)
        if "error_type" in access_token:
            raise Exception(access_token)

        profile = self.get_profile(access_token["access_token"])
        if "error_type" in profile:
            raise Exception(profile)

        # # チャンネル情報の取得
        # channels = self.get_channels(access_token["access_token"])

        # print(channels)
        return YoutubeTokenResult(
            user_id=profile["id"],
            email=profile["email"],
            user_name=profile["name"],
            access_token=access_token["access_token"],
            token_type=access_token["token_type"],
            expires_in=access_token["expires_in"],
            refresh_token=access_token["refresh_token"] if "refresh_token" in access_token else "",
        )

    def __get_short_access_token__(self, code):
        """
        認証コードからアクセストークンを取得
        """
        url = "https://accounts.google.com/o/oauth2/token"
        params = {
            "code": code,
            "client_id": self.YT_CLIENT_ID,
            "client_secret": self.YT_CLIENT_SECRET,
            "redirect_uri": self.YT_REDIRECT_URL,
            "grant_type": "authorization_code"
        }
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        _, content = self.client.request(
            url,
            method='POST',
            headers=headers,
            body=urlencode(params),
        )
        data = json.loads(content.decode('utf-8'))
        return data

    def get_profile(self, access_token):
        url = "https://www.googleapis.com/oauth2/v1/userinfo?access_token={}"
        _, content = self.client.request(url.format(access_token))
        data = json.loads(content.decode('utf-8'))
        logger.info("data={}".format(json.dumps(data)))
        return data

    def refresh_token(self, refresh_token):
        """
        認証コードからアクセストークンを取得
        """
        url = "https://accounts.google.com/o/oauth2/token"
        params = {
            "refresh_token": refresh_token,
            "client_id": self.YT_CLIENT_ID,
            "client_secret": self.YT_CLIENT_SECRET,
            "grant_type": "refresh_token"
        }
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        _, content = self.client.request(
            url,
            method='POST',
            headers=headers,
            body=urlencode(params),
        )
        res = json.loads(content.decode('utf-8'))
        logger.info("{}".format(json.dumps(res, indent=2)))
        return YoutubeRefreshToken(
            access_token=res["access_token"],
            expires_in=res["expires_in"],
            token_type=res["token_type"]
        )

    def get_channels(self, access_token):
        """
        チャンネルのアップロードの再生リストを取得
        """
        url = "/channels?part=id,snippet,contentDetails&mine=true"
        result = self.__call_api__(url, access_token)
        # print(json.dumps(result, ensure_ascii=False, indent=2))
        return list(map(lambda x: ChannelInfo(
            chanel_id=x["id"],
            channel_name=x["snippet"]["title"],
            thumbnail=x["snippet"]["thumbnails"]["default"]["url"],
            playlist_id=x["contentDetails"]["relatedPlaylists"]["uploads"]
        ), result["items"] if "items" in result else []))

    def get_videos(self, access_token, playlist_id, next_token=None):
        url = "/playlistItems?part=id,contentDetails&maxResults,status=5&playlistId={}".format(playlist_id)
        if next_token is not None:
            url += "&pageToken={}".format(next_token)

        result = self.__call_api__(url, access_token)
        # print(json.dumps(result, ensure_ascii=False, indent=2))
        if "items" in result:
            video_info_list = list(itertools.chain.from_iterable(
                map(lambda x: self._get_video_info_(access_token, x["contentDetails"]["videoId"]),
                    result["items"])))
        else:
            video_info_list = []
        return VideosResult(
            total_results=result["pageInfo"]["totalResults"],
            results_per_page=result["pageInfo"]["resultsPerPage"],
            next_token=result["nextPageToken"] if "nextPageToken" in result else None,
            videos=video_info_list,
        )

    def _get_video_info_(self, access_token, video_id):
        url = "/videos?part=id,snippet,contentDetails,status&id={}".format(video_id)
        result = self.__call_api__(url, access_token)
        # print(json.dumps(result, ensure_ascii=False, indent=2))

        public_videos = list(filter(lambda x: x["status"]["privacyStatus"] == "public", result["items"]))
        logger.info("original.size={}, public.size={}".format(len(result["items"]), len(public_videos)))

        return list(map(lambda x: VideoInfo(
            title=x["snippet"]["title"],
            details=x["snippet"]["description"],
            time=get_format_time(x["contentDetails"]["duration"]),
            video_id=x["id"],
            thumbnail=x["snippet"]["thumbnails"]["default"]["url"],
            url="https://www.youtube.com/watch?v={}".format(x["id"]),
            publishedAt=x["snippet"]["publishedAt"],
        ), public_videos))


if __name__ == '__main__':
    client = YoutubeApi(
        app_id="584258871565-9lfp2tjva5dn16nbliah3i35bfif6v4l.apps.googleusercontent.com",
        app_secret="GPIZNrWNB-fZNLuEClmTaWul",
        domain="127.0.0.1:8000"
    )

    client.get_profile(
        access_token="ya29.Il-1B55HQNMdpknNI_YmDaUyjcsLB0PG9L9g5BTUNDdFkeqrgk71BqcDF1ko5PMGzaI4h_uigczLJPql0mOAOvGE0QrTz5Pi5KNI3TrVA8uqSmNOA3bO-2H3XGfXk-8quw"
    )
