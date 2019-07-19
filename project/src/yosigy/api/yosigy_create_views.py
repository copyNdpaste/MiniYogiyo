import json
from json.decoder import JSONDecodeError
import datetime
from http import HTTPStatus
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin
from menu.models import Menu
from yosigy.forms import YosigyForm, YosigyMenuForm
from yosigy.models import YosigyMenu
from restaurant.models import Restaurant, RestaurantTimeline
from timeline.models import TimelineStatus, TimelineType


class YosigyMenuListAPIView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        restaurant_id = self.kwargs['restaurant_id']

        menus = (Menu.objects.filter(
            restaurant_id=restaurant_id,
            restaurant__store_owner=request.user).values())

        if not menus:
            data = {
                'error': '선택할 수 있는 메뉴가 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        data = {
            'menus': list(menus)
        }
        return JsonResponse(data, status=HTTPStatus.OK)


class YosigyCreateAPIView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        restaurants = (
            Restaurant.objects.distinct()
            .select_related('yosigy')
            .filter(
               Q(store_owner=request.user) & (Q(yosigy=None) | Q(yosigy__deadline__lte=datetime.datetime.now()))
            )
            .order_by(
                'name'
            ).values('id', 'name', 'title'))

        if not restaurants:
            data = {
                'error': '공고를 올릴 수 있는 restaurant가 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        data = {
            'restaurants': list(restaurants)
        }
        return JsonResponse(data, status=HTTPStatus.OK)

    def post(self, request, *args, **kwargs):
        try:
            post_data = json.loads(request.body)
            post_data['user'] = request.user.id
            restaurant_id = post_data['restaurant']
            menu_list = post_data['menus']

            restaurant_obj = Restaurant.objects.filter(id=restaurant_id)
            restaurant_menus = [menu['menu'] for menu in list(restaurant_obj.values('menu'))]

            menu_ids = []
            bulk_menus = []
            for menu in menu_list:
                yosigy_menu_form = YosigyMenuForm(menu)
                if not yosigy_menu_form.is_valid():
                    data = {
                        'error': yosigy_menu_form.errors,
                        'message': '요식이 식권 이벤트 생성을 실패 하였습니다.'
                    }
                    return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

                menu_ids.append(int(menu['id']))

                yosigy_menu = YosigyMenu()
                yosigy_menu.discounted_price = menu['discounted_price']
                yosigy_menu.menu_id = menu['id']
                bulk_menus.append(yosigy_menu)

        except (KeyError, ValueError, JSONDecodeError):
            data = {
                'error': '잘못된 요청 입니다.'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        menu_ids_set = set(menu_ids)
        restaurant_menus_set = set(restaurant_menus)
        if not menu_ids_set:
            data = {
                'error': '메뉴를 한개 이상 선택해야합니다.'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        elif list(menu_ids_set - (menu_ids_set & restaurant_menus_set)):
            data = {
                'error': '메뉴정보가 잘못되었습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        yosigy_form = YosigyForm(post_data)

        if not yosigy_form.is_valid():
            data = {
                'error': yosigy_form.errors,
                'message': '요식이 식권 이벤트 생성을 실패 하였습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        yosigy_obj = yosigy_form.save()

        for yosigy_menu in bulk_menus:
            yosigy_menu.yosigy = yosigy_obj

        YosigyMenu.objects.bulk_create(bulk_menus)
        restaurant_obj.update(is_yosigy=True)
        timeline_field = {
            'restaurant': yosigy_obj.restaurant,
            'yosigy': yosigy_obj,
            'status': TimelineStatus.CREATE,
            'timeline_type': TimelineType.YOSIGY_EVENT,
            'changed_field': '요식이 식권 이벤트',
        }
        RestaurantTimeline.objects.create(**timeline_field)

        data = {
            'yosigy_id': yosigy_obj.id,
            'message': '게시물 작성을 성공하였습니다.'
        }
        return JsonResponse(data, status=HTTPStatus.CREATED)
