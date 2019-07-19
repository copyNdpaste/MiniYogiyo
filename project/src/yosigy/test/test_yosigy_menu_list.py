import datetime
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from category.models import Category
from menu.models import Menu
from restaurant.models import Restaurant
from yosigy.models import YosigyMenu, Yosigy


class YosigyDetailListAPIViewTestCase(TestCase):
    def setUp(self):
        """
        1. 유저 생성 
        2. 요식이 지정 레스토랑 생성
        3. 요식이 메뉴 지정된 메뉴 생성
        """
        self.user = User.objects.create_user(
            username='yosigy_user',
            email='',
            password='yosigy_password'
        )
        self.owner = User.objects.create_user(
            username='im_owner',
            email='',
            password='owner_password'
        )

        self.category = Category.objects.create(
            name='중화요리'
        )
        self.restaurant = Restaurant.objects.create(
            name='금룡',
            store_owner=self.owner,
            title='금룡 한양대점',
            estimated_delivery_time='22:50',
            operation_start_hour='12:00',
            operation_end_hour='20:00',
            min_order_price=15000,
            delivery_charge=2000,
            is_yosigy=True,
            img='test.jpg'
        )
        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            name='짜장면',
            detail='맛있는 짜장면',
            price=3000,
            type='인기메뉴',
            img='test.jpg',

        )
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='짬뽕',
            detail='맛있는 짬뽕',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.tangsuyook = Menu.objects.create(
            restaurant=self.restaurant,
            name='탕수육',
            detail='맛있는 탕수육',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.spicy_jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='매운 짬뽕',
            detail='맛있는 매운 짬뽕',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.gganpoongi = Menu.objects.create(
            restaurant=self.restaurant,
            name='깐풍기',
            detail='맛있는 깐풍기',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )

    def test_yosigy_detail_should_return_401_when_user_is_anonymous(self):
        """
        요식이 디테일 API는 비로그인 상태일 때는 401을 반환해야한다. 
        """
        # Given: 유저는 비 로그인 상태이다.
        yosigy = Yosigy.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            deadline=datetime.datetime.now() + datetime.timedelta(days=10),
            notice="요식이 공지사항 입니다!",
            min_price=15000
        )

        # When: YosigyDetailAPIView를 호출한다.
        response = self.client.get(
            reverse(
                'yosigy_api:yosigy_detail_api',
                kwargs={'yosigy_id': yosigy.id}
            )
        )

        # Then: 상태코드 401을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNAUTHORIZED
        )

    def test_yosigy_detail_should_return_200_when_yosigy_restaurant_and_menu_exist(self):
        """
        요식이 디테일 API는 요식이 레스토랑과 메뉴가 정상적으로 존재하면, 200을 리턴해야한다. 
        """
        # Given: 유저는 로그인 상태이다. / 요식이 레스토랑과 요식이 메뉴를 정상적으로 지정한다.
        self.client.login(
            username='yosigy_user',
            password='yosigy_password'
        )
        yosigy = Yosigy.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            deadline=datetime.datetime.now() + datetime.timedelta(days=10),
            notice="요식이 공지사항 입니다!",
            min_price=15000
        )
        self.yosigy_menu_jjambbong = YosigyMenu.objects.create(
            discounted_price=4000,
            menu=self.jjambbong,
            yosigy=yosigy
        )
        self.yosigy_menu_jjajangmyun = YosigyMenu.objects.create(
            discounted_price=3500,
            menu=self.jjajangmyun,
            yosigy=yosigy
        )

        # When: YosigyDetailAPIView를 호출한다.
        response = self.client.get(
            reverse(
                'yosigy_api:yosigy_detail_api',
                kwargs={'yosigy_id': yosigy.id}
            )
        )

        # Then: 상태코드 200을 반환한다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

    def test_yosigy_detail_should_return_404_when_yosigy_obj_is_not_exists(self):
        """
        요식이 디테일 API는 요식이 객체가 존재하지 않으면,  404를 리턴해야한다.
        """
        # Given: 유저는 로그인 상태이다. / 요식이 레스토랑을 생성하지 않는다.
        self.client.login(
            username='yosigy_user',
            password='yosigy_password'
        )
        NOT_EXISTS_YOSIGY_OBJ_ID = 100000

        # When: YosigyDetailAPIView를 호출한다.
        response = self.client.get(
            reverse(
                'yosigy_api:yosigy_detail_api',
                kwargs={'yosigy_id': NOT_EXISTS_YOSIGY_OBJ_ID}
            )
        )

        # Then: 상태코드 404를 반환한다. / '해당하는 요식이가 존재하지 않습니다.' 메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(
            response.json()['message'],
            '해당하는 요식이가 존재하지 않습니다.'
        )

    def test_yosigy_detail_should_return_404_when_yosigy_menu_is_not_exists(self):
        """
        요식이 디테일 API는 요식이 메뉴가 존재하지 않는다면, 404를 리턴해야한다.  
        """
        # Given: 유저는 로그인 상태이다. / 요식이 레스토랑을 생성하고, 요식이 메뉴는 지정하지 않는다.
        self.client.login(
            username='yosigy_user',
            password='yosigy_password'
        )
        yosigy = Yosigy.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            deadline=datetime.datetime.now() + datetime.timedelta(days=10),
            notice="요식이 공지사항 입니다!",
            min_price=15000
        )
        # When: YosigyDetailAPIView를 호출한다.
        response = self.client.get(
            reverse(
                'yosigy_api:yosigy_detail_api',
                kwargs={'yosigy_id': yosigy.id}
            )
        )
        # Then: 상태코드 404를 반환한다. / '해당하는 요식이 메뉴가 없습니다.' 메세지를 보여준다.
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(
            response.json()['message'],
            '해당하는 요식이 메뉴가 없습니다.'
        )
