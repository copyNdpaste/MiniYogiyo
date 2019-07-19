import os
from django.views.generic import TemplateView, View
from django.http import JsonResponse, HttpResponse
from django.conf import settings


# CBV 클래스 기반 뷰
class PostListView(TemplateView):
    template_name = 'myapp/post_list.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['name'] = '공유'
        return context


post_list1 = PostListView.as_view()


class JsonPostListView(View):
    'CBV: JSON 형식 응답하기'

    def get(self, request):
        return JsonResponse(
            self.get_json_data(),
            json_dumps_params={'ensure_ascii': False})

    def get_json_data(self):
        json_data = {
            'message': '안녕! 파이썬&장고',
            'items': ['python', 'django', 'Celery', 'Azure', 'AWS'],
        }
        return json_data


post_list2 = JsonPostListView.as_view()


class ExcelDownloadView(View):
    'CBV 엑셀 다운로드 응답하기'

    filepath = os.path.join(
        settings.BASE_DIR, 'myapp', 'static', 'myapp/Money.xls')

    def get(self, request):
        filename = os.path.basename(self.filepath)
        with open(self.filepath, 'rb') as f:
            response = HttpResponse(f, content_type='application/vnd.ms-excel')
            # 필요한 응답 헤더 세팅
            response['Content-Disposition'] = 'attachment; filename="{}"'.\
                format(filename)
            return response


download_excel = ExcelDownloadView.as_view()
