from enum import Enum


class Choosable(str, Enum):
    @classmethod
    def choices(cls):
        return [(m.name, m.value) for m in cls]


class ConfigKey(Choosable):
    """
    システム設定のKEY
    """
    KEY_SSP_LANDSCAPE = "広告タグ: 横長"
    KEY_SSP_POST = "広告タグ: 投稿"
    KEY_SSP_GA_TAG = "GAタグ"
    KEY_OGP_IMAGE_URL = "OGP画像URL"


class Gender(Choosable):
    """
    性別
    """
    MALE = "男"
    FEMALE = "女"
    OTHER = "その他"


class Prefectures(Choosable):
    """
    都道府県のKEY
    """
    HOKKAIDO = "北海道"
    AOMORI = "青森"
    IWATE = "岩手"
    MIYAGI = "宮城"
    AKITA = "秋田"
    YAMAGATA = "山形"
    FUKUSHIMA = "福島"
    IBARAKI = "茨城"
    TOCHIGI = "栃木"
    GUNMA = "群馬"
    SAITAMA = "埼玉"
    CHIBA = "千葉"
    TOKYO = "東京都"
    KANAGAWA = "神奈川"
    NIIGATA = "新潟"
    TOYAMA = "富山"
    ISHIKAWA = "石川"
    FUKUI = "福井"
    YAMANASHI = "山梨"
    NAGANO = "長野"
    GIFU = "岐阜"
    SHIZUOKA = "静岡"
    AICHI = "愛知"
    MIE = "三重"
    SHIGA = "滋賀"
    KYOTO = "京都"
    OSAKA = "大阪"
    HYOGO = "兵庫"
    NARAA = "奈良"
    WAKAYAMA = "和歌山"
    TOTTORI = "鳥取"
    SHIMANE = "島根"
    OKAYAMA = "岡山"
    HIROSHIMA = "広島"
    YAMAGUCHI = "山口"
    TOKUSHIMA = "徳島"
    KAGAWA = "香川"
    EHIME = "愛媛"
    KOCHI = "高知"
    FUKUOKA = "福岡"
    SAGA = "佐賀"
    NAGASAKI = "長崎"
    KUMAMOTO = "熊本"
    OITA = "大分"
    MIYAZAKI = "宮崎"
    KAGOSHIMA = "鹿児島"
    OKINAWA = "沖縄"
    # OTHER = "その他"
    OVER_SEAS = "海外"


class IgMediaType(Choosable):
    """
    InstagramのMediaType
    """
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    CAROUSEL_ALBUM = "CAROUSEL_ALBUM"

    @classmethod
    def value_of(cls, target_value):
        for e in IgMediaType:
            if e.value == target_value:
                return e
        raise ValueError('{} is invalid'.format(target_value))
