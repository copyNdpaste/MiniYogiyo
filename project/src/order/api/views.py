import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.generic import View

from accounts.mixins import LoginRequiredMixin
from cart.models import CartItem, Cart
from menu.helpers import get_dong, get_x_y_grid, get_user_dong_weather
from order.api.utils import convert_datetime
from order.forms import OrderModelForm
from order.models import (Order,
                          STATUS_CHOICES,
                          PAYMENT_CHOICES,
                          DELIVERY_CHOICES)


class OrderCreateDetailAPIView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            order_data = json.loads(request.body)
            user_dong = get_dong(order_data['address'])
            x_y_grid = get_x_y_grid(user_dong)
            x = x_y_grid.x
            y = x_y_grid.y
            user_dong_weather = get_user_dong_weather(x, y)
            order_data['weather'] = user_dong_weather
        except json.JSONDecodeError:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '잘못된 요청 입니다.'
                }
            )
        form = OrderModelForm(order_data)

        if form.is_valid():
            order_obj = form.save()
            json_data = {
                'order_id': order_obj.id,
                'total_price': order_obj.total_price,
                'message': '주문에 성공하였습니다.'
            }
            Cart.objects.create(user=self.request.user)
        else:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '폼이 유효하지 않습니다.',
                    'error': form.errors
                }
            )
        return JsonResponse(
            status=HTTPStatus.CREATED,
            data=json_data
        )

    def get(self, request, *args, **kwargs):
        '''
        Cart에 담은 메뉴들을 보여주고 주문할 수 있다.
        '''
        user = self.request.user

        cart = user.cart_set.order_by('-created_time')[0]

        cart_items = CartItem.objects.select_related(
            'menu', 'menu__restaurant').filter(
            cart_id=cart.id
        )
        if cart_items.exists():
            user_info = {
                'id': user.id,
                'name': user.username,
                'address': user.address,
                'address_detail': user.address_detail,
                'phone': user.phone
            }
            menus_in_cart = [
                {
                    'id': cart_item.menu.id,
                    'name': cart_item.menu.name,
                    'description': cart_item.menu.detail,
                    'price': cart_item.menu.price,
                    'quantity': cart_item.quantity,
                    'subtotal': cart_item.subtotal_price,
                    'img': cart_item.menu.img.url
                }
                for cart_item in cart_items
            ]
            restaurant = cart_items[0].menu.restaurant
            restaurant_info = {
                'id': restaurant.id,
                'title': restaurant.title,
                'delivery_charge': restaurant.delivery_charge,
                'min_order_price': restaurant.min_order_price,
                'menu': menus_in_cart
            }
            cart_info = {
                'cart_id': cart.id,
                'total_price': cart.total_price + restaurant.delivery_charge,
                'total_quantity': cart.total_quantity,
            }
            json_data = {
                'cart': cart_info,
                'restaurant': restaurant_info,
                'user': user_info
            }

        else:
            return JsonResponse(
                status=HTTPStatus.NO_CONTENT,
                data={
                    'message': '주문표는 현재 비어있습니다.'
                }
            )

        return JsonResponse(
            status=HTTPStatus.OK,
            data=json_data,
        )


class OrderHistoryListAPIView(LoginRequiredMixin, View):
    """
    주문 내역 리스트를 보여주는 APIView
    """

    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        order_history_list = list(Order.objects.history_list(logged_in_user))

        if not order_history_list:
            return JsonResponse(
                status=HTTPStatus.NOT_FOUND,
                data={
                    'message': '주문이 없습니다.'
                },
            )

        cart_items_list = list(CartItem.objects.filtering_user(logged_in_user))

        order_data_list = []
        for order in order_history_list:
            ordered_menu_list = [
                item for item in cart_items_list
                if order['cart_id'] == item['cart_id']
            ]
            order_object = {
                'id': order['id'],
                'restaurant_img': order['restaurant__img'],
                'restaurant_title': order['restaurant__title'],
                'created_time': convert_datetime(order['created_time']),
                'delivery_status': DELIVERY_CHOICES[order['delivery_status']][1],
                'status': STATUS_CHOICES[order['status']][1],
                'payment_status': PAYMENT_CHOICES[order['payment_status']][1],
                'total_price': order['total_price'],
                'user_address': order['address'],
                'user_address_detail': order['address_detail'],
                'phone_num': order['phone_num'],
                'payment_status': order['payment_status'],
                'min_order_price': order['restaurant__min_order_price'],
                'delivery_charge': order['restaurant__delivery_charge'],
                'cart_id': order['cart_id'],
                'cartitem': ordered_menu_list,
                'is_yosigy_order': order['yosigy_ticket'],
                'yosigy_ticket__menu__name': order['yosigy_ticket__menu__name'],
                'yosigy_ticket__menu__img': order['yosigy_ticket__menu__img'],
                'yosigy_ticket__menu__detail': order['yosigy_ticket__menu__detail'],
                'is_gift_coupon': (True if order['gift_coupon'] is not None else False),
                'gift_coupon': (
                    {
                        'coupon_id': order['gift_coupon'],
                        'coupon_code': order['gift_coupon__coupon_code'],
                        'coupon_price':order['gift_coupon__price']
                    }if order['gift_coupon'] is not None else None)
            }
            order_data_list.append(order_object)

        json_data = {
            'user': logged_in_user.username,
            'order': order_data_list
        }

        return JsonResponse(
            status=HTTPStatus.OK,
            data=json_data,
        )


class ReOrderCreateAPIView(LoginRequiredMixin, View):
    def post(self, request, order_id, *args, **kwargs):
        """
        재주문을 하는 API 
        """
        try:
            order_obj = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return JsonResponse(
                status=HTTPStatus.NOT_FOUND,
                data={
                    'message': '주문 id를 찾을 수 없습니다.'
                }
            )

        if not order_obj.cart_id:
            return JsonResponse(
                status=HTTPStatus.NOT_FOUND,
                data={
                    'message': '해당 주문은 요식이로 구매하였습니다.'
                }
            )

        user = self.request.user
        new_cart = Cart.objects.create(user=user)
        menu_id_list = list(
            CartItem.objects.filter(cart_id=order_obj.cart_id).values_list('menu__id', flat=True)
        )
        cart_item_list = [
            CartItem(menu_id=menu_id, cart=new_cart, quantity=1)
            for menu_id in menu_id_list
        ]

        CartItem.objects.bulk_create(cart_item_list)

        return JsonResponse(
            status=HTTPStatus.OK,
            data={
                'message': "재주문할 새로운 주문표를 생성하였습니다."
            }
        )
