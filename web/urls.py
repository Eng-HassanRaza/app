"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import LogoutView
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from web.views import index_view, misc_view, auth_view, profile_view, account_view, auth_instagram_view, \
    auth_twitter_view, auth_youtube_view

app_name = 'web'
urlpatterns = [
    path('', index_view.index, name="index"),
    path('api/users', index_view.more_users, name="more_users"),

    # auth
    path('login/', auth_view.login, name="login"),
    path('signup/', auth_view.signup, name="signup"),
    path('leave/', auth_view.leave, name="leave"),
    path('thanks/', auth_view.thanks, name="thanks"),
    path('invite/<str:parent_id>/', auth_view.invite, name="invite"),
    path('logout/', LogoutView.as_view(), name="logout"),

    # profile
    path('profile/edit/', profile_view.profile, name="profile"),
    path('profile/<int:account_id>/', profile_view.profile_long, name="profile_long"),
    path('profile/<int:account_id>/ig/', profile_view.profile_ig, name="profile_long_ig"),
    path('profile/<int:account_id>/insta/', profile_view.instagram_list, name="profile_long_insta"),
    path('profile/<int:account_id>/twitter/', profile_view.twitter_list, name="profile_long_twitter"),
    path('profile/<int:account_id>/youtube/', profile_view.youtube_list, name="profile_long_youtube"),
    path('profile/<int:account_id>/yt/', profile_view.profile_yt, name="profile_long_yt"),

    # account
    path('account/', account_view.account, name="account"),

    # misc
    path('ask/', misc_view.ask, name="ask"),
    path('company/', misc_view.company, name="company"),
    path('manage/', misc_view.manage, name="manage"),
    path('tos/', misc_view.tos, name="tos"),
    path('policy/', misc_view.policy, name="policy"),
    path('about/', misc_view.about, name="about"),
    path('about_verification/', misc_view.about_verification, name="about_verification"),
    path('about_us_thanks/', misc_view.thanks_contact, name="thanks_contact"),
    path('articlelist/', misc_view.coming_soon, name="articlelist"),

    # oauth ig
    path('auth/ig/login/', auth_instagram_view.login, name="ig_login"),
    path('auth/ig/logout/', auth_instagram_view.logout, name="ig_logout"),
    path('auth/ig/login/callback/', auth_instagram_view.callback, name="ig_login_callback"),
    path('auth/ig/callback/', auth_instagram_view.callback, name="ig_callback"),

    # oauth tw
    path('auth/tw/login/', auth_twitter_view.login, name="tw_login"),
    path('auth/tw/logout/', auth_twitter_view.logout, name="tw_logout"),
    path('auth/tw/login/callback/', auth_twitter_view.callback, name="tw_login_callback"),

    # oauth yt
    path('auth/yt/login/', auth_youtube_view.login, name="yt_login"),
    path('auth/yt/logout/', auth_youtube_view.logout, name="yt_logout"),
    path('auth/yt/login/callback/', auth_youtube_view.callback, name="yt_login_callback"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,
document_root=settings.STATIC_ROOT)
