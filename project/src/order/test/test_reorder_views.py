import datetime
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from cart.models import Cart, CartItem
from category.models import Category
from menu.models import Menu
from order.models import Order, DeliveryStatus
from restaurant.models import Restaurant
from yosigy.models import YosigyTicket, YosigyMenu, Yosigy, YosigyTiketStatus


class ReorderCreateAPIViewTestCase(TestCase):
    def setUp(self):
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
        self.cart = Cart.objects.create(
            user=self.user
        )
        self.cart_item_jjajangmyun = CartItem.objects.create(
            menu=self.jjajangmyun,
            cart=self.cart,
            quantity=1
        )

    def test_reorder_should_return_401_when_user_is_anonymous(self):
        """
        재주문 생성 APIsms 비 로그인 상태일 때는 401을 반환한다. 
        """
        # Given: 유저는 비 로그인 상태이다.

        # When: ReOrderCreateAPIView를 호출한다.
        order = Order.objects.create(
            user=self.user,
            cart=self.cart,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )

        response = self.client.post(
            path=reverse(
                'order_api:reorder',
                kwargs={'order_id': order.id}
            ),
            content_type='application/json:charset=utf-8;'
        )

        # Then: 상태코드 401을 반환한다.
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_reorder_should_return_200_when_order_id_is_valid_and_not_yosigy_order(self):
        """
        재주문 생성 API는 url parameter로 받는 order_id가 유효하고, 요식이 주문이 아니라면, 200을 반환한다.  
        """
        # Given: 로그인을 한다. / 재주문 생성을 위한 요식이 주문이 아닌, 일반 주문을 생성한다.
        self.client.login(username='yosigy_user', password='yosigy_password')
        order = Order.objects.create(
            user=self.user,
            cart=self.cart,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )

        # When: ReorderCreateAPIView를 호출한다.
        response = self.client.post(
            path=reverse(
                'order_api:reorder',
                kwargs={'order_id': order.id}
            ),
            content_type='application/json:charset=utf-8;'
        )

        # Then: 상태코드 200을 반환한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['message'], '재주문할 새로운 주문표를 생성하였습니다.')

    def test_reorder_should_return_404_when_order_id_is_not_exists(self):
        """
        재주문 생성 API는 존재하지 않는 주문 id를 url paramter로 받을 때, 404를 반환한다. 
        """
        # Given: 유저는 로그인한 상태이다. / 올바르지 않은, 주문 id가 주어진다.
        self.client.login(username='yosigy_user', password='yosigy_password')
        NOT_EXISTS_ORDER_ID = "abcdabcd-abcd-abcd-abcd-abcdabcdabcd"

        # When: ReOrderCreateAPIView를 호출한다.
        response = self.client.post(
            path=reverse(
                'order_api:reorder',
                kwargs={'order_id': NOT_EXISTS_ORDER_ID}
            ),
            content_type='application/json:charset=utf-8;'
        )
        # Then: 상태코드 404를 반환한다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['message'], '주문 id를 찾을 수 없습니다.')

    def test_reorder_should_return_404_when_cart_is_empty(self):
        """
        재주문 생성 API는 주문표가 할당되지 않았다면, 404를 반환한다.
        (요식이로 생성된 주문은 재주문을 할 수 없다.(주문표 할당이 되어있지 않다.))
        """
        YOSIGY_PERIOD_DAYS = 10

        # Given: 유저는 로그인한 상태이다. / 요식이로 주문을 생성한다. 
        self.client.login(username='yosigy_user', password='yosigy_password')
        order = Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        yosigy = Yosigy.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            deadline=datetime.datetime.now() + datetime.timedelta(days=YOSIGY_PERIOD_DAYS),
            notice='요식이 레스토랑입니다.',
            min_price=20000,
        )
        yosigy_menu_jjajangmyun = YosigyMenu.objects.create(
            discounted_price=6000,
            menu=self.jjajangmyun,
            yosigy=yosigy,
        )
        yosigy_ticket_jjajangmyun = YosigyTicket.objects.create(
            user=self.user,
            yosigy_menu=yosigy_menu_jjajangmyun,
            menu=self.jjajangmyun,
            expire_time=datetime.datetime.now() + datetime.timedelta(days=YOSIGY_PERIOD_DAYS),
            status=YosigyTiketStatus.PUBLISHED
        )

        order.yosigy_ticket.add(yosigy_ticket_jjajangmyun)

        # When: ReOrderCreateAPIView를 호출한다.
        response = self.client.post(
            path=reverse(
                'order_api:reorder',
                kwargs={'order_id': order.id}
            ),
            content_type='application/json:charset=utf-8;'
        )

        # Then: 상태코드 404를 반환한다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['message'], '해당 주문은 요식이로 구매하였습니다.')
