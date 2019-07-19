from django.urls import path
from timeline.api import bestmenu_views, views
from timeline.api import menu_timeline_views
from timeline.api import restaurant_timeline_detail_views, menu_timeline_detail_views

app_name = "timeline_api"

urlpatterns = [
    path(
        'bestmenu/',
        bestmenu_views.BestSellingAPIView.as_view(),
        name='bestmenu'
    ),
    path(
        'restaurant/',
        views.RestaurantTimelineListApi.as_view(),
        name='restaurant'
    ),
    path(
        'menutimeline/',
        menu_timeline_views.MenuTimeLineAPIView.as_view(),
        name='menutimeline'
    ),
    path(
        'popularmenu/<str:sort_based_value>/',
        views.PopularMenu.as_view(),
        name='popularmenu'
    ),
    path(
        'restaurant/<int:restaurant_timeline_id>/like/',
        restaurant_timeline_detail_views.RestaurantTimelineLikeAPI.as_view(),
        name='restaurant_like'
    ),
    path(
        'restaurant/<int:restaurant_timeline_id>/comment/',
        restaurant_timeline_detail_views.RestaurantTimelineCommentListAPI.as_view(),
        name='restaurant_comment_list'
    ),
    path(
        'restaurant/<int:restaurant_timeline_id>/comment/<int:comment_id>/',
        restaurant_timeline_detail_views.RestaurantTimelineCommentAPI.as_view(),
        name='restaurant_comment'
    ),
    path(
        'menutimeline/<int:menu_timeline_id>/like/',
        menu_timeline_detail_views.MenuTimelineLikeAPI.as_view(),
        name='menu_like'
    ),
    path(
        'menutimeline/<int:menu_timeline_id>/comment/',
        menu_timeline_detail_views.MenuTimelineCommentListAPI.as_view(),
        name='menu_comment_list'
    ),
    path(
        'menutimeline/<int:menu_timeline_id>/comment/<int:comment_id>/',
        menu_timeline_detail_views.MenuTimelineCommentAPI.as_view(),
        name='menu_comment'
    ),
]
