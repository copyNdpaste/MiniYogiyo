import json
from http import HTTPStatus

from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import User
from cart.models import Cart, CartItem
from menu.models import Menu
from restaurant.models import Restaurant


class BestSellingMenuTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create_user(username='mike', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user_without_address = User.objects.create_user(username='mike1', email='', password='2',
                                              address='')
        self.user_without_dong = User.objects.create_user(username='mike3', email='', password='2',
                                               address='서울시 서초구 서초2 사랑의 교회 1300호')
        self.restaurant = Restaurant.objects.create(
            name='굽내치킨', title='굽내치킨-서초점',
            min_order_price=10000, delivery_charge=1000, estimated_delivery_time='20:00',
            operation_start_hour='11:00', operation_end_hour='20:00', )
        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            name='볼케이노',
            detail='매콤한 맛입니다.',
            price=20000,
            type='양념류',
            img='test.jpg',
        )

    def test_return_UNAUTHORIZED_when_anonymous_request(self):
        '''
        로그인 X
        '''
        # Given
        # When
        response = self.client.get(reverse("timeline_api:bestmenu"))
        # Then
        message = json.loads(response.content)['message']
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(message, "로그인이 필요합니다.")

    def test_return_BAD_REQUEST_when_user_without_address_request(self):
        '''
        주소 없는 사용자인 경우 BAD REQUEST 반환
        '''
        # Given
        self.client.login(username='mike1', password='2')
        # When
        response = self.client.get(reverse("timeline_api:bestmenu"))
        # Then
        message = response.json()['message']
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(message, "mypage에서 사용자 주소를 입력하세요.")

    def test_return_BAD_REQUEST_when_user_without_dong_request(self):
        '''
        동 없는 사용자인 경우 BAD REQUEST 반환
        '''
        # Given
        self.client.login(username='mike3', password='2')
        # When
        response = self.client.get(reverse("timeline_api:bestmenu"))
        # Then
        message = response.json()['message']
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(message, "mypage에서 주소의 동 입력하세요.")

    def test_return_BAD_REQUEST_when_user_without_cart_request(self):
        '''
        카트 없는 사용자인 경우 BAD REQUEST 반환
        '''
        # Given
        self.client.login(username='mike', password='2')
        # When
        response = self.client.get(reverse("timeline_api:bestmenu"))
        # Then
        message = response.json()['message']
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(message, "cart가 없습니다.")

    def test_return_BAD_REQUEST_when_order_does_not_exist(self):
        '''
        주문이 없는 경우 BAD REQUEST 반환
        '''
        # Given
        self.client.login(username='mike', password='2')
        print(self.client)
        self.cart = Cart.objects.create(user=self.user)
        self.cartitem = CartItem.objects.create(
            menu=self.menu,
            cart=self.cart,
            quantity=0)
        # When
        response = self.client.get(reverse("timeline_api:bestmenu"))
        # Then
        message = json.loads(response.content)['message']
        addr = json.loads(response.content)['address']
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(message, "아직 주문이 많은 메뉴가 없습니다. 어서 주문하세요.")
        self.assertEqual(addr, '서초2동')
