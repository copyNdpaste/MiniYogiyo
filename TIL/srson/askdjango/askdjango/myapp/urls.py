from django.urls import path
from . import views
from . import views_cbv

app_name = 'myapp'
urlpatterns = [
    # FBV urls
    path('list/', views.json_post_list),
    path('excel/', views.download_excel),
    # CBV urls
    path('cbv/list1/', views_cbv.post_list1),
    path('cbv/list2/', views_cbv.post_list2),
    path('cbv/excel/', views_cbv.download_excel),
]
