from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):

    # render는 첫번째 인수로 요청을 지정, 두번 째 인수로 렌더링할 템플릿 명을 지정한다.
    # 앱 폴더 내에 있는 templates라는 폴더를 자동으로 검색한다.
    # templates 컨텐츠를 기반으로 HttpResponse를 만들어 준다.
    return render(request, 'home.html')
