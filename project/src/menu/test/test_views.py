from http import HTTPStatus

from django.test import TestCase, RequestFactory
from django.urls import reverse

from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from category.models import Category
from order.models import Order
from restaurant.models import Restaurant
from menu.models import Menu
from grid.models import Grid

User = get_user_model()


class MenuTestClass(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

        self.user1 = User.objects.create_user(username='mike', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user2 = User.objects.create_user(username='jake', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user3 = User.objects.create_user(username='fake', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user4 = User.objects.create_user(username='lake', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user5 = User.objects.create_user(username='cake', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user6 = User.objects.create_user(username='cake2', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user7 = User.objects.create_user(username='cake3', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user8 = User.objects.create_user(username='cake4', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user9 = User.objects.create_user(username='cake5', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user10 = User.objects.create_user(username='cake6', email='', password='2',
                                              address='서울시 서초구 서초2동 사랑의 교회 1300호')
        self.user_without_addr = User.objects.create_user(username='james', email='', password='1')
        self.user_without_dong = User.objects.create_user(username='ajax', email='', password='1',
                                                          address='서울시 서초구 100호')
        self.user_without_x_y_dong = User.objects.create_user(username='차이니즈', email='', password='1',
                                                              address='서울시 서초구 베이징3동')
        self.user_with_wrong_x_y = User.objects.create_user(username='xy오류', email='', password='1',
                                                            address='서울시 서초구 서초9동')
        self.user_with_wrong_weather = User.objects.create_user(username='abc', email='', password='1',
                                                            address='서울시 서초구 서초2동')
        self.restaurant = Restaurant.objects.create(
            name='굽내치킨', title='굽내치킨-서초점',
            min_order_price=10000, delivery_charge=1000, estimated_delivery_time='20:00',
            operation_start_hour='11:00', operation_end_hour='20:00', )
        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            name='볼케이노',
            detail='매콤한 맛입니다.',
            price=20000,
            type='양념류',
            img='test.jpg',
        )
        self.menu2 = Menu.objects.create(
            restaurant=self.restaurant,
            name='갈비천왕',
            detail='갈비 맛입니다.',
            price=20000,
            type='양념류',
            img='test.jpg',
        )
        self.menu3 = Menu.objects.create(
            restaurant=self.restaurant,
            name='허니멜로',
            detail='꿀 맛입니다.',
            price=20000,
            type='양념류',
            img='test.jpg',
        )
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart2 = Cart.objects.create(user=self.user2)
        self.cart3 = Cart.objects.create(user=self.user3)
        self.cart4 = Cart.objects.create(user=self.user4)
        self.cart5 = Cart.objects.create(user=self.user5)
        self.cart6 = Cart.objects.create(user=self.user6)
        self.cart7 = Cart.objects.create(user=self.user7)
        self.cart8 = Cart.objects.create(user=self.user8)
        self.cart9 = Cart.objects.create(user=self.user9)
        self.cart10 = Cart.objects.create(user=self.user10)
        self.cart_without_user_addr = Cart.objects.create(user=self.user_without_addr)
        self.cart_item1 = CartItem.objects.create(menu=self.menu, cart=self.cart1, quantity=1)
        self.cart_item2 = CartItem.objects.create(menu=self.menu, cart=self.cart2, quantity=2)
        self.cart_item3 = CartItem.objects.create(menu=self.menu, cart=self.cart3, quantity=3)
        self.cart_item4 = CartItem.objects.create(menu=self.menu2, cart=self.cart4, quantity=4)
        self.cart_item5 = CartItem.objects.create(menu=self.menu2, cart=self.cart5, quantity=5)
        self.cart_item6 = CartItem.objects.create(menu=self.menu2, cart=self.cart6, quantity=6)
        self.cart_item7 = CartItem.objects.create(menu=self.menu3, cart=self.cart7, quantity=7)
        self.cart_item8 = CartItem.objects.create(menu=self.menu3, cart=self.cart8, quantity=8)
        self.cart_item9 = CartItem.objects.create(menu=self.menu3, cart=self.cart9, quantity=9)
        self.cart_item10 = CartItem.objects.create(menu=self.menu3, cart=self.cart10, quantity=10)


        self.cart_item_without_user_addr = CartItem.objects.create(menu=self.menu, cart=self.cart_without_user_addr, quantity=1)
        self.category = Category.objects.create(name='치킨', img='restaurant/chicken.jpg')
        self.category_weather = Category.objects.create(id=15, name='날씨별 추천')
        self.grid1 = Grid.objects.create(
            name='서초2동',
            x=61,
            y=125,
        )
        self.grid2 = Grid.objects.create(
            name='서초9동',
            x=32767,
            y=32767,
        )

    def test_menu_detail_page_should_be_open_on_request(self):
        '''
        메뉴 클릭 시 메뉴에 대한 상세 페이지 열기
        '''
        # Given
        url = reverse("menu:menu_detail", kwargs={
            'category_id': self.category.id,
            'restaurant_id': self.restaurant.id,
            'menu_id': self.menu.id,
        })
        # When
        response = self.client.get(url)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_menu_list_api_should_return_datas_on_valid_request(self):
        '''
        유효한 restaurant id 보낼 경우 데이터 응답
        '''
        # Given
        url = reverse("menu_api:menu_list_api", kwargs={
            'category_id': self.category.id,
            'restaurant_id': self.restaurant.id,
        })
        # When
        response = self.client.get(url)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_menu_detail_api_should_return_datas_on_valid_request(self):
        '''
        유효한 menu id 보낼 경우 데이터 응답
        '''
        # Given
        kwargs = {
            'category_id': self.category.id,
            'restaurant_id': self.restaurant.id,
            'menu_id': self.menu.id,
        }
        self.client.login(username='mike', password='2')
        # When
        response = self.client.get(reverse("menu_api:menu_detail_api", kwargs=kwargs))
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_menu_list_api_for_weather_should_return_datas_on_valid_request(self):
        '''
        사용자 로그인 성공, 주소 존재, 동 정보 존재, 동에 대한 x, y 좌표 존재, 기상청 API 응답 성공
        '''
        # Given
        kwargs = {
            'category_id': self.category_weather.id,
        }
        self.client.login(username='mike', password='2')
        self.order_weather_1 = Order.objects.create(
            user=self.user1,
            cart=self.cart1,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=0,
            weather=1,
        )
        self.order_weather_2 = Order.objects.create(
            user=self.user2,
            cart=self.cart2,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=0,
            weather=2,
        )
        self.order_weather_3 = Order.objects.create(
            user=self.user3,
            cart=self.cart3,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=0,
            weather=3,
        )
        self.order_weather_4 = Order.objects.create(
            user=self.user4,
            cart=self.cart4,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=0,
            weather=4,
        )
        # When
        response = self.client.get(reverse('menu_api:menu_list_api', kwargs=kwargs))
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_menu_list_api_for_weather_should_return_UNAUTHORIZED_on_userless_request(self):
        '''
        AnonymousUser인 경우 401 반환
        '''
        # Given
        kwargs = {
            'category_id': self.category_weather.id,
        }
        # When
        response = self.client.get(reverse("menu_api:menu_list_api", kwargs=kwargs))
        # Then
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_menu_list_api_for_weather_should_return_BAD_REQUEST_on_addressless_request(self):
        '''
        사용자 계정은 있지만 주소가 없는 경우 400 반환
        '''
        # Given
        kwargs = {
            'category_id': self.category_weather.id,
        }
        self.client.login(username='james', password='1')
        # When
        response = self.client.get(reverse('menu_api:menu_list_api', kwargs=kwargs))
        # Then
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_menu_list_api_for_weather_should_return_BAD_REQUEST_on_dongless_request(self):
        '''
        사용자 주소의 동이 없는 경우 400 반환
        '''
        # Given
        kwargs = {
            'category_id': self.category_weather.id,
        }
        self.client.login(username='ajax', password='1')
        # When
        response = self.client.get(reverse('menu_api:menu_list_api', kwargs=kwargs))
        # Then
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_menu_list_api_for_weather_should_return_BAD_REQUEST_on_xygridless_request(self):
        '''
        Grid 테이블에서 사용자의 동에 대한 x, y 좌표가 없는 경우 400 반환
        '''
        # Given
        kwargs = {
            'category_id': self.category_weather.id,
        }
        self.client.login(username='차이니즈', password='1')
        # When
        response = self.client.get(reverse('menu_api:menu_list_api', kwargs=kwargs))
        # Then
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_menu_list_api_for_weather_should_return_INTERNAL_SERVER_ERROR_when_meteorological_administration_return_err(
            self):
        '''
        기상청 API 응답에 문제가 있는 경우 500 반환, 기상청에 직접적으로 문제가 있는지 판단하기 어려우므로 x,y 좌표를 큰 값으로 줘서 에러 응답을 만듦.
        '''
        # Given
        kwargs = {
            'category_id': self.category_weather.id,
        }
        self.order_weather_1 = Order.objects.create(
            user=self.user1,
            cart=self.cart1,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=0,
            weather=1,
        )
        self.order_weather_2 = Order.objects.create(
            user=self.user1,
            cart=self.cart2,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=0,
            weather=2,
        )
        self.order_weather_3 = Order.objects.create(
            user=self.user1,
            cart=self.cart3,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=0,
            weather=3,
        )
        self.order_weather_4 = Order.objects.create(
            user=self.user1,
            cart=self.cart4,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=0,
            weather=4,
        )
        self.client.login(username='xy오류', password='1')
        # When
        response = self.client.get(reverse('menu_api:menu_list_api', kwargs=kwargs))
        # Then
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_return_OK_when_no_order_related_with_weather(self):
        '''
        날씨와 관계 있는 잘 팔린 메뉴가 없는 경우 200 반환
        '''
        # Given
        kwargs = {
            'category_id': self.category_weather.id,
        }
        self.order1 = Order.objects.create(
            user=self.user2,
            cart=self.cart2,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=1,
        )
        self.order2 = Order.objects.create(
            user=self.user2,
            cart=self.cart2,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=2,
        )
        self.client.login(username='mike', password='2')
        # When
        response = self.client.get(reverse("menu_api:menu_list_api", kwargs=kwargs))
        # Then
        message = response.json()['message']
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(message, '날씨에 따라 잘 팔린 메뉴가 없습니다.')

    def test_return_OK_when_request(self):
        '''
        정상 동작 시 OK
        '''
        # Given
        kwargs = {
            'category_id': self.category_weather.id,
        }
        self.client.login(username='mike', password='2')
        self.order1 = Order.objects.create(
            user=self.user1,
            cart=self.cart1,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=1,
        )
        self.order2 = Order.objects.create(
            user=self.user2,
            cart=self.cart2,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=1,
        )
        self.order3 = Order.objects.create(
            user=self.user3,
            cart=self.cart3,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=2,
        )
        self.order4 = Order.objects.create(
            user=self.user4,
            cart=self.cart4,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=2,
        )
        self.order5 = Order.objects.create(
            user=self.user5,
            cart=self.cart5,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=3,
        )
        self.order6 = Order.objects.create(
            user=self.user6,
            cart=self.cart6,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=3,
        )
        self.order7 = Order.objects.create(
            user=self.user7,
            cart=self.cart7,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=3,
        )
        self.order8 = Order.objects.create(
            user=self.user8,
            cart=self.cart8,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=3,
        )
        self.order9 = Order.objects.create(
            user=self.user9,
            cart=self.cart9,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=4,
        )
        self.order10 = Order.objects.create(
            user=self.user10,
            cart=self.cart10,
            restaurant=self.restaurant,
            address='서울시 서초구 서초2동',
            status=0,
            delivery_status=1,
            weather=4,
        )
        # When
        response = self.client.get(reverse('menu_api:menu_list_api', kwargs=kwargs))
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)
