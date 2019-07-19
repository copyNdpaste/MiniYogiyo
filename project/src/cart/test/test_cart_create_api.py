from http import HTTPStatus
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from cart.models import Cart


User = get_user_model()


class CartAPIViewTestCase(TestCase):
    def setUp(self):
        '''
        유저 생성
        '''
        self.user = User.objects.create_user(
            username='thkwon',
            email='',
            password='hohoho123!',
        )
        response = self.client.get('/home/')
        self.csrf_token = response.cookies.get('csrftoken')

    def test_cart_crate_api_should_return_401_when_user_is_anonymous(self):
        '''
        Anonymous 유저가 접근했을 때, 401을 반환한다.
        '''
        # Given: user는 Anomymous 상태이다. valid_json_data가 주어진다.
        valid_json_data = json.dumps({'user': self.user.id})
        header = {'X-CSRFToken': self.csrf_token}

        # When: body에 유효한 json을 넣어서, CartCreateAPIView를 호출한다.
        response = self.client.post(
            '/api/cart/',
            data=valid_json_data,
            content_type='application/json',
            **header
        )

        # Then: 상태코드 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_cart_create_api_should_return_400_when_json_is_invalid(self):
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

        # When: body에 유효하지 않은 json을 넣어서, CartCreateAPIView를 호출한다.
        response = self.client.post(
            '/api/cart/',
            data=invalid_json_data,
            content_type='application/json',
            **header
        )

        # Then: 상태코드 400를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )

    def test_cart_create_api_should_return_201_when_form_is_valid(self):
        '''
        form이 유효하면, Cart를 생성하고, 201을 리턴한다.
        '''
        # Given: user는 로그인 상태이다. valid_json_data가 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        valid_json_data = json.dumps({'user': self.user.id})
        header = {"X-CSRFToken": self.csrf_token}

        # When: body에 form에 유효한 json을 포함하여, CartCreateAPIView를 호출한다.

        response = self.client.post(
            '/api/cart/',
            data=valid_json_data,
            content_type='application/json',
            **header
        )

        # Then: Cart가 생성되고, 상태코드 201을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.CREATED
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
        invalid_json_data = json.dumps({'user': 'not_integer_value'})
        header = {"csrftoken": self.csrf_token}

        # When: body에 form에 유효하지 않은 json을 포함하여, CartCreateAPIView를 호출한다.
        response = self.client.post(
            '/api/cart/',
            data=invalid_json_data,
            content_type='application/json',
            **header
        )

        # Then: 상태코드 400을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )

    def test_cart_create_api_should_return_400_when_user_have_cart(self):
        '''
        해당 유저가 이미 주문함을 가지고 있다면, 400 에러를 반환한다.
        '''
        # Given: 새로운 유저를 생성하고, 로그인 후, 이 유저는 주문함을 생성한 상태이다.
        already_have_cart_user = User.objects.create_user(
            username='already_have_cart_user',
            email='',
            password='cartuser123!',
        )
        self.client.login(
            username='already_have_cart_user',
            password='cartuser123!'
        )
        cart = Cart.objects.create(
            user=already_have_cart_user
        )
        already_have_cart_user_json_data = json.dumps({'user': cart.user.id})
        header = {"csrftoken": self.csrf_token}

        # When: body에 form에 유효하지 않은 json을 포함하여, CartCreateAPIView를 호출한다.
        response = self.client.post(
            '/api/cart/',
            data=already_have_cart_user_json_data,
            content_type='application/json',
            **header
        )

        # Then: 상태코드 400을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.BAD_REQUEST
        )
