from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from cart.models import Cart, CartItem
from menu.models import Menu
from order.models import Order, DeliveryStatus
from restaurant.models import Restaurant


class AlreadyEatenRandomMenuListAPIViewTestCase(TestCase):
    def setUp(self):
        """
        * 유저 생성
        * 메뉴 생성
        * 주문표 생성
        * 주문표 내 메뉴 생성
        """

        self.user = User.objects.create_user(
            username='thkwon',
            email='',
            password='hohoho123!',
        )
        self.make_ten_menus()
        self.make_cart()
        self.make_cart_item()

    def test_already_eaten_random_api_should_return_401_when_user_is_anonymous(self):
        """
        비 로그인 상태이면 401을 반환한다.
        """
        # Given: user는 비 로그인 상태이다.

        # When: already_eaten_random_menu_list_api를 호출한다.
        response = self.client.get(
            reverse('menu_api:already_eaten_random_menu_list_api')
        )

        # Then: 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_already_eaten_random_api_should_return_200_when_already_be_ordered_menu_are_more_than_three(self):
        """
        유저가 이전에 주문한 메뉴의 개수가 3개 이상이면, 200을 반환한다.
        """
        # Given: 유저는 이전에 총 5개의 메뉴 주문하였다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        self.make_five_order()

        # When: already_eaten_random_menu_list_api를 호출한다.
        response = self.client.get(
            reverse('menu_api:already_eaten_random_menu_list_api')
        )

        # Then: 유저가 주문하였던 5개의 메뉴 중 3개를 랜덤으로 선택한다. / 200을 반환한다.
        RESULT_RANDOM_MENU_COUNT = 3

        self.assertEqual(
            len(response.json()['menu']),
            RESULT_RANDOM_MENU_COUNT
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

    def test_already_eaten_random_api_should_return_404_when_already_eaten_menu_count_is_two(self):
        """
        유저가 이전에 주문한 메뉴 수가 RANDOM_MENU_COUNT(3) 보다 작고, 개수가 2개이면, 404를 반환한다.
        """

        # Given: 유저는 이전에 총 2개의 메뉴 주문하였다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        self.make_two_order()

        # When: already_eaten_random_menu_list_api를 호출한다.
        response = self.client.get(
            reverse('menu_api:already_eaten_random_menu_list_api')
        )

        # Then: 유저가 주문하였던 2개의 메뉴는 RANDOM_MENU_COUNT 보다 작기 때문에 404를 반환한다.
        self.assertEqual(
            response.json()['message'],
            '아직 이전에 주문한 메뉴가 없거나 부족합니다.'
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )

    def test_already_eaten_random_api_should_return_404_when_already_eaten_menu_count_is_one(self):
        """
        유저가 이전에 주문한 메뉴 수가 RANDOM_MENU_COUNT(3) 보다 작고, 개수가 1개이면, 404를 반환한다.
        """

        # Given: 유저는 이전에 총 1개의 메뉴 주문하였다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        self.make_one_order()

        # When: already_eaten_random_menu_list_api를 호출한다.
        response = self.client.get(
            reverse('menu_api:already_eaten_random_menu_list_api')
        )

        # Then: 유저가 주문하였던 1개의 메뉴는 RANDOM_MENU_COUNT 보다 작기 때문에 404를 반환한다.
        self.assertEqual(
            response.json()['message'],
            '아직 이전에 주문한 메뉴가 없거나 부족합니다.'
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )

    def test_already_eaten_random_api_should_return_404_when_already_eaten_menu_count_is_zero(self):
        """
        유저가 이전에 주문한 메뉴 수가 RANDOM_MENU_COUNT(3) 보다 작고, 개수가 0개이면, 404를 반환한다.
        """

        # Given: 유저는 계정 생성 후, 바로 로그인한 상태이다.(주문수 0이다.)
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        # When: already_eaten_random_menu_list_api를 호출한다.
        response = self.client.get(
            reverse('menu_api:already_eaten_random_menu_list_api')
        )

        # Then: 유저는 아무런 주문을 하지 않았기 때문에, 404를 반환한다.
        self.assertEqual(
            response.json()['message'],
            '아직 이전에 주문한 메뉴가 없거나 부족합니다.'
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )

    def test_already_eaten_api_should_return_404_when_user_cart_is_not_exists(self):
        """
        주문자에 해당하는 Cart가 존재하지 않으면 404를 반환한다
        """

        # Given: 주문자 계정을 생성하고, 로그인을 한다. cart는 지정하지 않는다.
        user_do_not_have_cart = User.objects.create_user(
            username='user_do_not_have_cart',
            email='',
            password='passwd123!',
        )
        self.client.login(
            username=user_do_not_have_cart.username,
            password='passwd123!'
        )

        # When: RandomMenuListAPI를 호출한다.
        response = self.client.get(
            reverse('menu_api:already_eaten_random_menu_list_api')
        )

        # Then: 404를반환한다. / 현재 주문표가 존재하지 않습니다. 메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(
            response.json()['message'],
            "현재 주문표가 존재하지 않습니다."
        )

    def make_cart(self):
        """
        Cart 5개를 생성한다.
        """
        self.cart_1 = Cart.objects.create(
            user=self.user
        )
        self.cart_2 = Cart.objects.create(
            user=self.user
        )
        self.cart_3 = Cart.objects.create(
            user=self.user
        )
        self.cart_4 = Cart.objects.create(
            user=self.user
        )
        self.cart_5 = Cart.objects.create(
            user=self.user
        )

    def make_cart_item(self):
        """
        생성된 Cart에 Item을 넣는다.
        """
        CartItem.objects.create(
            cart=self.cart_1,
            menu=self.jjajangmyun,
            quantity=3
        )
        CartItem.objects.create(
            cart=self.cart_2,
            menu=self.jjambbong,
            quantity=2
        )
        CartItem.objects.create(
            cart=self.cart_3,
            menu=self.chinese_ddeokboke,
            quantity=2
        )
        CartItem.objects.create(
            cart=self.cart_4,
            menu=self.yangjangpi,
            quantity=5
        )
        CartItem.objects.create(
            cart=self.cart_5,
            menu=self.tangsuyook,
            quantity=4
        )

    def make_five_order(self):
        """
        생성된 Cart를 바탕으로 임의 주문 5개을 생성한다.
        """
        self.order_1 = Order.objects.create(
            user=self.user,
            cart=self.cart_1,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        self.order_2 = Order.objects.create(
            user=self.user,
            cart=self.cart_2,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        self.order_3 = Order.objects.create(
            user=self.user,
            cart=self.cart_3,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        self.order_4 = Order.objects.create(
            user=self.user,
            cart=self.cart_4,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        self.order_5 = Order.objects.create(
            user=self.user,
            cart=self.cart_5,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )

    def make_two_order(self):
        """
        생성된 Cart를 바탕으로 임의 주문 2개을 생성한다.
        """
        self.order_1 = Order.objects.create(
            user=self.user,
            cart=self.cart_1,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        self.order_2 = Order.objects.create(
            user=self.user,
            cart=self.cart_2,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )

    def make_one_order(self):
        """
        생성된 Cart를 바탕으로 임의 주문 2개을 생성한다.
        """
        self.order_1 = Order.objects.create(
            user=self.user,
            cart=self.cart_1,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )

    def make_ten_menus(self):
        """
        임의의 메뉴 10개를 생성한다.
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
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='짬뽕',
            detail='맛있는 짬뽕',
            price=3000,
            hit=9,
            type='인기메뉴',
            img='test.jpg',
        )
        self.tangsuyook = Menu.objects.create(
            restaurant=self.restaurant,
            name='탕수육',
            detail='맛있는 탕수육',
            price=3000,
            hit=8,
            type='인기메뉴',
            img='test.jpg',
        )
        self.spicy_jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='매운 짬뽕',
            detail='맛있는 매운 짬뽕',
            price=3000,
            hit=7,
            type='인기메뉴',
            img='test.jpg',
        )
        self.gganpoongi = Menu.objects.create(
            restaurant=self.restaurant,
            name='깐풍기',
            detail='맛있는 깐풍기',
            price=3000,
            hit=6,
            type='인기메뉴',
            img='test.jpg',
        )
        self.yangjangpi = Menu.objects.create(
            restaurant=self.restaurant,
            name='양장피',
            detail='맛있는 양장피',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.chinese_ddeokboke = Menu.objects.create(
            restaurant=self.restaurant,
            name='중국식 떡볶이',
            detail='맛있는 중국식 떡볶이',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.chinese_woodong = Menu.objects.create(
            restaurant=self.restaurant,
            name='중국식 우동',
            detail='맛있는 중국식 우동',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.fried_jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='볶음짬봉',
            detail='맛있는 볶음짬봉',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.jjabchaebob = Menu.objects.create(
            restaurant=self.restaurant,
            name='잡채밥',
            detail='맛있는 잡채밥',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
