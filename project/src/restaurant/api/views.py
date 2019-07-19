import enum
import json
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from accounts.mixins import LoginRequiredMixin
from restaurant.models import Restaurant

User = get_user_model()


class CategoryNum(enum.IntEnum):
    ALL_ID = 3


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.strftime('%H:%M')


class RestaurantListAPIView(View):
    def get(self, request, *args, **kwargs):
        category_id = self.kwargs['category_id']
        if category_id == CategoryNum.ALL_ID:
            restaurant_list = Restaurant.objects.all().values(
                'pk', 'title', 'min_order_price', 'estimated_delivery_time', 'img',
            )
        else:
            restaurant_list = Restaurant.objects.filter(category=category_id).values(
                'pk', 'title', 'min_order_price', 'estimated_delivery_time', 'img',
            )
        if not restaurant_list:
            return HttpResponse(
                json.dumps({"message": "레스토랑 리스트가 존재하지 않습니다.", }),
                status=HTTPStatus.NOT_FOUND,
                content_type='application/json',
            )
        restaurant_list = list(restaurant_list, )
        json_data = {
            'restaurant_list': restaurant_list,
            'category_id': category_id,
        }
        json_data = json.dumps(json_data, cls=DateTimeEncoder)

        return HttpResponse(
            json_data,
            content_type='application/json',
        )


class RestaurantDetailAPIView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        restaurant_id = self.kwargs['restaurant_id']
        try:
            restaurant_detail = Restaurant.objects.filter(id=restaurant_id).values(
                'name', 'img', 'min_order_price', 'order_way', 'owner', 'title', 'operation_start_hour',
                'operation_end_hour',
                'tel', 'origin', 'delivery_charge', 'info', 'estimated_delivery_time',
            )

            if not restaurant_detail:
                return HttpResponse(
                    json.dumps({"message": "해당 레스토랑이 없습니다.", }),
                    status=HTTPStatus.NOT_FOUND,
                    content_type='application/json',
                )

            restaurant_detail= json.dumps(list(restaurant_detail, ), cls=DateTimeEncoder)

            if request.user.is_authenticated:
                if user.subscribed_restaurants.filter(pk=restaurant_id):
                    subscribe_flag = False
                    json_data = {
                        'restaurant_detail': restaurant_detail,
                        'user_addr': request.user.address,
                        'subscribe_flag': subscribe_flag,
                    }
                else:
                    subscribe_flag = True
                    json_data = {
                        'restaurant_detail': restaurant_detail,
                        'user_addr': request.user.address,
                        'subscribe_flag': subscribe_flag,
                    }
            else:
                json_data = {
                    'restaurant_detail': restaurant_detail,
                }

            return HttpResponse(
                json.dumps(json_data),
                content_type='application/json',
            )
        except Restaurant.DoesNotExist:
            json_data = {
                "message": "레스토랑이 없습니다.",
            }
            return JsonResponse(
                json_data,
                status=HTTPStatus.BAD_REQUEST,
            )



class RestaurantSubscribeCreateAPIView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        restaurant_id = self.kwargs['restaurant_id']
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            if user.subscribed_restaurants.filter(pk=restaurant_id):
                user.subscribed_restaurants.remove(restaurant)
                json_data = {
                    "message": "구독 취소",
                    "subscribe_flag": True,
                }
                return JsonResponse(
                    json_data,
                )
            else:
                user.subscribed_restaurants.add(restaurant)
                user.save()
                json_data = {
                    "message": "구독 성공",
                    "subscribe_flag": False,
                }
                return JsonResponse(
                    json_data,
                )
        except:
            json_data = {
                "message": "구독할 레스토랑이 없습니다.",
            }
            return JsonResponse(
                json_data,
                status=HTTPStatus.BAD_REQUEST,
            )


class SubscribedRestaurantsAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        subscribed_restaurants = Restaurant.objects.filter(subscribers=request.user).values(
            'name', 'img', 'category', 'pk', 'title')
        if subscribed_restaurants:
            json_data = {
                "subscribed_restaurants": list(subscribed_restaurants),
            }
        else:
            json_data = {
                "message": "구독 중인 레스토랑이 없습니다.",
            }
        return JsonResponse(
            json_data,
            status=HTTPStatus.OK,
        )
