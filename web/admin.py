from django.contrib import admin
# Register your models here.
from import_export import resources
from import_export.admin import ExportMixin
from import_export.formats import base_formats

from web.models import SystemConfig, ActivityGenre, Account, InstagramToken, TwitterToken, YoutubeToken, InstagramInfo, \
    YoutubeInfo


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('key', 'value')


@admin.register(ActivityGenre)
class ActivityGenreAdmin(admin.ModelAdmin):
    ordering = ['order', 'id']
    list_display = ('order', 'id', 'name',)


@admin.register(InstagramToken)
class InstagramTokenAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'token', "name", "type", "expire")


@admin.register(TwitterToken)
class TwitterTokenAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'twitter_id', "twitter_name", "token", "secret")


@admin.register(YoutubeToken)
class YoutubeTokenAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'user_id', 'email', 'user_name', "token", "refresh",)


@admin.register(InstagramInfo)
class InstagramInfoAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('id', 'info_id', 'url', "type", "thumbnail", "publish_at", "user")
    search_fields = [
        'info_id',
        "type",
        "url",
    ]


@admin.register(YoutubeInfo)
class YoutubeInfoAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('id', 'info_id', "chanel_id", "title", "details", 'url', "thumbnail", "time", "publish_at", "user")
    search_fields = [
        'info_id',
        "chanel_id",
        "title",
        "url",
    ]


class AccountResource(resources.ModelResource):
    class Meta:
        model = Account
        fields = (
            'id',
            'display_name',
            'prefecture',
            "birth_place",
            "height",
            "birth_day",
            "page_id",
            "parent_id",
            "activity_genres",
            "is_private",
            "work_email",
            "profile",
            "gender",
            "pr",
            "created_at",
            "updated_at"
        )

    def dehydrate_prefecture(self, obj):
        return obj.get_prefecture_display() if obj.prefecture is not None else ""

    def dehydrate_gender(self, obj):
        return obj.get_gender_display() if obj.gender is not None else ""

    def dehydrate_activity_genres(self, obj):
        activity_names = list(map(lambda x: x.name, list(obj.activity_genres.all())))
        return ",".join(activity_names)

    def dehydrate_is_private(self, obj):
        return "非公開" if obj.is_private is not None or obj.is_private else "公開"


@admin.register(Account)
class AccountAdmin(ExportMixin, admin.ModelAdmin):
    ordering = ['id']
    list_display = (
        'id', 'display_name', "prefecture", "birth_place", "height", "birth_day", "page_id", "parent_id", "user")
    search_fields = [
        'display_name',
        "page_id",
        "prefecture",
        "birth_place",
        "height",
        "birth_day",
        "activity_genres__name"
    ]
    list_filter = ('prefecture', "activity_genres__name", "gender")

    # django-import-exports
    resource_class = AccountResource
    formats = [base_formats.CSV]
