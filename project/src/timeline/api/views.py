import datetime
import json
from http import HTTPStatus

from django.db.models import Count, F, Q, Prefetch
from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from accounts.mixins import LoginRequiredMixin
from menu.models import Menu
from django.core.serializers.json import DjangoJSONEncoder
from restaurant.models import RestaurantTimeline
from timeline.models import TYPE_CHOICES, STATUS_CHOICES, RestaurantTimelineComment
from timeline.api.utils import SortedBasedValue


class RestaurantTimelineListApi(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        subscribed_restaurants = user.subscribed_restaurants.values('id')
        liked_restaurant_timeline = [timeline['id'] for timeline in list(user.restauranttimeline_set.values('id'))]

        if not subscribed_restaurants:
            data = {
                'error': '구독중인 restaurant가 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        subscribed_restaurants_ids = [restaurant['id'] for restaurant in subscribed_restaurants]

        timeline_qs = (
            RestaurantTimeline.objects
            .select_related('restaurant', 'yosigy')
            .prefetch_related('like',
                              Prefetch('restauranttimelinecomment_set',
                                       queryset=(
                                           RestaurantTimelineComment.objects
                                           .select_related('restaurant_timeline')
                                           .filter(is_active=True)
                                                )
                                       )
                              )
            .filter(
                Q(restaurant_id__in=subscribed_restaurants_ids) &
                (~Q(restauranttimelinecomment__id=None) |
                    Q(restauranttimelinecomment=None))).order_by('-created_time')
            .annotate(
                comment=Count('restauranttimelinecomment'),
                yosigy_deadline=F('yosigy__deadline')
            )
        )

        timeline_list = [
            {'restaurant_id': timeline.restaurant.id,
             'restaurant_timeline_id': timeline.id,
             'restaurant_name': timeline.restaurant.name,
             'restaurant_title': timeline.restaurant.title,
             'restaurant_img': str(timeline.restaurant.img),
             'min_price': timeline.restaurant.min_order_price,
             'delivery_charge': timeline.restaurant.delivery_charge,
             'created_time': timeline.created_time,
             'updated_time': timeline.updated_time,
             'post_img': str(timeline.changed_img),
             'prior_info': timeline.prior_info,
             'post_info': (timeline.yosigy.notice
                           if timeline.yosigy_id is not None else timeline.post_info+timeline.changed_data),
             'timeline_type': timeline.timeline_type,
             'timeline_type_name': dict(TYPE_CHOICES)[timeline.timeline_type],
             'changed_item': timeline.changed_field,
             'status': dict(STATUS_CHOICES)[timeline.status],
             'like': (True if timeline.id in liked_restaurant_timeline else False),
             'like_count': timeline.like.count(),
             'comment_count': timeline.restauranttimelinecomment_set.count(),
             'yosigy_id': timeline.yosigy_id,
             'yosidy_deadline': timeline.yosigy_deadline}
            for timeline in timeline_qs]

        if not timeline_list:
            data = {
                'error': '업데이트 된 정보가 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        return HttpResponse(content=json.dumps(timeline_list, cls=DjangoJSONEncoder), status=HTTPStatus.OK,
                            content_type='application/json')
      
      
class PopularMenu(LoginRequiredMixin, View):
    def get(self, request, sort_based_value, *args, **kwargs):
        """
        인기메뉴를 조회수, 좋아요 개수, 메뉴 점수가 높은 순으로 보여주는 API
        """
        user = request.user
        last_created_cart = (
            user.cart_set
                .order_by('-created_time')
                .values_list('id', flat=True)[0]
        )
        try:
            popular_menu_top_ten_obj_queryset = (
                Menu.objects
                    .select_related('restaurant')
                    .annotate(like_count=Count('like'))
                    .order_by(SortedBasedValue.from_str(sort_based_value).value)[:10]
            )
        except AttributeError:
            return JsonResponse(
                status=HTTPStatus.NOT_FOUND,
                data={'message': '파라미터 값이 올바르지 않습니다.'}
            )

        menu_json_list = [
            {
                'rank': ('0' + str(index + 1)
                         if (index + 1) < 10
                         else index + 1
                         ),
                'id': menu.id,
                'img': menu.img.url,
                'name': menu.name,
                'price': menu.price,
                'hit': menu.hit,
                'score': menu.score,
                'like_count': menu.like_count,
                'restaurant_img': menu.restaurant.img.url,
                'restaurant_title': menu.restaurant.title,
                'cart_id': last_created_cart
            }
            for index, menu in enumerate(popular_menu_top_ten_obj_queryset)
        ]

        json_data = {
            'menu': menu_json_list
        }

        return JsonResponse(
            status=HTTPStatus.OK,
            data=json_data
        )
