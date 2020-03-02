from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def ask(request):
    """お問い合わせ"""
    return render(request, 'new_ask.html')


@require_GET
def company(request):
    """運営会社"""
    return render(request, 'new_company.html')


@require_GET
def manage(request):
    """報酬管理"""
    return render(request, 'manage.html')


@require_GET
def tos(request):
    """利用規約"""
    return render(request, 'new_kiyaku.html')


@require_GET
def policy(request):
    """プライバシーポリシー"""
    return render(request, 'new_privacypolicy.html')


@require_GET
def about(request):
    """ABOUT"""
    return render(request, 'about.html')
def about_verification(request):
    """ABOUT VERIFICATION"""
    context = {'name':request.POST['ab_name'],'email':request.POST['ab_email'],'desc':request.POST['ab_desc']}
    return render(request, 'new_verification.html',context=context)

def thanks_contact(request):
    return render(request, 'about_us_thank.html')
@require_GET
def coming_soon(request):
    """coming soon"""
    return render(request, 'comingsoon.html')
