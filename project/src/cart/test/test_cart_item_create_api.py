from http import HTTPStatus
import json

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from cart.models import Cart, CartItem
from menu.models import Menu
from restaurant.models import Restaurant


User = get_user_model()


class CartItemCreateAPIViewTestCase(TestCase):
    def setUp(self):
        '''
        * 유저 생성
        * Cart 생성
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
            name="금룡",
            owner="권태형",
            title="금룡 한양대점",
            estimated_delivery_time="2019-04-29 22:50",
            operation_start_hour="2019-04-29 12:00",
            operation_end_hour="2019-04-29 20:00",
            min_order_price=15000,
            delivery_charge=2000,
        )
        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            name="짜장면",
            detail="맛있는 짜장면",
            price=8000,
            type="인기메뉴"
        )

        response = self.client.get('/home/')
        self.csrf_token = response.cookies.get('csrftoken')
        self.client = Client(enforce_csrf_checks=False)
        self.client.cookies['csrftoken'] = self.csrf_token

    def test_cart_item_create_api_should_return_401_when_user_is_anonymous(self):
        '''
        Anonymous 유저가 접근했을 때 401을 반환한다.
        '''
        # Given: user는 Anonymous 상태이다. valid_json_data가 주어진다.
        valid_json_data = json.dumps({'user': self.user.id})

        # When: body에 유효한 json을 넣어서, CartItemListCreateAPIView 호출한다.
        response = self.client.post(
            '/api/cart/' + str(self.cart.id) + '/',
            data=valid_json_data,
            content_type='application/json',
            **{'X-CSRFTOKEN': self.csrf_token}

        )

        # Then: 상태코드 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_cart_item_create_api_should_return_400_when_json_is_invalid(self):
        '''
        request body json이 유효하지 않을 때, 400을 리턴한다.
        '''
        # Given: user는 로그인 상태이다. invalid_json_data가 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        invalid_json_data = "{'invalid_json_data': 'data'}"
        header = {"X-CSRFToken": self.csrf_token}

        # When: body에 유효하지 않은 json을 넣어서, CartItemListCreateAPIView 호출한다.
        response = self.client.post(
            '/api/cart/' + str(self.cart.id) + '/',
            data=invalid_json_data,
            content_type='application/json',
            **header
        )

        # Then: 상태코드 400를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )

    def test_cart_item_create_api_should_return_201_when_form_is_valid(self):
        '''
        form이 유효하면, CartItem를 생성하고, 201을 리턴한다.
        '''
        # Given: 레스토랑 생성 / 메뉴(짜장면) 생성/ 로그인이 되었고, 유효한 json이 주어진다.

        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        valid_json_data = json.dumps({
            'cart': str(self.cart.id),
            'menu': self.jjajangmyun.id
        })
        header = {"X-CSRFToken": self.csrf_token}

        # When: body에 form에 유효한 json을 포함하여, CartItemListCreateAPIView 호출한다.
        response = self.client.post(
            '/api/cart/' + str(self.cart.id) + '/',
            data=valid_json_data,
            content_type='application/json',
            **header
        )

        # Then: Cart안에 CartItem(메뉴)가 생성되고,, 상태코드 201을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.CREATED
        )

    def test_cart_item_create_api_should_return_400_when_added_menu_is_duplicated(self):
        '''
        해당 Cart에 메뉴가 이미 있다면, 400을 리턴한다.
        '''
        # Given: 레스토랑 생성 / 메뉴(짜장면) 생성/ 로그인이 되었고, Cart안에 짜장면 1개를 미리 추가한 상태에서 유효한 json 데이터(짜장면이 있는)가 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        CartItem.objects.create(
            cart=self.cart,
            menu=self.jjajangmyun
        )
        cart_item_json_data = json.dumps({
            'cart': str(self.cart.id),
            'menu': self.jjajangmyun.id
        })
        header = {"csrftoken": self.csrf_token}

        # When: body에 form에 유효한 json을 포함하여, CartItemListCreateAPIView 호출한다.
        response = self.client.post(
            '/api/cart/' + str(self.cart.id) + '/',
            data=cart_item_json_data,
            content_type='application/json',
            **header
        )

        # Then: 짜장면이 중복이기 때문에, 상태코드 400을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )

    def test_cart_item_create_api_should_return_400_when_form_is_invalid(self):
        '''
        form이 유효하지 않으면, 400을 리턴한다.
        '''
        # Given: user는 로그인 상태이다. 형식은 uuid, int이고, 유효하지않은 json 데이터가 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        invalid_json_data = json.dumps({
            'cart': '12345678-1234-1234-1234-123456123456',
            'menu': 0000
        })
        header = {"csrftoken": self.csrf_token}

        # When: body에 form에 유효하지 않은 json을 포함하여, CartItemListCreateAPIView 호출한다.
        response = self.client.post(
            '/api/cart/' + str(self.cart.id) + '/',
            data=invalid_json_data,
            content_type='application/json',
            **header
        )

        # Then: 상태코드 400을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
