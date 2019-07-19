from http import HTTPStatus
import json

from django.test import TestCase

from accounts.models import User
from cart.models import Cart, CartItem
from category.models import Category
from menu.models import Menu
from restaurant.models import Restaurant


class OrderDetailAPIViewTestCase(TestCase):
    def setUp(self):
        '''
        * 유저 생성
        * 중화요리(카테고리) -> 금룡(음식점)
        * 메뉴 생성 - 짬뽕, 짜장면
        * Cart 생성
        '''
        self.user = User.objects.create_user(
            username='thkwon',
            email='',
            password='hohoho123!',
        )
        self.category = Category.objects.create(
            name='중화요리'
        )
        self.restaurant = Restaurant.objects.create(
            name='금룡',
            owner='권태형',
            title='금룡 한양대점',
            estimated_delivery_time='2019-04-29 22:50',
            operation_start_hour='2019-04-29 12:00',
            operation_end_hour='2019-04-29 20:00',
            min_order_price=15000,
            delivery_charge=2000,
        )
        self.category.restaurant_set.add(self.restaurant)
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            img='http://127.0.0.1:8000/media/menu/2019/04/29/jjambbong.jpg',
            name='짬뽕',
            detail='맛있는 짬뽕',
            price=8000,
            type='인기메뉴'
        )
        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            img='http://127.0.0.1:8000/media/menu/2019/04/29/jjajangmyun.jpg',
            name='짜장면',
            detail='맛있는 짜장면',
            price=9000,
            type='인기메뉴'
        )
        self.cart = Cart.objects.create(
            user=self.user
        )

    def _put_in_cart_menu_item(self, menu, quantity):
        '''
        Cart에 메뉴 하나를 넣는다.
        '''
        CartItem.objects.create(
            cart=self.cart,
            menu=menu,
            quantity=quantity
        )

    def test_order_detail_should_returns_401_when_anonymous_user_request(self):
        '''
        비 로그인 상태 일 떄, 상태 코드 401를 반환한다.
        '''
        # Given: user는 비 로그인 상태이다.
        # self.client.login(
        #     username='thkwon',
        #     password='hohoho123!'
        # )

        # When: OrderDetailAPIView를 호출한다.
        response = self.client.get(
            '/api/order/'
        )

        # Then: 상태코드 401를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_order_detail_should_returns_200_and_data_when_cart_items_exist(self):
        '''
        로그인 상태에서, 주문표 내 메뉴가 2개 일 때, 상태코드 200을 반환한다.
        '''
        # Given: 로그인 후, Cart에 메뉴 2개를 추가 한다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        self._put_in_cart_menu_item(
            menu=self.jjajangmyun,
            quantity=2
        )
        self._put_in_cart_menu_item(
            menu=self.jjambbong,
            quantity=3
        )

        # When: OrderDetailAPIVIew를 호출한다.
        response = self.client.get('/api/order/')
        json_data = json.loads(response.content)
        menu_list = json_data['restaurant']['menu']
        jjajangmyun_quantity = json_data['restaurant']['menu'][0]['quantity']
        jjambbong_quantity = json_data['restaurant']['menu'][1]['quantity']

        # Then: 상태코드 200을 반환하고 메뉴의 개수는 2개이고, 총 quantity는 5이다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )
        self.assertEqual(
            len(menu_list),
            2
        )
        self.assertEqual(
            self.cart.total_quantity,
            jjajangmyun_quantity + jjambbong_quantity
        )

    def test_order_detail_should_returns_204_when_cart_items_are_empty(self):
        '''
        로그인 상태에서, 주문표 내 메뉴가 비어있을 때, 상태코드 204를 반환한다.
        '''
        # Given: 1. 로그인을 한 상태이고,
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        # Given: 2. Cart에는 아무 메뉴도 넣지 않았다.
        # self._put_in_cart_menu_item(
        #     menu=self.jjajangmyun,
        #     quantity=1
        # )

        # When: OrderDetailAPIVIew를 호출한다.
        response = self.client.get('/api/order/')

        # Then: Cart에 아무 메뉴가 없으므로, 상태코드 204을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NO_CONTENT
        )
