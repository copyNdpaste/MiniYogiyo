from http import HTTPStatus
from django.test import TestCase
from django.shortcuts import reverse
from accounts.models import User
from restaurant.models import Restaurant
from category.models import Category
from menu.models import Menu
from yosigy.models import Yosigy, YosigyMenu


class YosigyCreateAPIViewTestCase(TestCase):

    def setUp(self):
        self.username = 'store_owner'
        self.password = 'store'
        self.restaurant_owner = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='store_owner@gmail.com'
        )

        self.pizza_restaurant = Restaurant.objects.create(
            name='피자나라',
            owner='홍길동',
            store_owner=self.restaurant_owner,
            title='피자나라 서초점',
            estimated_delivery_time='22:50',
            operation_start_hour='12:00',
            operation_end_hour='22:00',
            min_order_price=10000,
            delivery_charge=2000,
        )

        self.chicken_restaurant = Restaurant.objects.create(
            name='치킨나라',
            owner='홍길동',
            store_owner=self.restaurant_owner,
            title='치킨나라 서초점',
            estimated_delivery_time='22:50',
            operation_start_hour='12:00',
            operation_end_hour='22:00',
            min_order_price=10000,
            delivery_charge=2000,
        )
        self.chicken = Menu.objects.create(
            restaurant=self.chicken_restaurant,
            img='/media/menu/2019/04/29/후라이드치킨.jpeg',
            name='후라이드 치킨',
            detail='후라이드에요',
            price='16000',
            type='인기메뉴'
        )
        self.pizza = Menu.objects.create(
            restaurant=self.pizza_restaurant,
            name='치즈피자',
            detail='치즈가 듬뿍',
            price='12000',
            type='인기메뉴'
        )

    def test_anonymous_user_post_yoisgy_create_api(self):
        # Given1: user is anonymous
        # self.client.login(username=self.username, password=self.password)
        # Given2: valid form data is given
        restaurant_menu_list = list(self.chicken_restaurant.menu_set.all().values('id', 'price'))
        form_data = {
            "restaurant": self.chicken_restaurant.id,
            "notice": "",
            "min_price": "10000",
            "menus": [
                {"id": restaurant_menu_list[0]['id'], "discounted_price": restaurant_menu_list[0]['price']-2000}]}

        # When: user post yoisgy_create_api
        response = self.client.post(
            path=reverse('yosigy_api:yosigy_create_api'),
            data=form_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should hava HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_restaurant_user_post_yoisgy_create_api_with_invalid_form_data(self):
        # Given1: user login
        self.client.login(username=self.username, password=self.password)
        # Given2: invalid form data has no menus key
        restaurant_menu_list = list(self.chicken_restaurant.menu_set.all().values('id', 'price'))
        form_data = {
            "restaurant": self.chicken_restaurant.id,
            "notice": "",
            "min_price": "10000",
            # "menus":
            #   [{"id": restaurant_menu_list[0]['id'], "discounted_price": restaurant_menu_list[0]['price'] - 2000}]
        }

        # When: user post yoisgy_create_api
        response = self.client.post(
            path=reverse('yosigy_api:yosigy_create_api'),
            data=form_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should hava HTTPStatus.BAD_REQUEST & error '잘못된 요청 입니다.'
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error'], '잘못된 요청 입니다.')

    def test_restaurant_user_post_yosigy_create_api_with_the_other_restaurant_menu(self):
        # Given1: user login
        self.client.login(username=self.username, password=self.password)
        # Given2: form data has the other restaurant menu
        restaurant_menu_list = list(self.pizza_restaurant.menu_set.all().values('id', 'price'))
        form_data = {
            "restaurant": self.chicken_restaurant.id,
            "notice": "",
            "min_price": "10000",
            "menus":
                [{"id": restaurant_menu_list[0]['id'], "discounted_price": restaurant_menu_list[0]['price'] - 2000}]
        }

        # When: user post yoisgy_create_api
        response = self.client.post(
            path=reverse('yosigy_api:yosigy_create_api'),
            data=form_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should hava HTTPStatus.BAD_REQUEST & error '잘못된 요청 입니다.'
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error'], '메뉴정보가 잘못되었습니다.')

    def test_restaurant_user_post_yoisgy_create_api(self):
        # Given1: user login
        self.client.login(username=self.username, password=self.password)
        # Given2: valid form data is given
        restaurant_menu_list = list(self.chicken_restaurant.menu_set.all().values('id', 'price'))
        form_data = {
            "restaurant": self.chicken_restaurant.id,
            "notice": "",
            "min_price": "10000",
            "menus":
                [{"id": restaurant_menu_list[0]['id'], "discounted_price": restaurant_menu_list[0]['price'] - 2000}]
        }

        # When: user post yoisgy_create_api
        response = self.client.post(
            path=reverse('yosigy_api:yosigy_create_api'),
            data=form_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should hava HTTPStatus.CREATED & message 게시물 작성을 성공하였습니다. & yosigy_id
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json()['message'], '게시물 작성을 성공하였습니다.')
        yosigy_id = Yosigy.objects.all().order_by('-created_time')[0].id
        self.assertEqual(response.json()['yosigy_id'], yosigy_id)

    def test_restaurant_user_post_yoisgy_create_api_when_the_restaurant_already_post_yosigy_event(self):
        # Given1: user login
        self.client.login(username=self.username, password=self.password)
        # Given2: valid form data is given
        restaurant_menu_list = list(self.chicken_restaurant.menu_set.all().values('id', 'price'))
        form_data = {
            "restaurant": self.chicken_restaurant.id,
            "notice": "",
            "min_price": "10000",
            "menus":
                [{"id": restaurant_menu_list[0]['id'], "discounted_price": restaurant_menu_list[0]['price'] - 2000}]
        }
        #  Given3: restaurant already_post_yosigy_event
        self.client.post(
            path=reverse('yosigy_api:yosigy_create_api'),
            data=form_data,
            content_type='application/json:charset=utf-8;'
        )

        # When: user post yoisgy_create_api
        response = self.client.post(
            path=reverse('yosigy_api:yosigy_create_api'),
            data=form_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should hava HTTPStatus.BAD_REQUEST
        # message 요식이 식권 이벤트 생성을 실패 하였습니다. & error 이미 이벤트를 진행 중 입니다
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['message'], '요식이 식권 이벤트 생성을 실패 하였습니다.')
        self.assertEqual(response.json()['error']['restaurant'][0], '이미 이벤트를 진행 중 입니다.')
