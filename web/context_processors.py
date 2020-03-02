from web.domain.enums import ConfigKey
from web.models import SystemConfig


def settings(request):
    return {
        "GA_TAG": SystemConfig.get_value(ConfigKey.KEY_SSP_GA_TAG),
        "SSP_TAG_LAND": SystemConfig.get_value(ConfigKey.KEY_SSP_LANDSCAPE),
        "SSP_TAG_POST": SystemConfig.get_value(ConfigKey.KEY_SSP_POST),
        "OGP_URL": SystemConfig.get_value(ConfigKey.KEY_OGP_IMAGE_URL),
        "RES_VER": "?v=1115"
    }
