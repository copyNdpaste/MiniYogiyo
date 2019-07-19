from http import HTTPStatus
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from cart.models import Cart, CartItem
from category.models import Category
from menu.models import Menu
from restaurant.models import Restaurant


User = get_user_model()


class CartItemListAPIViewTestCase(TestCase):
    def setUp(self):
        '''
        * 로그인된 유저
        * 중화요리(카테고리) -> 금룡(음식점)
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

    def test_cart_list_should_returns_401_when_anonymous_user_request(self):
        '''
        비 로그인 상태 일 떄, 상태 코드 401를 반환한다.
        '''
        # Given: user는 비 로그인 상태이다.

        # When: CartItemListCreateAPIVIew를 호출한다.
        response = self.client.get(
            '/api/cart/fc1d1205-aadd-4c4c-b2e7-66e8afae8dc4/'
        )

        # Then: 상태코드 401를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_cart_list_should_returns_404_when_unfit_cart_id_request(self):
        '''
        없는 장바구니를 선택할 시, 상태 코드 404를 반환한다.
        '''
        # Given: user는 로그인 상태이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        not_exists_cart = '123456-aadd-4c4c-b2e7-66e8afae8dc1'

        # When: CartItemListCreateAPIVIew를 호출한다.
        response = self.client.get(
            '/api/cart/' + not_exists_cart + '/'
        )

        # Then: 상태코드 404를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )

    def test_cart_list_should_returns_200_when_there_is_more_than_one(self):
        '''
        로그인 상태에서, 주문표 내 메뉴가 2개 일 때, 상태코드 200을 반환하고, 메뉴의 개수는 2개이다.
        '''
        # Given: 로그인 후, 카트를 생성하고, 카트에 메뉴 2개를 추가 한다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        self.cart = Cart.objects.create(
            user=self.user
        )

        CartItem.objects.create(
            menu=self.jjambbong,
            cart=self.cart,
            quantity=2
        )

        CartItem.objects.create(
            menu=self.jjajangmyun,
            cart=self.cart,
            quantity=2
        )

        # When: CartItemListCreateAPIVIew를 호출한다.
        response = self.client.get('/api/cart/' + str(self.cart.id) + '/')
        json_data = json.loads(response.content)
        menu_list = json_data['restaurant']['menu']

        # Then: 메뉴의 개수는 2개이고, 상태코드 200을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )
        self.assertEqual(
            len(menu_list),
            2
        )

    def test_cart_list_should_returns_200_when_cart_menu_is_empty(self):
        '''
        로그인 상태에서, 주문표 내 메뉴가 비어있을 때, 상태코드 200을 반환하고,
        '주문표는 현재 비어있습니다.' 텍스트를 출력한다.
        '''
        # Given: 로그인 후, 카트를 생성한다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        self.cart = Cart.objects.create(
            user=self.user
        )

        # When: CartItemListCreateAPIVIew를 호출한다.
        response = self.client.get('/api/cart/' + str(self.cart.id) + '/')
        content = json.loads(response.content)['message']

        # Then: 상태코드 200을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )
        self.assertEqual(
            content,
            '주문표는 현재 비어있습니다.'
        )
