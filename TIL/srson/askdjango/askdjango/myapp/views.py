import os
from django.http import HttpResponse, JsonResponse
from django.conf import settings


# Create your views here.
# FBV 함수 기반 뷰
# json 응답
def json_post_list(request):
    'FBV: JSON 형식 응답하기'

    json_data = {
        'message': '안녕, 파이썬&장고',
        'items': ['파이썬', '장고', 'Celery', 'Azure', 'AWS'],
    }
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


# excel다운로드 # 해결안됨
def download_excel(request):
    'FBV: 엑셀 다운로드 응답하기'

    filepath = os.path.join(
        settings.BASE_DIR, 'myapp', 'static', 'myapp/Money.xls')
    filename = os.path.basename(filepath)

    with open(filepath, 'rb') as f:  # binary mode로 읽음
        response = HttpResponse(f, content_type="application/vnd.ms-excel")
        # 필요한 응답헤더 세팅
        response['Content-Disposition'] = 'attachment; filename="{}"'.\
            format(filename)
        return response
