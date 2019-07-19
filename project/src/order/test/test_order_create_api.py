from http import HTTPStatus
import json

from django.test import TestCase
from django.shortcuts import reverse

from accounts.models import User
from cart.models import Cart
from category.models import Category
from coupon.models import GiftCoupon
from menu.models import Menu
from restaurant.models import Restaurant


class OrderCreateAPIViewTestCase(TestCase):
    def setUp(self):
        '''
        * 주문자 생성
        * 카테고리 생성
        * 레스토랑 생성
        * 메뉴(짬뽕, 짜장면) 생성
        * 주문자에 해당하는 주문표 생성
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
            estimated_delivery_time='22:50',
            operation_start_hour='12:00',
            operation_end_hour='20:00',
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
        self.cart = Cart.objects.create(
            user=self.user
        )
        self.sender_name = 'sender_name',
        self.sender_password = 'sender_password'
        self.sender = User.objects.create_user(
            username=self.sender_name, password=self.sender_password
        )
        self.coupon_code = self.send_coupon()

    def send_coupon(self):
        self.client.login(username=self.sender_name, password=self.sender_password)

        gift_coupon_data = {
            'receiver_name': '홍길동',
            'receiver_email': 'test190508@gmail.com',
            'receiver_phone': '',
            'sender_msg': '선물입니다.^^',
            'price': '10000',
        }

        self.client.post(
            path=reverse('create_gift_coupon_api'),
            data=gift_coupon_data,
            content_type='application/json:charset=utf-8;'
        )
        self.client.logout()

        coupon_code = (GiftCoupon.objects
                       .filter(sender__username=self.sender_name)
                       .order_by('-created_time')[0].coupon_code)
        return coupon_code

    def register_coupon(self, coupon_code):

        self.client.post(
            path=reverse('register_gift_coupon_api'),
            data={
                'coupon_code': coupon_code
            },
            content_type='application/json:charset=utf-8;'
        )

        gift_coupon = (GiftCoupon.objects
                       .get(usergiftcoupon__is_owner=True,
                            usergiftcoupon__user=self.user.id,
                            coupon_code=coupon_code))
        return gift_coupon

    def test_order_crate_api_should_return_401_when_user_is_anonymous(self):
        '''
        Anonymous 유저가 접근했을 때, 401을 반환한다.
        '''
        # Given: user는 Anomymous 상태이다. valid_json_data가 주어진다.
        # self.client.login(
        #     username='thkwon',
        #     password='hohoho123!'
        # )

        request_body_data = {
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "cart": str(self.cart.id),
            "total_price": self.cart.total_price + self.restaurant.delivery_charge,
            "address": "주소 입니다.",
            "address_detail": "디테일 주소입니다.",
            "phone_num": "010-7331-4120",
            "payment_status": 1
        }
        valid_json_data = json.dumps(request_body_data)

        # When: body에 유효한 json_data를 넣어서, OrderCreateDetailAPIView를 호출한다.
        response = self.client.post(
            '/api/order/',
            data=valid_json_data,
            content_type='application/json',
        )

        # Then: 상태코드 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_order_create_api_should_return_400_when_json_is_invalid(self):
        '''
        request body으로 보낸 json 데이터가 유효하지 않을 때, 400을 리턴한다.
        '''
        # Given: user는 로그인 상태이다. invalid_json_data가 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        invalid_json_data = "{'invalid_json_data': 'not json but string'}"

        # When: body에 유효하지 않은 json을 넣어서, OrderCreateDetailAPIView를 호출한다.
        response = self.client.post(
            '/api/order/',
            data=invalid_json_data,
            content_type='application/json'
        )

        # Then: 상태코드 400를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )

    def test_order_create_api_should_return_201_when_form_is_valid(self):
        '''
        form이 유효하면, Order를 생성하고, 201을 리턴한다.
        '''
        # Given: user는 로그인 상태이다. valid_json_data가 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        request_body_data = {
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "cart": str(self.cart.id),
            "total_price": self.cart.total_price + self.restaurant.delivery_charge,
            "address": "주소 입니다.",
            "address_detail": "디테일 주소입니다.",
            "phone_num": "010-7331-4120",
            "payment_status": 1
        }
        valid_json_data = json.dumps(request_body_data)

        # When: body에 form에 유효한 json을 포함하여, OrderCreateDetailAPIView를 호출한다.
        response = self.client.post(
            '/api/order/',
            data=valid_json_data,
            content_type='application/json',
        )

        # Then: Cart가 생성되고, 상태코드 201을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.CREATED
        )
        self.assertEqual(
            response.json()['message'],
            '주문에 성공하였습니다.'
        )

    def test_cart_create_api_should_return_400_when_form_is_invalid(self):
        '''
        form이 유효하지 않으면, 400을 리턴한다.
        '''
        # Given: user는 로그인 상태이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        invalid_request_body_data = {
            "invalid_form_data": "invalid_form_data",
        }
        invalid_data = json.dumps(invalid_request_body_data)

        # When: body에 form에 유효하지 않은 json을 포함하여, OrderCreateDetailAPIView를 호출한다.
        response = self.client.post(
            '/api/order/',
            data=invalid_data,
            content_type='application/json',
        )

        # Then: 상태코드 400을 반환하고, 폼이 유효하지 않습니다. 메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(
            response.json()['message'],
            '폼이 유효하지 않습니다.'
        )

    def test_order_create_api_should_return_400_when_number_dividing_bar_count_is_not_two(self):
        '''
        핸드폰 번호를 나누는 bar의 개수가 2개가 아니면 올바르지 않은 폰번호로써, 에러를 리턴한다.
        '''

        # Given: user는 로그인 상태이다. 유효하지않은 dividing_bar_count_is_not_two가 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        dividing_bar_count_is_not_two = "010-73-3-4120"
        request_body_data = {
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "cart": str(self.cart.id),
            "total_price": self.cart.total_price + self.restaurant.delivery_charge,
            "address": "주소 입니다.",
            "address_detail": "디테일 주소입니다.",
            "phone_num": dividing_bar_count_is_not_two,
            "payment_status": 1
        }
        valid_json_data = json.dumps(request_body_data)

        # When: body에 form에 유효한 json을 포함하여, OrderCreateDetailAPIView를 호출한다.
        response = self.client.post(
            '/api/order/',
            data=valid_json_data,
            content_type='application/json',
        )

        # Then: 상태코드 400을 반환하고, 올바르지 않은 폰 번호 입니다 메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(
            response.json()['error']['phone_num'][0],
            '올바르지 않은 폰 번호 입니다.'
        )

    def test_order_create_api_should_return_400_when_phone_num_first_part_is_not_010(self):
        '''
        핸드폰 번호를 맨 앞부분이 010이 아니면,  올바르지 않은 폰번호로써, 에러를 리턴한다.
        '''
        # Given: user는 로그인 상태이다. 유효하지않은 first_part_is_not_010_data가 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        first_part_is_not_010_data = "011-7331-4120"
        request_body_data = {
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "cart": str(self.cart.id),
            "total_price": self.cart.total_price + self.restaurant.delivery_charge,
            "address": "주소 입니다.",
            "address_detail": "디테일 주소입니다.",
            "phone_num": first_part_is_not_010_data,
            "payment_status": 1
        }
        valid_json_data = json.dumps(request_body_data)

        # When: body에 form에 유효한 json을 포함하여, OrderCreateDetailAPIView를 호출한다.
        response = self.client.post(
            '/api/order/',
            data=valid_json_data,
            content_type='application/json',
        )

        # Then: 상태코드 400을 반환하고, 올바르지 않은 폰 번호 입니다 메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(
            response.json()['error']['phone_num'][0],
            '올바르지 않은 폰 번호 입니다.'
        )

    def test_order_create_api_should_return_201_when_valid_coupon_is_used(self):
        # Given : user login & user register coupon & valid data has gift_coupon
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        gift_coupon = self.register_coupon(self.coupon_code)
        total_price = 10000

        valid_data = {
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "cart": str(self.cart.id),
            "total_price": total_price,
            "address": "주소 입니다.",
            "address_detail": "디테일 주소입니다.",
            "phone_num": "010-1111-2222",
            "payment_status": 1,
            "gift_coupon": gift_coupon.id
        }

        # When : user is trying to call OrderCreateDetailAPIView
        response = self.client.post(
            '/api/order/',
            data=valid_data,
            content_type='application/json',
        )

        # Then : response should have HTTPStatus.Created
        self.assertEqual(
            response.status_code,
            HTTPStatus.CREATED
        )
        # Then: total price is equal to total_price - coupon_price
        self.assertEqual(
            response.json()['total_price'],
            total_price-gift_coupon.price
        )

    def test_order_create_api_should_return_400_when_invalid_coupon_is_used(self):
        # Given : user login & user register coupon
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        gift_coupon = self.register_coupon(self.coupon_code)

        # Given :invalid data has unavailable coupon because total price is not over coupon's price
        total_price = self.restaurant.delivery_charge
        invalid_json_data = {
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "cart": str(self.cart.id),
            "total_price": total_price,
            "address": "주소 입니다.",
            "address_detail": "디테일 주소입니다.",
            "phone_num": "010-1111-2222",
            "payment_status": 1,
            "gift_coupon": gift_coupon.id
        }

        # When : user is trying to call OrderCreateDetailAPIView
        response = self.client.post(
            '/api/order/',
            data=invalid_json_data,
            content_type='application/json',
        )

        # Then : response should have HTTPStatus.BAD_REQUEST & message '폼이 유효하지 않습니다.'
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(
            response.json()['message'],
            '폼이 유효하지 않습니다.'
        )
