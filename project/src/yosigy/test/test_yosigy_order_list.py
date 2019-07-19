from datetime import datetime
from http import HTTPStatus

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from menu.models import Menu
from restaurant.models import Restaurant
from yosigy.models import Yosigy, YosigyMenu, YosigyTicket, YosigyTiketStatus


class YosigyOrderListTest(TestCase):
    def setUp(self):
        self.datetime_future=timezone.now() + relativedelta(years=10)
        self.datetime_past=timezone.now() - relativedelta(years=10)

        self.owner = User.objects.create_user(
            username='owner',
            email='',
            password='1',
            address='서울시 서초구 서초2동 마제스타 시티',
        )
        self.user = User.objects.create_user(
            username='yosigy',
            email='',
            password='1',
            address='서울시 서초구 서초2동 사랑의 교회',
        )
        self.user_without_yosigy = User.objects.create_user(
            username='yosigy2',
            email='',
            password='1',
            address='서울시 서초구 서초2동 사랑의 교회',
        )
        self.restaurant1 = Restaurant.objects.create(
            name='굽네치킨',
            title='굽네치킨-서초점',
            min_order_price=10000,
            delivery_charge=1000,
            store_owner=self.owner,
            estimated_delivery_time='20:00',
            operation_start_hour='10:00',
            operation_end_hour='20:00',
        )
        self.restaurant2 = Restaurant.objects.create(
            name='굽네치킨2',
            title='굽네치킨2-서초점',
            min_order_price=10000,
            delivery_charge=1000,
            store_owner=self.owner,
            estimated_delivery_time='20:00',
            operation_start_hour='10:00',
            operation_end_hour='20:00',
        )
        self.menu1 = Menu.objects.create(
            restaurant=self.restaurant1,
            name='볼케이노',
            detail='매콤',
            price=15000,
            type='양념류',
            img='test.jpg',
            is_yosigy=True,
        )
        self.menu2 = Menu.objects.create(
            restaurant=self.restaurant1,
            name='허니멜로',
            detail='달콤',
            price=16000,
            type='양념류',
            img='test2.jpg',
            is_yosigy=True,
        )
        self.yosigy = Yosigy.objects.create(
            restaurant=self.restaurant1,
            user=self.user,
            deadline=datetime(2100,11,11),
            notice='요식이 레스토랑입니다.',
            min_price=20000,
        )
        self.yosigy_menu1 = YosigyMenu.objects.create(
            discounted_price=12000,
            menu=self.menu1,
            yosigy=self.yosigy,
        )
        self.yosigy_menu2 = YosigyMenu.objects.create(
            discounted_price=11000,
            menu=self.menu2,
            yosigy=self.yosigy,
        )
        self.yosigy_ticket_published = YosigyTicket.objects.create(
            user=self.user,
            yosigy_menu=self.yosigy_menu1,
            menu=self.menu1,
            expire_time=self.datetime_future,
            status=YosigyTiketStatus.PUBLISHED,
        )
        self.yosigy_ticket_used = YosigyTicket.objects.create(
            user=self.user,
            yosigy_menu=self.yosigy_menu2,
            menu=self.menu1,
            expire_time=self.datetime_future,
            status=YosigyTiketStatus.USED,
        )
        self.yosigy_ticket_expired = YosigyTicket.objects.create(
            user=self.user,
            yosigy_menu=self.yosigy_menu2,
            menu=self.menu1,
            expire_time=self.datetime_past,
            status=YosigyTiketStatus.USED,
        )

    def test_yosigy_order_list(self):
        '''
        사용자가 선택한 요식이가 요식이 주문 페이지에 나오는 지 테스트
        '''
        # Given
        self.client.login(username='yosigy', password='1')
        yosigy_ticket_pk = [str(self.yosigy_ticket_published.pk)]
        # When
        response = self.client.get(reverse('yosigy_api:yosigy_order_list_api'), {'yosigyPks': str(yosigy_ticket_pk)})
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_return_BAD_REQUEST_when_yosigy_unchecked(self):
        '''
        선택된 요식이가 없는 경우 BAD REQUEST 반환
        '''
        # Given
        self.client.login(username='yosigy', password='1')
        # When
        response = self.client.get(reverse('yosigy_api:yosigy_order_list_api'))
        # Then
        message = response.json()['message']
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(message, '체크된 요식이가 없습니다. 요식이를 체크 후 사용해주세요 !')

    def test_return_BAD_REQUEST_when_no_yosigy(self):
        '''
        요식이가 없는 경우 BAD REQUEST 반환
        '''
        # Given
        self.client.login(username='yosigy', password='1')
        not_exist_yosigy_ticket_pk = 999999
        yosigy_ticket_pk = [str(not_exist_yosigy_ticket_pk)]
        # When
        response = self.client.get(reverse('yosigy_api:yosigy_order_list_api'), {'yosigyPks': str(yosigy_ticket_pk)})
        # Then
        message = response.json()['message']
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(message, '해당 요식이가 없습니다. 확인 후 다시 사용해주세요 !')
