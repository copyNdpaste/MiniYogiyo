import json
from http import HTTPStatus

from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import View
from django_bulk_update.helper import bulk_update

from accounts.mixins import LoginRequiredMixin
from cart.forms import (
    CartModelForm,
    CartItemModelForm,
    CartItemUpdateModelForm
)
from cart.models import Cart, CartItem
from menu.models import Menu


class CartItemQuantityAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            cart_obj = self.request.user.cart_set.order_by('-created_time')[0]
        except IndexError:
            return JsonResponse(
                status=HTTPStatus.OK,
                data={
                    "total_quantity": 0
                }
            )

        return JsonResponse(
            status=HTTPStatus.OK,
            data={
                "cart_id": cart_obj.id,
                "total_quantity": cart_obj.total_quantity
            }
        )


class CartListCreateAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        '''
        주문표 내 메뉴의 리스트를 보여준다.
        '''
        cart_obj = self.request.user.cart_set.order_by('-created_time')[0]
        cart_items = (
            CartItem.objects.select_related(
                'menu',
                'menu__restaurant'
            ).prefetch_related('menu__tastes')
                .filter(cart__id=cart_obj.id)
        )

        if not cart_items.exists():
            return JsonResponse(
                data={
                    'message': '주문표는 현재 비어있습니다.'
                }
            )

        first_menu = cart_items.first()

        cart_info = {
            'cart_id': first_menu.cart.id,
            'order_start_url': '',
            'home_url': reverse('home'),
            'total_price': first_menu.cart.total_price,
            'total_quantity': first_menu.cart.total_quantity,
            'delete_url': reverse('cart_api:cart_delete_api',
                                  kwargs={'cart_id': first_menu.cart.id}
                                  )
        }

        menus_in_cart = [
            {
                'id': cart_item.menu.id,
                'img': cart_item.menu.img.url,
                'name': cart_item.menu.name,
                'description': cart_item.menu.detail,
                'price': cart_item.menu.price,
                'quantity': cart_item.quantity,
                'subtotal': cart_item.subtotal_price,
                'taste': ''
            }
            for cart_item in cart_items
        ]

        for index, cart_item in enumerate(cart_items):
            temp_taste_list = []
            for taste in cart_item.menu.tastes.all():
                temp_taste_list.append(taste.name)
            menus_in_cart[index]['taste'] = temp_taste_list

        restaurant = first_menu.menu.restaurant
        restaurant_info = {
            'id': restaurant.id,
            'name': restaurant.name,
            'min_order_price': restaurant.min_order_price,
            'menu': menus_in_cart
        }
        json_data = {
            'cart': cart_info,
            'restaurant': restaurant_info
        }

        return JsonResponse(
            status=HTTPStatus.OK,
            data=json_data,
        )

    def post(self, request, *args, **kwargs):
        '''
        주문표을 생성한다.
        '''
        try:
            cart_data = json.loads(request.body)
        except ValueError:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '잘못된 요청 입니다.'
                }
            )
        form = CartModelForm(cart_data)

        if form.is_valid():
            cart_obj = form.save(commit=True)
            json_data = {
                'cart_id': cart_obj.id,
                'user': cart_obj.user.username
            }
            return JsonResponse(
                status=HTTPStatus.CREATED,
                data=json_data,
            )

        return JsonResponse(
            status=HTTPStatus.BAD_REQUEST,
            data={
                'message': '유효 하지 않은 폼 형식 혹은 해당 유저는 이미 생성된 Cart가 있습니다.'
            }
        )


class CartItemCreateAPIView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        '''
        주문표에 메뉴를 추가한다.
        '''
        try:
            cart_data = json.loads(request.body)
        except ValueError:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '잘못된 요청 입니다.'
                }
            )
        form = CartItemModelForm(cart_data)

        if not form.is_valid():
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '유효하지않은 폼 형식 입니다.'
                }
            )

        cart_item_list = list(
            CartItem.objects.select_related(
                'menu__restaurant',
                'cart'
            ).filter(
                cart__id=cart_data['cart'],
            ).values('menu', 'menu__restaurant')
        )

        if cart_item_list:
            new_cart_item_restaurant_id = Menu.objects.filter(id=cart_data['menu']).first().restaurant_id

            if new_cart_item_restaurant_id is not cart_item_list[0]['menu__restaurant']:
                return JsonResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    data={
                        'message': '다른 레스토랑의 메뉴는 주문함에 담을 수 없습니다.'
                    }
                )

            if cart_data['menu'] in [(lambda element: element['menu'])(cart_item) for cart_item in cart_item_list]:
                return JsonResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    data={
                        'message': '중복된 메뉴 입니다.'
                    }
                )

        cart_item = form.save(commit=True)
        json_data = {
            'menu_id': cart_item.menu.id,
            'cart_id': cart_item.cart.id,
            'menu_name': cart_item.menu.name,
            'total_quantity': cart_item.cart.total_quantity
        }
        return JsonResponse(
            status=HTTPStatus.CREATED,
            data=json_data,
        )


class CartItemDeleteAPIView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        '''
        주문표의 특정 메뉴를 삭제한다.
        '''
        try:
            cart_item_obj = CartItem.objects.get(
                cart__id=self.kwargs['cart_id'],
                menu__id=self.kwargs['menu_id']
            )
        except CartItem.DoesNotExist:
            return JsonResponse(
                status=HTTPStatus.NOT_FOUND,
                data={
                    'message': '주문표에 해당하는 메뉴가 없습니다.'
                }
            )
        else:
            cart_item_obj.delete()

        return JsonResponse(
            status=HTTPStatus.OK,
            data={
                'message': '성공적으로 삭제하였습니다.',
                'subtotal': cart_item_obj.subtotal_price,
                'total_price': cart_item_obj.cart.total_price,
                'total_quantity': cart_item_obj.cart.total_quantity
            }
        )


class CartDeleteAPIView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        '''
        주문표를 삭제한다.
        '''
        try:
            cart_obj = Cart.objects.get(
                id=self.kwargs['cart_id']
            )
        except Cart.DoesNotExist:
            return JsonResponse(
                status=HTTPStatus.NOT_FOUND,
                data={
                    'message': '해당하는 주문표가 존재하지 않습니다.',
                }
            )
        else:
            cart_obj.delete()
            new_cart = Cart.objects.create(user=self.request.user)

        return JsonResponse(
            status=HTTPStatus.OK,
            data={
                'message': '주문표는 현재 비어있습니다.',
                'total_quantity': cart_obj.total_quantity,
                'cart_id': new_cart.id
            }
        )


class CartItemUpdateAPIView(LoginRequiredMixin, View):
    def put(self, request, *args, **kwargs):
        '''
        Cart 내 메뉴 개수를 조정한다.
        '''
        try:
            json_datas = json.loads(request.body)
        except ValueError:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '잘못된 요청 입니다.'
                }
            )

        cart_items = CartItem.objects.select_related('menu', 'cart').filter(
            cart__id=self.kwargs['cart_id'],
        )

        for json_data in json_datas:
            form = CartItemUpdateModelForm(
                json_data,
            )
            if form.is_valid():
                for cart_item in cart_items:
                    if cart_item.menu.id == json_data['menu']:
                        cart_item.quantity = json_data['quantity']
            else:
                return JsonResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    data={
                        'message': '폼이 유효하지 않습니다.',
                        'error': form.errors
                    }
                )

        bulk_update(cart_items, update_fields=['quantity'])

        return JsonResponse(
            status=HTTPStatus.OK,
            data={
                'message': '메뉴가 성공적으로 추가되었습니다.',
                'subtotal': cart_items[0].subtotal_price,
                'total_price': cart_items[0].cart.total_price,
                'total_quantity': cart_items[0].cart.total_quantity
            },
        )
