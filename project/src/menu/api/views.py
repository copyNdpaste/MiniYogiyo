import enum
import json
import operator
import random
from datetime import datetime
from http import HTTPStatus

from django.db.models import F, Q, Sum
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from accounts.mixins import LoginRequiredMixin
from accounts.models import Taste
from cart.models import Cart
from menu.models import Menu
from menu.helpers import get_dong, get_x_y_grid, get_user_dong_weather, get_restaurants
from order.models import Order, DeliveryStatus, PaymentStatus

ONE_RANDOM_MENU_COUNT = settings.ONE_RANDOM_MENU_COUNT
LOCALHOST = settings.LOCALHOST


class CategoryNum(enum.IntEnum):
    WEATHER_ID = 15


class WeatherNum(enum.IntEnum):
    SUNNY = 1
    PARTLY_CLOUDY = 2
    CLOUDY = 3
    BLUR = 4


class Month(enum.IntEnum):
    one_month = 1
    two_month = 2
    three_month = 3


class Weight(enum.auto):
    one_month_ago_weight = 0.8
    two_month_ago_weight = 0.6


class MenuListAPIView(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs['category_id']
        weather_list = [WeatherNum.SUNNY, WeatherNum.PARTLY_CLOUDY,
                        WeatherNum.CLOUDY, WeatherNum.BLUR, ]
        count_duplicated_weather_order = {}
        menu_quantity_to_exclude_or_not = {}
        excluded_menu_count = {}
        excluded_menu_quantity = {}
        this_month = datetime.now().month

        if category_id != CategoryNum.WEATHER_ID:
            return get_restaurants(**kwargs)

        elif category_id == CategoryNum.WEATHER_ID:
            category_id = kwargs['category_id']
            if request.user.is_anonymous:
                return JsonResponse(
                    {
                        "message": "로그인되어 있지 않습니다.",
                    },
                    status=HTTPStatus.UNAUTHORIZED,
                )

            if not request.user.address:
                return JsonResponse(
                    {
                        "message": "사용자 주소가 존재하지 않습니다.",
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )

            user_dong = get_dong(request.user.address)

            if user_dong is None:
                return JsonResponse(
                    {'message': 'mypage에서 주소의 동을 입력하세요.'},
                    status=HTTPStatus.BAD_REQUEST
                )

            x_y_grid = get_x_y_grid(user_dong)
            try:
                x = x_y_grid.x
                y = x_y_grid.y
            except:
                return x_y_grid

            user_dong_weather = get_user_dong_weather(x, y)

            if type(user_dong_weather) != int:
                return user_dong_weather

            for weather in weather_list:
                menu_list = (Cart.objects
                             .prefetch_related('order')
                             .filter(order__address__contains=user_dong, order__weather=weather.value, order__created_time__month__gt=this_month - Month.three_month)
                             .exclude(cartitem__menu__isnull=True)
                             .values('cartitem__menu__name')
                             .annotate(menu_quantity=Sum('cartitem__quantity'), menu=F('cartitem__menu__name'))
                             .order_by('-menu_quantity')[:5]
                             .values('menu', quantity=F('menu_quantity'),
                                     price=F('cartitem__menu__price'), img=F('cartitem__menu__img'),
                                     id=F('cartitem__menu__id'), detail=F('cartitem__menu__detail'),
                                     restaurant=F(
                                         'cartitem__menu__restaurant__id'),
                                     )
                             )
                for menu in menu_list:
                    if count_duplicated_weather_order.get(menu['menu']):
                        count_duplicated_weather_order[menu['menu']] += 1
                        menu_quantity_to_exclude_or_not[menu['menu']] += menu['quantity']
                    else:
                        count_duplicated_weather_order[menu['menu']] = 1
                        menu_quantity_to_exclude_or_not[menu['menu']] = menu['quantity']

            try:
                for menu_name, menu_cnt in count_duplicated_weather_order.items():
                    if menu_cnt >= 4:
                        excluded_menu_count[menu_name] = count_duplicated_weather_order[menu_name]
                        excluded_menu_quantity[menu_name] = menu_quantity_to_exclude_or_not[menu_name]
            except KeyError:
                return HttpResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    content={
                        'message': '사전 key(메뉴명) 에러',
                    }
                )
            menu_list = (Cart.objects
                         .prefetch_related('order')
                         .filter(order__address__contains=user_dong, order__weather=user_dong_weather, order__created_time__month__gt=this_month - Month.three_month)
                         .values('cartitem__menu__name')
                         .annotate(menu=F('cartitem__menu__name'), quantity=Sum('cartitem__quantity'))
                         .exclude(menu__in=excluded_menu_count)
                         .order_by('-quantity')
                         .values('menu', 'quantity',
                                 price=F('cartitem__menu__price'), img=F('cartitem__menu__img'),
                                 id=F('cartitem__menu__id'), detail=F('cartitem__menu__detail'),
                                 restaurant=F(
                                     'cartitem__menu__restaurant__id'),
                                 )
                         )[:10]
            if not menu_list:
                return JsonResponse(
                    {'message': '날씨에 따라 잘 팔린 메뉴가 없습니다.'},
                    status=HTTPStatus.OK
                )
            weighted_quantity = {}
            for menu in menu_list:
                for month in range(this_month, this_month - Month.three_month, -1):
                    queryset = (Order.objects
                                .filter(cart__cartitem__menu__name=menu['menu'], created_time__month=month,
                                        weather=user_dong_weather)
                                .exclude(cart__isnull=True)
                                .select_related('cart', 'cart__cartitem__menu')
                                .prefetch_related('cart__cartitem')
                                .annotate(name=F('cart__cartitem__menu__name'),
                                          quantity=F('cart__cartitem__quantity'))
                                .values('name', 'quantity', 'created_time__month')
                                )
                    for q in queryset:
                        if month == this_month:
                            if q['name'] not in weighted_quantity:
                                weighted_quantity[q['name']] = q['quantity']
                            else:
                                weighted_quantity[q['name']] += q['quantity']
                        elif month == this_month - Month.one_month:
                            if q['name'] not in weighted_quantity:
                                weighted_quantity[q['name']] = round(
                                    q['quantity'] * Weight.one_month_ago_weight, 2)
                            else:
                                weighted_quantity[q['name']] += round(
                                    q['quantity'] * Weight.one_month_ago_weight, 2)
                        elif month == this_month - Month.two_month:
                            if q['name'] not in weighted_quantity:
                                weighted_quantity[q['name']] = round(
                                    q['quantity'] * Weight.two_month_ago_weight, 2)
                            else:
                                weighted_quantity[q['name']] += round(
                                    q['quantity'] * Weight.two_month_ago_weight, 2)
                if menu['menu'] in weighted_quantity.keys():
                    menu['weighted_quantity'] = weighted_quantity[menu['menu']]
            menu_list = sorted(list(menu_list), key=operator.itemgetter('weighted_quantity'), reverse=True)

            menu_list = list(menu_list, )
            data = {
                "menu_list": menu_list,
                "category_id": category_id,
                "sky_info": user_dong_weather,
                "exclude_menu": excluded_menu_count,
                "exclude_menu_quantity": excluded_menu_quantity,
                "message": "날씨별 메뉴 Top5 성공"
            }
            return JsonResponse(
                data,
            )


class MenuDetailAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        menu_id = kwargs['menu_id']
        menu = get_object_or_404(Menu, id=menu_id)
        cart = user.cart_set.order_by("-created_time")[0]
        try:
            data = {
                'id': menu.id,
                'name': menu.name,
                'img': menu.img.url,
                'detail': menu.detail,
                'price': menu.price,
                'cart_id': str(cart.id),
            }
            return JsonResponse(data)
        except ValueError:
            return JsonResponse(
                {
                    "message": "메뉴가 존재하지 않습니다.",
                },
                status=HTTPStatus.NOT_FOUND,
            )


class RandomMenuListAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        랜덤 메뉴 리스트를 보여주는 API
        """
        user = request.user
        try:
            last_created_cart = user.cart_set.order_by(
                '-created_time').values('id')[0]
        except IndexError:
            return JsonResponse({
                "message": "현재 주문표가 존재하지 않습니다."
            },
                status=HTTPStatus.NOT_FOUND
            )

        user_tastes = list(user.tastes.values('id', 'name'))

        if len(user_tastes) == 0:
            return JsonResponse({
                "message": "선택하신 취향이 존재하지않습니다. 'My Page'에서 취향을 선택해주세요.",
            },
                status=HTTPStatus.NOT_FOUND,
            )

        menus = (
            Menu.objects
            .filter(
                tastes__in=[
                    (lambda taste: taste['id'])(taste)
                    for taste in user_tastes
                ]
            )
            .prefetch_related('tastes')
            .select_related('restaurant')
            .distinct()
            .order_by('-score')
        )[:10]

        menu_count = menus.count()
        if menu_count == 0:
            return JsonResponse({
                "message": "취향에 해당하는 메뉴가 없습니다."
            },
                status=HTTPStatus.NOT_FOUND
            )

        random_menus = random.sample(
            list(menus),
            ONE_RANDOM_MENU_COUNT
        )

        menu_datas = [
            {
                'id': menu.id,
                'img': LOCALHOST + menu.img.url,
                'name': menu.name,
                'detail': menu.detail,
                'price': menu.price,
                'restaurant_name': menu.restaurant.name,
                'restaurant_min_order_price': menu.restaurant.min_order_price,
                'restaurant_delivery_charge': menu.restaurant.delivery_charge,
                'tastes': ""
            }
            for menu in random_menus
        ]

        for index, menu in enumerate(random_menus):
            temp_taste_list = []
            for taste in menu.tastes.all():
                temp_taste_list.append(taste.name)
            menu_datas[index]['tastes'] = temp_taste_list

        user_data = {
            'id': user.id,
            'name': user.username,
            'cart_id': last_created_cart['id'],
            'tastes': user_tastes
        }

        json_data = {
            'user': user_data,
            'menu': menu_datas
        }

        return JsonResponse(
            status=HTTPStatus.OK,
            data=json_data
        )


class AlreadyEatenMenuRandomListAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        내가 이미 주문했던 메뉴들 중, 3가지 메뉴를 랜덤으로 메뉴를 보여주는 API
        """
        user = request.user
        try:
            last_created_cart = user.cart_set.order_by(
                '-created_time').values('id')[0]
        except IndexError:
            return JsonResponse({
                "message": "현재 주문표가 존재하지 않습니다."
            },
                status=HTTPStatus.NOT_FOUND
            )

        already_eaten_menu_list = (
            Cart.objects
            .prefetch_related('order', 'cartitem')
            .filter(
                Q(order__delivery_status=DeliveryStatus.COMPLETE) &
                Q(order__status=PaymentStatus.ACCEPT) &
                ~Q(order=None)
            )
            .distinct()
            .filter(user=user)
            .annotate(
                menu_id=F('cartitem__menu__id'),
                img=F('cartitem__menu__img'),
                name=F('cartitem__menu__name'),
                detail=F('cartitem__menu__detail'),
                price=F('cartitem__menu__price'),
                restaurant_name=F('cartitem__menu__restaurant__name'),
                restaurant_min_order_price=F(
                    'cartitem__menu__restaurant__min_order_price'),
                restaurant_delivery_charge=F(
                    'cartitem__menu__restaurant__delivery_charge'),
            )
            .values(
                'menu_id',
                'img',
                'name',
                'detail',
                'price',
                'restaurant_name',
                'restaurant_min_order_price',
                'restaurant_delivery_charge',
            )

        )[:10]

        already_eaten_menu_count = already_eaten_menu_list.count()
        if already_eaten_menu_count < ONE_RANDOM_MENU_COUNT:
            return JsonResponse({
                "message": "아직 이전에 주문한 메뉴가 없거나 부족합니다."
            },
                status=HTTPStatus.NOT_FOUND
            )

        random_menus = random.sample(
            list(already_eaten_menu_list),
            ONE_RANDOM_MENU_COUNT
        )

        menu_data_list = [
            {
                'id': menu['menu_id'],
                'img': menu['img'],
                'name': menu['name'],
                'detail': menu['detail'],
                'price': menu['price'],
                'restaurant_name': menu['restaurant_name'],
                'restaurant_min_order_price': menu['restaurant_min_order_price'],
                'restaurant_delivery_charge': menu['restaurant_delivery_charge'],
                'tastes': ''
            }
            for menu in random_menus
        ]

        tastes = Taste.objects.prefetch_related('menu_set')
        for index, menu in enumerate(random_menus):
            temp_taste_list = tastes.filter(
                menu=menu['menu_id']).values_list('name', flat=True)
            menu_data_list[index]['tastes'] = list(temp_taste_list)

        json_data = {
            'user': {
                'cart_id': last_created_cart['id'],
            },
            'menu': menu_data_list
        }

        return JsonResponse(
            status=HTTPStatus.OK,
            data=json_data
        )
