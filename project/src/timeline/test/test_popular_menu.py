from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from cart.models import Cart
from menu.models import Menu
from restaurant.models import Restaurant


class PopularMenuListAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='thkwon',
            email='',
            password='hohoho123!',
        )
        self.cart = Cart.objects.create(
            user=self.user
        )
        self._make_ten_menus()
        settings.POPULAR_MENU_LIST_MAX_LENGTH = 10

    def test_popular_menu_list_api_should_return_401_when_user_is_anonymous(self):
        """
        비 로그인 상태이면 401을 반환한다.
        """
        # Given: user는 비 로그인 상태이다.

        # When: popular_menu_list_api를 호출한다.
        response = self.client.get(
            reverse('timeline_api:popularmenu', kwargs={'sort_based_value': 'hit'})
        )

        # Then: 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_popular_menu_list_api_should_return_404_when_url_parameter_is_not_valid(self):
        """
        url 파라미터가 정상적이지 않을 때, 404 에러를 반환한다.
        """
        # Given: 유저는 로그인 상태이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        # When: popular_menu_list_api를 호출한다.
        response = self.client.get(
            reverse(
                'timeline_api:popularmenu',
                kwargs={'sort_based_value': 'INVALID_PARAMETER'}
            )
        )
        # Then: 404를 반환하고, 파라미터 값이 올바르지 않습니다. 메세지를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(
            response.json()['message'],
            '파라미터 값이 올바르지 않습니다.'
        )

    def test_popular_menu_list_api_should_return_200_when_url_parameter_is_hit(self):
        """
        url 파라미터가 hit로 정상적으로 넘어왔을 때, 200을 리턴한다.
        """
        # Given: 유저는 로그인 상태이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        # When: popular_menu_list_api를 호출한다.
        response = self.client.get(
            reverse(
                'timeline_api:popularmenu',
                kwargs={'sort_based_value': 'hit'}
            )
        )
        # Then: 200을 반환하고, 반환하는 리스트의 길이는 10 이고, response의 첫번째 값이 MAX 값이다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )
        self.assertEqual(
            len(response.json()['menu']),
            settings.POPULAR_MENU_LIST_MAX_LENGTH
        )
        result_menu_list = response.json()['menu']
        max_obj = max(result_menu_list, key=lambda x: x['hit'])
        self.assertEqual(
            result_menu_list[0]['hit'],
            max_obj['hit']
        )

    def test_popular_menu_list_api_should_return_200_when_url_parameter_is_like(self):
        """
        url 파라미터가 like로 정상적으로 넘어왔을 때, 200을 리턴한다.
        """
        # Given: 유저는 로그인 상태이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        # When: popular_menu_list_api를 호출한다.
        response = self.client.get(
            reverse(
                'timeline_api:popularmenu',
                kwargs={'sort_based_value': 'like'}
            )
        )
        # Then: 200을 반환하고, 반환하는 리스트의 길이는 10 이고, response의 첫번째 값이 MAX 값이다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )
        self.assertEqual(
            len(response.json()['menu']),
            settings.POPULAR_MENU_LIST_MAX_LENGTH
        )
        result_menu_list = response.json()['menu']
        max_obj = max(result_menu_list, key=lambda x: x['like_count'])
        self.assertEqual(
            result_menu_list[0]['like_count'],
            max_obj['like_count']
        )

    def test_popular_menu_list_api_should_return_200_when_url_parameter_is_score(self):
        """
        url 파라미터가 score로 정상적으로 넘어왔을 때, 200을 리턴한다.
        """
        # Given: 유저는 로그인 상태이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        # When: popular_menu_list_api를 호출한다.
        response = self.client.get(
            reverse(
                'timeline_api:popularmenu',
                kwargs={'sort_based_value': 'score'}
            )
        )
        # Then: 200을 반환하고, 반환하는 리스트의 길이는 10 이고, response의 첫번째 값이 MAX 값이다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )
        self.assertEqual(
            len(response.json()['menu']),
            settings.POPULAR_MENU_LIST_MAX_LENGTH
        )
        result_menu_list = response.json()['menu']
        max_obj = max(result_menu_list, key=lambda x: x['score'])
        self.assertEqual(
            result_menu_list[0]['score'],
            max_obj['score']
        )

    def _make_ten_menus(self):
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
            img='restaurant.jpg'
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

        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            name='짜장면',
            detail='맛있는 맛있는 짜장면',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
