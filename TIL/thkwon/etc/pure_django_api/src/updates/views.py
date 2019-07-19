import json

from django.core.serializers import serialize
from django.http import (

    JsonResponse,
    HttpResponse
)
from django.views.generic import View

from config.mixins import JsonResponseMixin
from .models import Update


class SerializedDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = Update.objects.get(id=1)
        json_data = obj.serialize()
        return HttpResponse(
            json_data,
            content_type='application/json'
        )


class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        qs = Update.objects.all()
        json_data = qs.serialize()
        return HttpResponse(
            json_data,
            content_type='application/json'
        )


class JsonCBV1(View):
    def get(self, request, *args, **kwargs):
        data = {
            "count": 1000,
            "content": "CBV without mixin"
        }
        return JsonResponse(data)


class JsonCBV2(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            "count": 1000,
            "content": "CBV with mixin"
        }
        return self.render_to_json_response(data)


def very_simple_json_response(request):
    data = {
        "count": 1000,
        "content": "Some new content"
    }
    return JsonResponse(data)


def use_http_response_for_json(request):
    data = {
        "count": 1000,
        "content": "Http response for json"
    }
    json_data = json.dumps(data)
    return HttpResponse(
        json_data,
        content_type='application/json'
    )


