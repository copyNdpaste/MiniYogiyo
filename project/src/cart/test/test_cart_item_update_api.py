from http import HTTPStatus
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from cart.models import Cart, CartItem
from menu.models import Menu
from restaurant.models import Restaurant


User = get_user_model()


class CartItemUpdateAPIViewTestCase(TestCase):
    def setUp(self):
        '''
        * 유저 생성
        * Cart 생성
        * 레스토랑 생성
        * 메뉴 2개 생성 - 짜장면, 짬뽕
        * Cart Item에 , 위 메뉴 2개 추가
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
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='짬뽕',
            detail='맛있는 짬뽕',
            price=7000,
            type='인기메뉴'
        )
        CartItem.objects.create(
            cart=self.cart,
            menu=self.jjajangmyun
        )
        CartItem.objects.create(
            cart=self.cart,
            menu=self.jjambbong
        )

    def test_cart_item_update_api_should_return_401_when_user_is_anonymous(self):
        '''
        Anonymous 유저가 접근했을 때 401을 반환한다.
        '''
        # Given: user는 Anonymous 상태이다. 유효한 json data가 주어진다.

        valid_json_data = [
            {
                'quantity': 1,
                'menu': self.jjajangmyun.id,
            },
            {
                'quantity': 2,
                'menu': self.jjambbong.id,
            }
        ]

        # When: 유효한 json을 data에 실어서 요청을 한다.
        response = self.client.put(
            '/api/cart/' + str(self.cart.id) + '/update/',
            content_type='application/json',
            data=valid_json_data
        )

        # Then: 상태코드 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_cart_item_update_api_should_return_400_when_you_send_invalid_json(self):
        '''
        유효하지 않은 json을 보내면, 400을 리턴한다.
        '''
        # Given: user는 로그인 상태이다. 유효하지 않은 json이 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        invalid_json_data = [
            {
                'quantity': 1,
                'menu': self.jjajangmyun.id,
                'invalid_field': 'invalid_data'
            },
            {
                'quantity': 2,
                'menu': self.jjambbong.id,
                'invalid_field': 'invalid_data'
            }
        ]

        # When: 유효하지않은 json을 data에 실어서 요청을 한다.
        response = self.client.put(
            '/api/cart/' + str(self.cart.id) + '/update/',
            content_type='application/json',
            data=invalid_json_data
        )

        # Then: 상태코드 400를 반환하고, '잘못된 요청 입니다.' 메세지를 나타낸다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(
            response.json()['message'],
            '잘못된 요청 입니다.'
        )

    def test_cart_item_update_api_should_return_400_when_you_send_invalid_value(self):
        '''
        json 형태는 유효하지만, 유효하지 않은 값(string)을 보내게 되면 400 에러를 발생시킨다.
        - 유효하지 않은 값 - quantity, menu 모두 int를 값을 받기 때문에, 여기선 string이라고 가정한다.
        '''

        # Given: user는 로그인 상태이다. json의 형태는 유효하지만, 유효하지 않은 값(string)이 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        string_data = "string"

        valid_json_data = [
            {
                'quantity': string_data,
                'menu': self.jjajangmyun.id
            },
            {
                'quantity': string_data,
                'menu': self.jjambbong.id
            }
        ]

        # When: 유효하지않은 json을 data에 실어서 요청을 한다.
        response = self.client.put(
            '/api/cart/' + str(self.cart.id) + '/update/',
            content_type='application/json',
            data=json.dumps(valid_json_data)
        )

        # Then: 상태코드 400를 반환하고, 폼이 유효하지 않습니다. , Enter a whole number. 에러메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(
            response.json()['message'],
            '폼이 유효하지 않습니다.'
        )
        self.assertEqual(
            response.json()['error']['quantity'][0],
            "Enter a whole number."
        )

    def test_cart_item_update_api_should_return_400_when_you_send_invalid_quantity_more_than_one_hundred(self):
        '''
        json 형태는 유효하지만, 100보다 큰 quantity 개수를 보내게 되면 400 에러를 발생시킨다.
        '''

        # Given: user는 로그인 상태이다. json의 형태는 유효하지만, 유효하지않은 quantity 값이 주어진다.( 100보다 큰 수)
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        invalid_quantity = 101

        valid_json_data = [
            {
                'quantity': invalid_quantity,
                'menu': self.jjajangmyun.id,
            },
            {
                'quantity': invalid_quantity,
                'menu': self.jjambbong.id,
            }
        ]

        # When: 유효하지않은 json을 data에 실어서 요청을 한다.
        response = self.client.put(
            '/api/cart/' + str(self.cart.id) + '/update/',
            content_type='application/json',
            data=json.dumps(valid_json_data)
        )

        # Then: 상태코드 400를 반환하고, quantity의 개수가 올바르지 않습니다 에러 메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(
            response.json()['error']['quantity'][0],
            'quantity의 개수가 올바르지 않습니다.'
        )

    def test_cart_item_update_api_should_return_400_when_you_send_invalid_quantity_less_than_one(self):
        '''
        json 형태는 유효하지만, 1보다 작은 quantity 개수를 보내게 되면 400 에러를 발생시킨다.
        '''

        # Given: user는 로그인 상태이다. json의 형태는 유효하지만, 유효하지않은 quantity 값이 주어진다.( 1보다 작은 수)
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        invalid_quantity = 0

        valid_json_data = [
            {
                'quantity': invalid_quantity,
                'menu': self.jjajangmyun.id,
            },
            {
                'quantity': invalid_quantity,
                'menu': self.jjambbong.id,
            }
        ]

        # When: 유효하지않은 json을 data에 실어서 요청을 한다.
        response = self.client.put(
            '/api/cart/' + str(self.cart.id) + '/update/',
            content_type='application/json',
            data=json.dumps(valid_json_data)
        )

        # Then: 상태코드 400를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(
            response.json()['error']['quantity'][0],
            'quantity의 개수가 올바르지 않습니다.'
        )

    def test_cart_item_update_api_should_return_200_when_you_send_valid_json(self):
        '''
        유효한 데이터를 보내고, 정상적으로 수정되면, 200을 리턴한다.
        '''

        # Given: user는 로그인 상태이다. 유효한 데이터가 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        valid_data = [
            {
                'quantity': 1,
                'menu': self.jjajangmyun.id
            },
            {
                'quantity': 2,
                'menu': self.jjambbong.id
            }

        ]

        # When: 유효한 json을 data에 실어서 요청을 한다.
        response = self.client.put(
            '/api/cart/' + str(self.cart.id) + '/update/',
            data=json.dumps(valid_data),
            content_type='application/json'
        )

        # Then: 상태코드 200을 반환한다. 총 개수는 3개이고, 메뉴가 성공적으로 추가되었습니다. 메뉴를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )
        self.assertEqual(
            response.json()['total_quantity'],
            3
        )
        self.assertEqual(
            response.json()['message'],
            '메뉴가 성공적으로 추가되었습니다.'
        )
