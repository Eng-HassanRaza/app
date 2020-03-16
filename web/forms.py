from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, ChoiceField, RadioSelect

from web.domain.enums import Gender
from web.models import Account, ActivityGenre


class AccountForm(ModelForm):
    activity_genres = ModelMultipleChoiceField(
        queryset=ActivityGenre.objects.order_by("order", "id"),
        widget=CheckboxSelectMultiple,
        required=False
    )

    gender = ChoiceField(
        choices=Gender.choices(),
        widget=RadioSelect,
        required=False
    )

    class Meta:
        model = Account
        fields = [
            'display_name',
            "profile_image",
            "profile_image1",
            "profile_image2",
            "profile_image3",
            'is_private',
            'work_email',
            "profile",
            "twitter_comment",
            "instagram_comment",
            "youtube_comment",
            "prefecture",
            "active_place",
            "birth_place",
            "height",
            "activity_genres",
            "birth_day",
            "gender",
            "pr",
            "wikipidia_desc",
            "others1_name",
            "others1",
            "others1_comment",
            "others2_name",
            "others2",
            "others2_comment",
            "others3_name",
            "others3",
            "others3_comment",
            "others4_name",
            "others4",
            "others4_comment",
            "others5_name",
            "others5",
            "others5_comment",
        ]
