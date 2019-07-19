from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from menu.models import Menu
from restaurant.models import Restaurant


class MenuTimeLineTest(TestCase):
    def setUp(self):
        self.user_subscribing_restaurant = User.objects.create_user(username='홍길동', email='', password='1',
                                             address='서울시 서초구 서초2동 사랑의 교회')
        self.user_without_subscribing = User.objects.create_user(username='홍두깨', email='', password='1',
                                                                 address='서울시 서초구 서초2동 사랑의 교회')
        self.restaurant_create_one_menu = Restaurant.objects.create(
            name='굽내치킨1', title='굽내치킨1-서초점',
            min_order_price=10000, delivery_charge=1000, estimated_delivery_time='20:00',
            operation_start_hour='11:00', operation_end_hour='20:00', )
        self.restaurant_update_menu = Restaurant.objects.create(
            name='굽내치킨2', title='굽내치킨2-서초점',
            min_order_price=10000, delivery_charge=1000, estimated_delivery_time='20:00',
            operation_start_hour='11:00', operation_end_hour='20:00', )
        self.restaurant_without_menu_alarm = Restaurant.objects.create(
            name='굽내치킨3', title='굽내치킨-서초점',
            min_order_price=10000, delivery_charge=1000, estimated_delivery_time='20:00',
            operation_start_hour='11:00', operation_end_hour='20:00', )
        self.user_subscribing_restaurant.subscribed_restaurants.set = self.restaurant_create_one_menu
        self.created_menu = Menu(
            restaurant=self.restaurant_create_one_menu,
            name='갈비천왕',
            detail='갈비 맛입니다.',
            price=20000,
            type='양념류',
            img='test.jpg',
        )
        self.created_menu.save()

    def test_when_menutimeline_empty_return_message(self):
        '''
        타임라인이 없는 경우 메시지
        '''
        # Given
        self.client.login(username='홍길동', password='1')
        # When
        response = self.client.get(reverse('timeline_api:menutimeline'))
        message = response.json()['message']
        # Then
        self.assertEqual(message, '구독 중인 레스토랑이 없거나 전해드릴 메뉴 알림이 없습니다.')
