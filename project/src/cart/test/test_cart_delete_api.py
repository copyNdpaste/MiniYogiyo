from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from cart.models import Cart


User = get_user_model()


class CartDeleteAPIViewTestCase(TestCase):
    def setUp(self):
        '''
        * 유저 생성
        * 카트 생성
        '''
        self.user = User.objects.create_user(
            username='thkwon',
            email='',
            password='hohoho123!',
        )
        self.cart = Cart.objects.create(
            user=self.user
        )

    def test_cart_delete_api_should_return_401_when_user_is_anonymous(self):
        '''
        Anonymous 유저가 접근했을 때 401을 반환한다.
        '''
        # Given: user는 Anonymous 상태이다.

        # When: 정상적인 delete url을 요청한다.
        response = self.client.delete(
            '/api/cart/' + str(self.cart.id) + '/delete/',
            content_type='application/json',
        )
        # Then: 로그인이 되어있지 않기 때문에, 상태코드 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_cart_delete_api_should_return_200_when_cart_you_want_to_delete_exist(self):
        '''
        삭제하려는 Cart가 있으면, 삭제하고, 200을 반환한다.
        '''
        # Given: user는 로그인 상태이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        # When: Cart를 삭제하는 요청을 한다.
        response = self.client.delete(
            '/api/cart/' + str(self.cart.id) + '/delete/',
            content_type='application/json',
        )
        # Then: 성공적으로 삭제되면, 상태코드 200를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )
        self.assertFalse(
            Cart.objects.filter(
                id=self.cart.id
            ).exists()
        )

    def test_cart_delete_api_should_return_404_when_cart_you_want_to_delete_not_exist(self):
        '''
        삭제하려는 Cart가 없으면 404를 반환한다.
        '''
        # Given: user는 로그인 상태이고, 존재하지 않는 cart_id 값이 주어진다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )
        not_exist_cart = '1234569c-ae86-4781-adce-21655e3561f0'
        # When: 생성되지 않은 menu의 id 값을 url에 입력 한다. - 1000
        response = self.client.delete(
            '/api/cart/' + not_exist_cart + '/delete/',
            content_type='application/json',
        )
        # Then: 상태코드 404를 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
