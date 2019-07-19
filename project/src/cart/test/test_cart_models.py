import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from cart.models import Cart, CartItem
from category.models import Category
from menu.models import Menu
from restaurant.models import Restaurant


User = get_user_model()


class CartItemModelTestCase(TestCase):
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
        self.client.login(
            username='thkwon',
            password='hoho123!'
        )
        self.category = Category.objects.create(
            name="중화요리"
        )
        self.restaurant = Restaurant.objects.create(
            name="금룡",
            owner="권태형",
            title="금룡 한양대점",
            estimated_delivery_time=datetime.datetime.now(),
            operation_start_hour='2019-04-29 12:00',
            operation_end_hour='2019-04-29 22:00',
            min_order_price=15000,
            delivery_charge=2000,
        )
        self.category.restaurant_set.add(self.restaurant)

    def test_subtotal_price_should_be_equal_specific_menu_total_price(self):
        '''
        subtotal_price()의 리턴 값은 주문함에 담긴 특정 메뉴의 총 금액과 같다.
        '''
        # Given: 짬뽕 2개를 주문함에 답는다.
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name="짬뽕",
            detail="맛있는 짬뽕",
            price=8000,
            type="인기메뉴"
        )
        self.cart = Cart.objects.create(
            user=self.user
        )
        CartItem.objects.create(
            menu=self.jjambbong,
            cart=self.cart,
            quantity=2
        )
        cart_item = CartItem.objects.first()

        # When: 짬뽕 2개의 값을 구한다
        subtotal_price = cart_item.subtotal_price

        # Then: subtotal_price는 짬뽕 가격 * 2(16000원)와 같다.
        self.assertEqual(
            16000,
            subtotal_price
        )

    def test_total_price_should_be_equal_all_menu_price(self):
        '''
        total_price()는 주문함에 담긴 메뉴들의 총 금액과 같다.
        '''

        # Given: 짬뽕 2개, 짜장면 2개를 주문함에 답는다.
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name="짬뽕",
            detail="맛있는 짬뽕",
            price=8000,
            type="인기메뉴"
        )
        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            name="짜장면",
            detail="맛있는 짜장면",
            price=9000,
            type="인기메뉴"
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

        # When: 짬뽕 2개, 짜장면 2개 금액의 합을 구한다.
        total_price = self.cart.total_price

        # Then: total_price는 짬뽕 가격 * 2(16000원) + 짜장면 가격 * 2(18000원)과 같다.
        self.assertEqual(
            34000,
            total_price
        )

    def test_total_quantity_should_be_equal_all_menu_quantity(self):
        '''
        total_quantity는 주문함에 담긴 메뉴들의 총 개수와 같다.
        '''
        # Given: 짬뽕 2개, 짜장면 2개를 주문함에 답는다.
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name="짬뽕",
            detail="맛있는 짬뽕",
            price=8000,
            type="인기메뉴"
        )
        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            name="짜장면",
            detail="맛있는 짜장면",
            price=9000,
            type="인기메뉴"
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

        # When: 주문함의 모든 메뉴 개수를 담는다.
        total_quantity = self.cart.total_quantity

        # Then: total_quantity는 짜장면 2개, 짬뽕 2개, 총 4개 이다.
        self.assertEqual(
            4,
            total_quantity
        )

    def total_price_should_request_one_query_when_used_cached_property(self):
        '''
        cached_property를 이용하면, 모델 인스턴스의 메소드를 호출 할 때 마다,
        쿼리는 최초 1개만 요청한다.
        '''
        # Given: 짬뽕 1개를 주문함에 답는다.
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name="짬뽕",
            detail="맛있는 짬뽕",
            price=8000,
            type="인기메뉴"
        )
        self.cart = Cart.objects.create(
            user=self.user
        )
        CartItem.objects.create(
            menu=self.jjambbong,
            cart=self.cart,
            quantity=2
        )
        cart = Cart.objects.first()

        # When: total_price메소드를 최초 호출 한다. 이때 쿼리 1번이 요청된다.
        total_price = cart.total_price

        # Then: 모델 인스턴스 메소드를 3번 호출해도, 쿼리 호출 횟수는 0 이다.
        with self.assertNumQueries(0):
            total_price
            total_price
            total_price
