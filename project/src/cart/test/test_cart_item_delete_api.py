from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from cart.models import Cart, CartItem
from menu.models import Menu
from restaurant.models import Restaurant


User = get_user_model()


class CartItemDeleteAPIViewTestCase(TestCase):
    def setUp(self):
        '''
        * 유저 생성
        * Cart 생성
        * 레스토랑 생성
        * 메뉴 1개 생성 - 짜장면
        * Cart에 짜장면 담기
        '''
        self.user = User.objects.create_user(
            username='thkwon',
            email='',
            password='hohoho123!',
        )
        self.cart = Cart.objects.create(
            user=self.user
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
        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            name='짜장면',
            detail='맛있는 짜장면',
            price=8000,
            type='인기메뉴'
        )

    def _put_in_cart_menu_item(self):
        CartItem.objects.create(
            cart=self.cart,
            menu=self.jjajangmyun
        )

    def test_cart_item_crate_api_should_return_401_when_user_is_anonymous(self):
        '''
        Anonymous 유저가 접근했을 때 401을 반환한다.
        '''
        # Given: user는 Anonymous 상태이고, 존재하는 메뉴가 주어진다.
        exists_menu = str(self.jjajangmyun.id)
        self._put_in_cart_menu_item()

        # When: 정상적인 delete url을 요청한다.
        response = self.client.delete(
            '/api/cart/' + str(self.cart.id) + '/menu/' +
            exists_menu + '/',
            content_type='application/json',
        )
        # Then: 상태코드 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_cart_item_delete_api_should_return_200_when_cart_item_you_want_to_delete_exist(self):
        '''
        삭제하려는 Cart Item이 있으면 200을 반환한다.
        '''
        # Given: user는 로그인 상태이다. 짜장면 메뉴를 주문표에 담는다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        self._put_in_cart_menu_item()

        # When: 짜장면을 삭제하기위해서 요청한다.
        response = self.client.delete(
            '/api/cart/' + str(self.cart.id) + '/menu/' +
            str(self.jjajangmyun.id) + '/',
            content_type='application/json',
        )
        # Then: 상태코드 200를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

    def test_cart_item_delete_api_should_return_404_when_cart_item_you_want_to_delete_not_exist(self):
        '''
        삭제하려는 Cart Item이 없으면 404를 반환한다.
        '''
        # Given: user는 로그인 상태이다. 짜장면 메뉴를 주문표에 담는다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        not_exists_menu = '1234'

        # When: 존재하지 않는 메뉴를 넣어서, api를 호출한다.
        response = self.client.delete(
            '/api/cart/' + str(self.cart.id) + '/menu/' +
            not_exists_menu + '/',
            content_type='application/json',
        )
        # Then: 상태코드 404를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
