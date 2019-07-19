from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.generic import View

from ..models import Category
import json


class CategoryListAPIView(View):
    def get(self, request, *args, **kwargs):
        category_list = Category.objects.all().values('pk', 'name', 'img')
        if request.user.is_authenticated:
            json_data = {
                'category_list': list(category_list),
                'user_addr': request.user.address,
            }
        else:
            json_data = {
                'category_list': list(category_list),
            }
        return HttpResponse(
            json.dumps(json_data),
            content_type='application/json'
        )
