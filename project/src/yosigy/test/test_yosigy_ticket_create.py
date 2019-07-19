# test_yosigy_ticket_create
import datetime
import json
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from category.models import Category
from menu.models import Menu
from restaurant.models import Restaurant
from yosigy.models import Yosigy, YosigyMenu


class YosigyTicketCreateAPIViewTestCase(TestCase):
    def setUp(self):
        """
        1. 유저 생성 
        2. 요식이 지정 레스토랑 생성
        3. 메뉴 생성
        """
        self.user = User.objects.create_user(
            username='yosigy_user',
            email='',
            password='yosigy_password'
        )
        self.owner = User.objects.create_user(
            username='im_owner',
            email='',
            password='owner_password'
        )

        self.category = Category.objects.create(
            name='중화요리'
        )
        self.restaurant = Restaurant.objects.create(
            name='금룡',
            store_owner=self.owner,
            title='금룡 한양대점',
            estimated_delivery_time='22:50',
            operation_start_hour='12:00',
            operation_end_hour='20:00',
            min_order_price=15000,
            delivery_charge=2000,
            is_yosigy=True,
            img='test.jpg'
        )

        # 메뉴 5개 생성
        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            name='짜장면',
            detail='맛있는 짜장면',
            price=3000,
            type='인기메뉴',
            img='test.jpg',

        )
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='짬뽕',
            detail='맛있는 짬뽕',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.tangsuyook = Menu.objects.create(
            restaurant=self.restaurant,
            name='탕수육',
            detail='맛있는 탕수육',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.spicy_jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='매운 짬뽕',
            detail='맛있는 매운 짬뽕',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.gganpoongi = Menu.objects.create(
            restaurant=self.restaurant,
            name='깐풍기',
            detail='맛있는 깐풍기',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        # 요식이 이벤트와, 요식이 메뉴 생성
        self.yosigy = Yosigy.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            deadline=datetime.datetime.now() + datetime.timedelta(days=10),
            notice="요식이 공지사항 입니다!",
            min_price=15000
        )
        self.yosigy_menu_jjambbong = YosigyMenu.objects.create(
            discounted_price=4000,
            menu=self.jjambbong,
            yosigy=self.yosigy
        )
        self.yosigy_menu_jjajangmyun = YosigyMenu.objects.create(
            discounted_price=3500,
            menu=self.jjajangmyun,
            yosigy=self.yosigy
        )

    def test_yosigy_ticket_create_should_return_401_when_user_is_anonymous(self):
        """
        요식이 티켓 생성 API는 비로그인 상태일 때는 401을 반환해야한다. 
        """
        # Given: 유저는 비 로그인 상태이다. / 유효한 폼 데이터가 주어진다.

        valid_form_data_list = [
            {
                'yosigy_menu_id': self.yosigy_menu_jjajangmyun.id,
                'menu_id': self.jjajangmyun.id,
                'discounted_price': 5000,
                'quantity': 3
            },
            {
                'yosigy_menu_id': self.yosigy_menu_jjambbong.id,
                'menu_id': self.jjambbong.id,
                'discounted_price': 4000,
                'quantity': 2
            }
        ]

        # When: YosigyTicketCreateAPIView를 호출한다.
        response = self.client.post(
            path=reverse(
                'yosigy_api:yosigy_create_ticket_api',
                kwargs={'restaurant_id': self.restaurant.id}
            ),
            data=json.dumps(valid_form_data_list),
            content_type='application/json:charset=utf-8;'
        )

        # Then: 상태코드 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_yosigy_ticket_create_should_return_201_when_yosigy_menu_obj_list_is_valid(self):
        """
        요식이 티켓 생성 API는 req.body로 전달받는 값이 정상적이면, 200을 반환한다.    
        """
        # Given: user는 로그인 상태이다 / valid_form_data가 주어진다.
        self.client.login(
            username='yosigy_user',
            password='yosigy_password'
        )

        valid_form_data_list = [
            {
                'yosigy_menu_id': self.yosigy_menu_jjajangmyun.id,
                'menu_id': self.jjajangmyun.id,
                'discounted_price': self.yosigy_menu_jjajangmyun.discounted_price,
                'quantity': 10
            },
            {
                'yosigy_menu_id': self.yosigy_menu_jjambbong.id,
                'menu_id': self.jjambbong.id,
                'discounted_price': self.yosigy_menu_jjambbong.discounted_price,
                'quantity': 10
            }
        ]

        # When: YosigyTicketCreateAPIView를 호출한다.
        response = self.client.post(
            path=reverse(
                'yosigy_api:yosigy_create_ticket_api',
                kwargs={'restaurant_id': self.restaurant.id}
            ),
            data=json.dumps(valid_form_data_list),
            content_type='application/json:charset=utf-8;'
        )

        # Then: 상태코드 201을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.CREATED
        )

    def test_yosigy_ticket_create_should_return_400_when_json_decode_error_occured_in_req_body(self):
        """
        요식이 티켓 생성 API는 req.body로 부터 받은 json 값이 디코딩 에러를 발생시키면,  400을 반환해야한다. 
        """
        # Given: user는 로그인 상태이다. 유효하지 않은 json이 주어진다.
        self.client.login(
            username='yosigy_user',
            password='yosigy_password'
        )

        invalid_json_data = """[
            {"yosigy_menu_id": 2, "menu_id": 2, "quantity": 10, "discounted_price": 10000}
            {"yosigy_menu_id": 1, "menu_id": 1, "quantity": 10, "discounted_price": 10000},
        ]"""

        # When: YosigyTicketCreateAPIView를 호출한다.
        response = self.client.post(
            path=reverse(
                'yosigy_api:yosigy_create_ticket_api',
                kwargs={'restaurant_id': self.restaurant.id}
            ),
            data=invalid_json_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then: 상태코드 400을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )

    def test_yosigy_ticket_create_should_return_400_when_menu_id_is_not_exists(self):
        """
        요식이 티켓 생성 API는 메뉴가 존재하지 않을 때, 400을 반환해야한다. 
        """
        INVALID_YOSIGY_MENU_ID = 1000

        # Given: 유저는 로그인 상태이다 / 요시기 이벤트 생성 / 요식이 메뉴가 생성
        self.client.login(
            username='yosigy_user',
            password='yosigy_password'
        )

        invalid_form_data_list = [
            {
                'yosigy_menu_id': INVALID_YOSIGY_MENU_ID,
                'menu_id': self.tangsuyook.id,
                'discounted_price': 15000,
                'quantity': 3
            },
        ]

        # When: YosigyTicketCreateAPIView를 호출한다.
        response = self.client.post(
            path=reverse(
                'yosigy_api:yosigy_create_ticket_api',
                kwargs={'restaurant_id': self.restaurant.id}
            ),
            data=json.dumps(invalid_form_data_list),
            content_type='application/json:charset=utf-8;'
        )

        # Then: 상태코드 400을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(
            response.json()['message'],
            '해당하는 메뉴가 없습니다.'
        )

    def test_yosigy_ticket_create_should_return_400_when_discounted_price_is_less_than_zero(self):
        """
        요식이 티켓 생성 API는 discounted_price가 0원 보다 작을 때,  400을 반환해야한다.
        """

        INVALID_DISCOUNTED_PRICE = -4000

        # Given: 유저는 로그인 상태이다 / 요시기 이벤트 생성 / 요식이 메뉴가 생성 / 유효하지않은 폼 데이터가 주어진다.
        self.client.login(
            username='yosigy_user',
            password='yosigy_password'
        )

        invalid_form_data_list = [
            {
                'yosigy_menu_id': self.yosigy_menu_jjajangmyun.id,
                'menu_id': self.jjajangmyun.id,
                'discounted_price': INVALID_DISCOUNTED_PRICE,
                'quantity': 1
            }
        ]

        # When: YosigyTicketCreateAPIView를 호출한다.
        response = self.client.post(
            path=reverse(
                'yosigy_api:yosigy_create_ticket_api',
                kwargs={'restaurant_id': self.restaurant.id}
            ),
            data=json.dumps(invalid_form_data_list),
            content_type='application/json:charset=utf-8;'
        )

        # Then: 상태코드 400을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )

        self.assertEqual(
            response.json()['error']['discounted_price'][0],
            '가격은 0원 이상 입니다.'
        )

    def test_yosigy_ticket_create_should_return_400_when_quantity_is_less_than_one_or_more_than_hundred(self):
        """
        요식이 티켓 생성 API는 메뉴의 quantity가 1 보다 작거나, 100 보다 크면,  400을 반환해야한다.
        """
        INVALID_QUANTITY = 101

        # Given: 유저는 로그인 상태이다 / 요시기 이벤트 생성 / 요식이 메뉴가 생성 / 유효하지 않음 폼 데이터가 주어진다.
        self.client.login(
            username='yosigy_user',
            password='yosigy_password'
        )

        invalid_form_data_list = [
            {
                'yosigy_menu_id': self.yosigy_menu_jjajangmyun.id,
                'menu_id': self.jjajangmyun.id,
                'discounted_price': self.yosigy_menu_jjajangmyun.discounted_price,
                'quantity': INVALID_QUANTITY
            }
        ]

        # When: YosigyTicketCreateApiView를 호출한다.
        response = self.client.post(
            path=reverse(
                'yosigy_api:yosigy_create_ticket_api',
                kwargs={'restaurant_id': self.restaurant.id}
            ),
            data=json.dumps(invalid_form_data_list),
            content_type='application/jsoncharset=utf-8;'
        )

        # Then: 상태코드 400을 반환한다. / 개수는 1~100개 까지 입력 가능합니다. 메세지를 출력합니다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(
            response.json()['error']['quantity'][0],
            '개수는 1~100 개 까지 입력 가능합니다.'
        )
