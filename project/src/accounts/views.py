from django.shortcuts import render


def top_view(request):
    return render(request, 'common/base.html')


def my_page(request):
    tab_num = request.GET.get('tab')
    if not tab_num:
        tab_num = 0
    return render(request, 'accounts/mypage.html', {'tab_num': tab_num})
