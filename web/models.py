import os
import uuid
import logging

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy

from web.domain.enums import ConfigKey, Prefectures, Gender, IgMediaType

logger = logging.getLogger("main")


class SystemConfig(models.Model):
    """
    システム設定
    """
    key = models.CharField(max_length=100, choices=ConfigKey.choices(), unique=True)
    value = models.TextField(blank=False)

    class Meta:
        verbose_name = ugettext_lazy("システム設定")
        verbose_name_plural = ugettext_lazy("システム設定")

    @classmethod
    def get_value(cls, key: ConfigKey):
        config = SystemConfig.objects.filter(key=key.name).first()
        value = config.value if config else ""
        return value

    def __str__(self):
        return self.get_key_display()


class ActivityGenre(models.Model):
    """
    活動ジャンル
    """
    name = models.CharField("ジャンル名", max_length=100)
    order = models.IntegerField("順序", default=99)

    class Meta:
        verbose_name = ugettext_lazy("活動ジャンル")
        verbose_name_plural = ugettext_lazy("活動ジャンル")

    def __str__(self):
        return self.name


class InstagramToken(models.Model):
    """
    トークン情報: Instagram
    """
    token = models.CharField("アクセストークン", max_length=400)
    name = models.CharField("ユーザID", max_length=400)
    type = models.CharField("トークンタイプ", max_length=400, blank=True)
    expire = models.IntegerField("有効期限", default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ugettext_lazy("Instagramトークン")
        verbose_name_plural = ugettext_lazy("Instagramトークン")

    def is_valid(self):
        diff = timezone.now() - getattr(self, "updated_at")
        return getattr(self, "expire") > diff.total_seconds() + 10


class TwitterToken(models.Model):
    """
    トークン情報: Twitter
    """
    twitter_id = models.CharField("userId", max_length=100, unique=True)
    twitter_name = models.CharField("displayName", max_length=100)
    token = models.CharField("access_token", max_length=100)
    secret = models.CharField("secret_token", max_length=100)

    class Meta:
        verbose_name = ugettext_lazy("Twitterトークン")
        verbose_name_plural = ugettext_lazy("Twitterトークン")


class YoutubeToken(models.Model):
    """
    トークン情報: Youtube
    """
    user_id = models.CharField("ユーザID", max_length=100, unique=True)
    email = models.CharField("Email", max_length=400)
    user_name = models.CharField("ユーザ名", max_length=400)
    token = models.CharField("アクセストークン", max_length=400)
    refresh = models.CharField("リフレッシュトークン", max_length=400, blank=True)
    type = models.CharField("トークンタイプ", max_length=400, blank=True)
    expire = models.IntegerField("有効期限", default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ugettext_lazy("Youtubeトークン")
        verbose_name_plural = ugettext_lazy("Youtubeトークン")

    def is_valid(self):
        diff = timezone.now() - getattr(self, "updated_at")
        return getattr(self, "expire") > diff.total_seconds() + 10


# 関数を用意すると、ファイル名まで設定できる
def get_file_path(instance, filename):
    _, ext = os.path.splitext(filename)
    name = uuid.uuid4().hex + ext
    return os.path.join("profile", name)


def get_uuid_no_dash():
    return uuid.uuid4().hex


class Account(models.Model):
    """
    アカウント情報
    """
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    display_name = models.CharField("表示名", max_length=100, blank=True)

    profile_image = models.FileField(verbose_name="プロフィール画像", upload_to=get_file_path,
                                     validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', ])],
                                     null=True, blank=True)

    profile_image1 = models.FileField(verbose_name="プロフィール画像", upload_to=get_file_path,
                                     validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', ])],
                                     null=True, blank=True)

    profile_image2 = models.FileField(verbose_name="プロフィール画像", upload_to=get_file_path,
                                     validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', ])],
                                     null=True, blank=True)

    profile_image3 = models.FileField(verbose_name="プロフィール画像", upload_to=get_file_path,
                                     validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', ])],
                                     null=True, blank=True)
    # lang = models.CharField("言語設定", max_length=100, blank=False) # 次期開発
    is_private = models.BooleanField("非公開ページ", default=False)
    work_email = models.EmailField("お仕事連絡用のメールアドレス", null=True, blank=True)
    profile = models.TextField("プロフィール", max_length=400, blank=True)

    # 各SNSの情報
    twitter_comment = models.CharField("Twitterコメント", max_length=400, blank=True)
    instagram_comment = models.CharField("Instagramコメント", max_length=400, blank=True)
    youtube_comment = models.CharField("Youtubeコメント", max_length=400, blank=True)
    twitter_token = models.ForeignKey(TwitterToken, verbose_name="Twitter Token", related_name="twitter_accounts",
                                      null=True, blank=True, on_delete=models.CASCADE)
    instagram_token = models.ForeignKey(InstagramToken, verbose_name="Instagram Token",
                                        related_name="instagram_accounts",
                                        null=True, blank=True, on_delete=models.CASCADE)
    youtube_token = models.ForeignKey(YoutubeToken, verbose_name="Youtube Token", related_name="youtube_accounts",
                                      null=True, blank=True, on_delete=models.CASCADE)

    # 非公開情報
    prefecture = models.CharField("都道府県", max_length=100, choices=Prefectures.choices(), null=True, blank=True)
    active_place = models.CharField("活動エリア", max_length=400, blank=True)
    wikipidia_desc = models.CharField("活動エリア", max_length=400, blank=True)
    birth_place = models.CharField("出身地", max_length=400, blank=True)
    height = models.CharField("身長", max_length=100, blank=True)
    activity_genres = models.ManyToManyField(ActivityGenre, verbose_name="活動ジャンル", related_name="accounts", blank=True)
    birth_day = models.DateField("誕生日", null=True, blank=True)

    gender = models.CharField("性別", max_length=10, choices=Gender.choices(), blank=True)

    pr = models.TextField("PR", blank=True)

    # 設定
    ssp_landscape = models.TextField("SSP(縦長)", null=True, blank=True)
    ssp_post = models.TextField("SSP(投稿)", null=True, blank=True)
    page_id = models.CharField("登録者ページID", max_length=100, editable=False, default=get_uuid_no_dash)
    parent_id = models.CharField("親の登録者ID", max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ugettext_lazy("アカウント")
        verbose_name_plural = ugettext_lazy("アカウント")

    def __str__(self):
        return self.display_name


@receiver(models.signals.post_delete, sender=Account)
def _delete_user(sender, instance, *args, **kwargs):
    logger.info("delete user: account_id={}, user_id={}".format(instance.id, instance.user.id))
    instance.user.delete()


class InstagramInfo(models.Model):
    """
    InstagramのMedia情報
    """
    info_id = models.CharField("INFO_ID", max_length=100)
    url = models.CharField("URL", max_length=400)
    type = models.CharField("Type", choices=IgMediaType.choices(), max_length=100)
    thumbnail = models.CharField("サムネイル", max_length=400, blank=True)
    publish_at = models.DateTimeField("公開日", blank=True, null=True)
    user = models.ForeignKey(User, related_name="instagram_list", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ugettext_lazy("InstagramのMedia情報")
        verbose_name_plural = ugettext_lazy("InstagramのMedia情報")

    def __str__(self):
        return "{}(id:{})".format(self.info_id, self.id)


class YoutubeInfo(models.Model):
    """
    YoutubeのMedia情報
    """
    info_id = models.CharField("ID", max_length=100)
    chanel_id = models.CharField("チャネルID", max_length=100)
    url = models.CharField("URL", max_length=400)
    thumbnail = models.CharField("サムネイル", max_length=400, blank=True)
    time = models.CharField("再生時間", max_length=50, blank=True)
    title = models.CharField("タイトル", max_length=400, blank=True)
    details = models.TextField("説明文", blank=True)
    publish_at = models.DateTimeField("公開日", blank=True, null=True)
    user = models.ForeignKey(User, related_name="youtube_list", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ugettext_lazy("YoutubeのMedia情報")
        verbose_name_plural = ugettext_lazy("YoutubeのMedia情報")

    def __str__(self):
        return "{}(id:{})".format(self.info_id, self.id)
