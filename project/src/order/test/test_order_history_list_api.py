from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from cart.models import Cart, CartItem
from menu.models import Menu
from order.models import Order, PaymentStatus, DeliveryStatus
from restaurant.models import Restaurant


class OrderHistoryListAPIViewTestCase(TestCase):
    def setUp(self):
        """
        * 레스토랑과 메뉴를 생성
        * 유저 생성
        * 유저에 해당하는 주문표 생성
        * 주문표에 메뉴를 생성
        """
        self.restaurant = Restaurant.objects.create(
            name='금룡',
            owner='권태형',
            title='금룡 한양대점',
            estimated_delivery_time='22:50',
            operation_start_hour='12:00',
            operation_end_hour='20:00',
            min_order_price=15000,
            delivery_charge=2000,
        )
        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            name='짜장면',
            detail='맛있는 짜장면',
            price=3000,
            hit=10,
            type='인기메뉴',
            img='test.jpg',
        )
        self.has_order_history_user = User.objects.create_user(
            username='has_order_history_user',
            email='',
            password='passwd123!'
        )
        self.no_order_history_user = User.objects.create_user(
            username='no_order_history_user',
            email='',
            password='passwd123!'
        )
        self.cart = Cart.objects.create(
            user=self.has_order_history_user
        )
        self.cartitem = CartItem.objects.create(
            cart=self.cart,
            menu=self.jjajangmyun,
            quantity=3
        )

    def make_one_order(self):
        """
        * 주문 생성
        """
        self.order = Order.objects.create(
            user=self.has_order_history_user,
            cart=self.cart,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status=PaymentStatus.ACCEPT,
            delivery_status=DeliveryStatus.WATING,
            phone_num="010-1234-1234"
        )

    def test_order_history_list_should_return_200_when_order_succeed(self):
        """
        로그인한 유저가 주문 내역이 있을 때, 200을 반환한다.
        """
        # Given: 1개의 주문 내역을 가진 유저가 로그인을 한다.
        self.make_one_order()
        self.client.login(
            username='has_order_history_user',
            password='passwd123!'
        )

        # When: OrderHistoryListAPIView를 호출한다.
        response = self.client.get(
            reverse('order_api:order_history_list')
        )

        # Then: 상태코드 200을 반환한다. / 주문의 개수는 실제 생성된 주문의 수(1개)와 같다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )
        self.assertEqual(
            len(response.json()['order']),
            1
        )

    def test_order_history_list_should_return_401_when_user_is_anonymous(self):
        """
        로그인하지 않았을 때, 401을 반환한다.
        """
        # Given: 유저는 로그인하지 않은 상태이다.

        # When: OrderHistoryListAPIView를 호출한다.
        response = self.client.get(
            reverse('order_api:order_history_list')
        )

        # Then: 상태코드 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_order_history_list_should_return_404_when_order_is_not_exists(self):
        """
        로그인한 유저의 주문이 하나도 없을 경우에 404를 반환한다. / 주문이 없습니다. 메세지를 출력한다.
        """
        # Given: 0개의 주문 내역을 가진 유저가 로그인을 한다.
        self.client.login(
            username='no_order_history_user',
            password='passwd123!'
        )
        # When: OrderHistoryListAPIView를 호출한다.
        response = self.client.get(
            reverse('order_api:order_history_list')
        )
        # Then: 상태코드 404를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(
            response.json()['message'],
            '주문이 없습니다.'
        )
