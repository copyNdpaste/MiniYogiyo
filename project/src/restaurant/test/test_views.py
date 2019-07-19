from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from category.models import Category
from restaurant.models import Restaurant


class RestaurantTestClass(TestCase):
    def setUp(self):
        self.category=Category.objects.create(name='치킨',img='restaurant/chicken.jpg')
        self.restaurant=Restaurant.objects.create(
            name='굽내치킨',title='굽내치킨-서초점', estimated_delivery_time='2019-01-01 00:20',
            min_order_price=10000, delivery_charge=1000, operation_end_hour='2019-01-01 10:00',
            operation_start_hour='2019-01-01 10:00', )

    def test_restaurant_detail_page_should_be_opened_on_request(self):
        '''
        category id를 보낼 시 레스토랑 상세 페이지 열기
        '''
        # Given
        url = reverse("restaurant:restaurant_detail", kwargs={
            'category_id': self.category.id, 'restaurant_id': self.restaurant.id
        })
        # When
        response = self.client.get(url)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_restaurant_detail_api_should_return_datas_on_valid_request(self):
        '''
        유효한 restaurant id 보낼 시 레스토랑에 관한 데이터 응답하기
        '''
        # Given
        url = reverse("restaurant_api:restaurant_detail_api", kwargs={
            'category_id': self.category.id, 'restaurant_id': self.restaurant.id
        })
        # When
        response = self.client.get(url)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_restaurant_detail_api_should_return_404_on_invalid_request(self):
        '''
        유효하지 않은 restaurant id 보낼 시 404 에러 출력하기
        '''
        # Given
        not_exist_id = 99999
        url = reverse("restaurant_api:restaurant_detail_api", kwargs={
            'category_id': not_exist_id, 'restaurant_id': not_exist_id
        })
        # When
        response = self.client.get(url)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class SubscribeTestCase(TestCase):
    def setUp(self):
        self.username = 'mypage_user'
        self.password = 'mypage_password!'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.restaurant = Restaurant.objects.create(
            name='굽내치킨', title='굽내치킨-서초점', estimated_delivery_time='00:20',
            min_order_price=10000, delivery_charge=1000, operation_end_hour='10:00',
            operation_start_hour='10:00', )

    def test_return_OK_when_subscribe_success(self):
        '''
        로그인 유저가 레스토랑 구독 시 성공 반환
        '''
        # Given
        self.client.login(username=self.username, password=self.password)
        self.user.subscribed_restaurants.set = self.restaurant
        self.user.save()
        url = reverse("restaurant_api:restaurant_subscribe_api", kwargs={
            'restaurant_id': self.restaurant.id,
        })
        # When
        response = self.client.post(url)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.restaurant, Restaurant.objects.filter(subscribers=self.user))

    def test_return_OK_when_subscribe_cancel_success(self):
        '''
        로그인 유저가 구독 중인 레스토랑 구독 취소 시 성공 반환
        '''
        # Given
        self.client.login(username=self.username, password=self.password)
        url_save = reverse("restaurant_api:restaurant_subscribe_api", kwargs={
            'restaurant_id': self.restaurant.id,
        })
        url_cancel = reverse("restaurant_api:restaurant_subscribe_api", kwargs={
            'restaurant_id': self.restaurant.id,
        })
        # When
        self.client.post(url_save)
        response = self.client.post(url_cancel)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.restaurant, Restaurant.objects.filter(subscribers=self.user))

    def test_return_BAD_REQUEST_when_try_subscribe_without_restaurant_id(self):
        '''
        레스토랑 id가 없는 상태에서 구독 시도 시 BAD REQUEST 리턴
        '''
        # Given
        self.client.login(username=self.username, password=self.password)
        self.unvalid_restaurant_id = 999999999999
        url = reverse("restaurant_api:restaurant_subscribe_api", kwargs={
            'restaurant_id': self.unvalid_restaurant_id,
        })
        # When
        response = self.client.post(url)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_return_OK_when_subscribed_restaurants_on_request(self):
        '''
        구독중인 레스토랑 요청 시 OK 반환
        '''
        # Given
        self.client.login(username=self.username, password=self.password)
        self.user_id = self.user.id
        url_save = reverse("restaurant_api:restaurant_subscribe_api", kwargs={
            'restaurant_id': self.restaurant.id,
        })
        url_lookup = reverse("restaurant_api:subscribed_restaurant_api", kwargs={
            'user_id': self.user_id,
        })
        # When
        self.client.post(url_save)
        response = self.client.get(url_lookup)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_return_OK_when_subscribe_cancel_and_no_subscribed_restaurants_on_request(self):
        '''
        레스토랑 구독 취소 후 레스토랑 없는 데 요청한 경우 OK 반환
        '''
        # Given
        self.client.login(username=self.username, password=self.password)
        self.user_id = self.user.id
        url_save = reverse("restaurant_api:restaurant_subscribe_api", kwargs={
            'restaurant_id': self.restaurant.id,
        })
        url_cancel = reverse("restaurant_api:restaurant_subscribe_api", kwargs={
            'restaurant_id': self.restaurant.id,
        })
        url_lookup = reverse("restaurant_api:subscribed_restaurant_api", kwargs={
            'user_id': self.user_id,
        })
        # When
        self.client.post(url_save)
        self.client.post(url_cancel)
        response = self.client.get(url_lookup)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.restaurant, Restaurant.objects.filter(subscribers=self.user))
