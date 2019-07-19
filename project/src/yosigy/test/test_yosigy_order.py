import json
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


class YosigyOrderTest(TestCase):
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
        self.yosigy_ticket_published1 = YosigyTicket.objects.create(
            user=self.user,
            yosigy_menu=self.yosigy_menu1,
            menu=self.menu1,
            expire_time=self.datetime_future,
            status=YosigyTiketStatus.PUBLISHED,
        )
        self.yosigy_ticket_published2 = YosigyTicket.objects.create(
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

    def test_yosigy_order(self):
        '''
        사용자가 선택한 요식이로 주문하는 테스트, order 레코드 생성됨
        '''
        # Given
        self.client.login(username='yosigy', password='1')
        json_data = {
            'user': self.user.pk,
            'address': '서울시 서초구 서초2동 힐스테이트 102동 101호',
            'address_detail': '서초2동 마제스타 시티 타워 2',
            'phone_num': '010-1234-1234',
            'yosigy_ticket': [self.yosigy_ticket_published1.pk, self.yosigy_ticket_published2.pk],
            'restaurant': self.restaurant1.pk,
        }
        # When
        response = self.client.post(reverse('yosigy_api:yosigy_order_api'),
                                    data=json.dumps(json_data), content_type='application/json')
        # Then
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_return_BAD_REQUEST_when_there_are_no_yosigy_to_use(self):
        '''
        사용할 수 있는 요식이가 없는 경우 BAD REQUEST 반환
        '''
        # Given
        self.client.login(username='yosigy', password='1')
        json_data = {
            'user': self.user.pk,
            'address': '서울시 서초구 서초2동 힐스테이트 102동 101호',
            'address_detail': '서초2동 마제스타 시티 타워 2',
            'phone_num': '010-1234-1234',
            'yosigy_ticket': [self.yosigy_ticket_used.pk, self.yosigy_ticket_expired.pk],
            'restaurant': self.restaurant1.pk,
        }
        # When
        response = self.client.post(reverse('yosigy_api:yosigy_order_api'),
                                    data=json.dumps(json_data), content_type='application/json')
        # Then
        message = response.json()['message']
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(message, '사용할 수 없는 요식이가 있습니다.')
