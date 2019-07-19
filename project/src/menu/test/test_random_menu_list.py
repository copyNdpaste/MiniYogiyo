from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from cart.models import Cart


class RandomMenuListAPIViewTestCase(TestCase):

    fixtures = [
        'restaurant.json',
        'category.json',
        'menu.json',
        'tastes.json'
    ]

    def setUp(self):
        """
        * fixture
            - category 생성
            - restaurant - 금룡
            - menu - 10개
            - tastes - 8개
        * 유저 생성
        * Cart 생성
        """

        self.user = User.objects.create_user(
            username='thkwon',
            email='',
            password='hohoho123!',
        )
        self.cart = Cart.objects.create(
            user=self.user
        )

    def test_random_menu_list_api_should_return_401_when_user_is_anonymous(self):
        """
        비 로그인 상태이면 401을 반환한다.
        """
        # Given: user는 비 로그인 상태이다.

        # When: RandomMenuListAPI를 호출한다.
        response = self.client.get(
            reverse('menu_api:random_menu_list_api')
        )

        # Then: 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_random_menu_list_api_should_return_200_when_menu_with_taste_of_user_quantity_is_more_than_three(self):
        """
        주문자 취향에 맞는 메뉴가 3개 이상이면, 200을 반환한다.
        """
        # Given: 메뉴 10개가 존재한다.(fixture를 통해 미리 생성) 유저의 취향은 #매운맛(1)과 #국물(3) 이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        TASTE_SPICY = 1
        TASTE_SOUP = 3
        self.user.tastes.add(TASTE_SPICY, TASTE_SOUP)

        # When: RandomMenuListAPI를 호출한다.
        response = self.client.get(
            reverse('menu_api:random_menu_list_api')
        )

        # Then: 주문자 취향에 맞는 메뉴 중 3개를 랜덤으로 선택한다. / 200을 반환한다.
        RESULT_RANDOM_MENU_COUNT = 3

        self.assertEqual(
            len(response.json()['menu']),
            RESULT_RANDOM_MENU_COUNT
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

    def test_random_menu_list_api_should_return_200_when_menu_with_taste_of_user_quantity_is_two(self):
        """
        주문자 취향에 맞는 메뉴가 2개 이면, 200을 반환한다.
        """

        # Given: 메뉴 10개가 존재한다.(fixture를 통해 미리 생성) 유저의 취향은 #밥류(7) 이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        TASTE_RICE = 7
        self.user.tastes.add(TASTE_RICE)

        # When: RandomMenuListAPI를 호출한다.
        response = self.client.get(
            reverse('menu_api:random_menu_list_api')
        )

        # Then: 주문자 취향에 맞는 메뉴의 개수는 2개이다. / 200을 반환한다.
        RESULT_RANDOM_MENU_COUNT = 2

        self.assertEqual(
            len(response.json()['menu']),
            RESULT_RANDOM_MENU_COUNT
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

    def test_random_menu_list_api_should_return_200_when_menu_with_taste_of_user_quantity_is_one(self):
        """
        주문자 취향에 맞는 메뉴가 1개 이면, 200을 반환한다.
        """

        # Given: 메뉴 10개가 존재한다.(fixture를 통해 미리 생성) 유저의 취향은 #25000원이상(5) 이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        TASTE_MORE_THAN_25000_WON = 5
        self.user.tastes.add(TASTE_MORE_THAN_25000_WON)

        # When: RandomMenuListAPI를 호출한다.
        response = self.client.get(
            reverse('menu_api:random_menu_list_api')
        )

        # Then: 주문자 취향에 맞는 메뉴의 개수는 1개이다. / 200을 반환한다.
        RESULT_RANDOM_MENU_COUNT = 1

        self.assertEqual(
            len(response.json()['menu']),
            RESULT_RANDOM_MENU_COUNT
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

    def test_random_menu_list_api_should_return_404_when_user_cart_is_not_exists(self):
        """
        주문자에 해당하는 Cart가 존재하지 않으면 404를 반환한다
        """

        # Given: 주문자 계정을 생성하고, 로그인을 한다. cart는 지정하지 않는다.
        user_do_not_have_cart = User.objects.create_user(
            username='user_do_not_have_cart',
            email='',
            password='passwd123!',
        )
        self.client.login(
            username=user_do_not_have_cart.username,
            password='passwd123!'
        )

        # When: RandomMenuListAPI를 호출한다.
        response = self.client.get(
            reverse('menu_api:random_menu_list_api')
        )

        # Then: 404를반환한다. / 현재 주문표가 존재하지 않습니다. 메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(
            response.json()['message'],
            "현재 주문표가 존재하지 않습니다."
        )

    def test_random_menu_list_api_should_return_404_when_user_does_not_choice_any_taste(self):
        """
        주문자가 어떤 취향도 선택하지않았을 때, 404를 반환한다.
        """

        # Given: 주문자가 계정을 생성하고, 주문자가 로그인을 한다. /  취향 선택은 선택하지 않은 상태이다.
        user_does_not_choice_any_taste = User.objects.create_user(
            username='user_does_not_choice_any_taste',
            email='',
            password='passwd123!',
        )
        self.cart = Cart.objects.create(
            user=user_does_not_choice_any_taste
        )
        self.client.login(
            username=user_does_not_choice_any_taste.username,
            password='passwd123!'
        )

        # When: RandomMenuListAPI를 호출한다.
        response = self.client.get(
            reverse('menu_api:random_menu_list_api')
        )

        # Then: 404를반환한다. / 선택하신 취향이 존재하지않습니다. 'My Page'에서 취향을 선택해주세요. 메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(
            response.json()['message'],
            "선택하신 취향이 존재하지않습니다. 'My Page'에서 취향을 선택해주세요."
        )

    def test_random_menu_list_api_should_return_404_when_user_choices_taste_but_that_menu_quantity_is_zero(self):
        """
        주문자 취향에 해당하는 메뉴가 0개 이면, 404를 반환한다.
        """

        # Given: 메뉴 10개가 존재한다.(fixture를 통해 미리 생성) 유저의 취향은 #50000원이상(9) 이다.
        self.client.login(
            username='thkwon',
            password='hohoho123!'
        )

        TASTE_MORE_THAN_50000_WON = 9
        self.user.tastes.add(TASTE_MORE_THAN_50000_WON)

        # When: RandomMenuListAPI를 호출한다.
        response = self.client.get(
            reverse('menu_api:random_menu_list_api')
        )

        # Then: 404를반환한다. / 취향에 해당하는 메뉴가 없습니다.메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(
            response.json()['message'],
            "취향에 해당하는 메뉴가 없습니다."
        )
