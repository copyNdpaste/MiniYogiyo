from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path(
        '',
        views.very_simple_json_response
    ),
    path(
        'http_response/',
        views.use_http_response_for_json
    ),
    path(
        'cbv1/',
        views.JsonCBV1.as_view(),
    ),
    path(
        'cbv2/',
        views.JsonCBV2.as_view(),
    ),
    path(
        'serialized_detail/',
        views.SerializedDetailView.as_view(),
    ),
    path(
        'serialized_list/',
        views.SerializedListView.as_view(),
    )




]
