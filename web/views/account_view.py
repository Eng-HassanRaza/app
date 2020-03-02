from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def account(request):
    if request.user.is_authenticated:
        """アカウントメニュー: ログイン後"""
        return render(request, 'account.html')
    else:
        """アカウントメニュー: ログイン前"""
        return render(request, 'account2.html')
