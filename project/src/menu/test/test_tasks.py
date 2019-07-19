from http import HTTPStatus

from django.conf import settings
from django.db.models import Count, F, Sum
from django.test import TestCase

from accounts.models import User
from cart.models import Cart, CartItem
from menu.api import tasks
from menu.models import Menu
from order.models import Order, DeliveryStatus
from restaurant.models import Restaurant


class CalcMenuScoreTestCase(TestCase):
    def setUp(self):
        self.MAX_RANDOM_SCORE_SUM_TEN_MENU = 100
        self.MIN_RANDOM_SCORE_SUM_TEN_MENU = 60
        self.HIT_COUNT_OR_LIKE_SCORE_SUM = 97.5
        self.ORDER_SCORE_SUM = 100

        self.user = User.objects.create_user(
            username='thkwon',
            email='',
            password='hohoho123!',
        )

    def test_update_random_score_should_return_0_when_queryset_is_not_exists(self):
        """
        update_random_score() 함수는 메뉴에 더해진 총 점수를 리턴하는데, 쿼리셋이 비어있으면 0을 리턴한다.
        """

        # Given: 현재 생성된 메뉴가 하나도 없는 상황에서 모든 메뉴 객체를 불러온다.
        all_menu = Menu.objects.all()

        # When: update_random_score를 호출한다.
        random_score_sum = tasks.update_random_score(
            all_menu,
            settings.RANDOM_SCORE_WEIGHT
        )

        # Then: 0을 리턴한다.
        self.assertEqual(random_score_sum, 0)

    def test_update_random_score_should_return_added_score_sum(self):
        """
        update_random_score() 함수는 메뉴에 더해진 총 점수를 리턴한다.
        """

        # Given: 현재 메뉴가 10개 생성되어 있다.
        self.make_ten_menus()
        all_menu = Menu.objects.all()

        # When: update_random_score를 호출한다.
        random_score_sum = tasks.update_random_score(
            all_menu,
            settings.RANDOM_SCORE_WEIGHT
        )

        # Then: 10개 메뉴에 대해서 랜덤(6~10) 점수의 합이 리턴되고, 이 값은 최소: 60점, 최대 100점 사이이다.
        self.assertLessEqual(
            random_score_sum,
            self.MAX_RANDOM_SCORE_SUM_TEN_MENU
        )
        self.assertGreaterEqual(
            random_score_sum,
            self.MIN_RANDOM_SCORE_SUM_TEN_MENU
        )

    def test_update_hit_count_or_like_score_should_return_0_when_queryset_is_not_exists(self):
        """
        update_hit_count_or_like() 함수는 메뉴에 더해진 총 점수를 리턴하는데, 쿼리셋이 비어있으면 0을 리턴한다.
        """

        # Given: 현재 생성된 메뉴가 하나도 없는 상황에서 모든 메뉴 객체를 불러온다.
        all_menu = Menu.objects.all()

        # When: update_hit_count_or_like_score를 호출한다. hit,like 계산법이 같고 가중치만 다르기때문에 hit만 테스트 한다.
        hit_count_or_like_score = tasks.update_hit_count_or_like(
            all_menu,
            settings.HIT_SCORE_WEIGHT
        )

        # Then: 0을 리턴한다.
        self.assertEqual(hit_count_or_like_score, 0)

    def test_update_hit_count_or_like_score_should_return_added_score_sum(self):
        """
        update_hit_count_or_like_score() 함수는 메뉴에 더해진 총 점수를 리턴한다.
        """

        # Given: 현재 메뉴가 10개 생성되어 있다. 모든 메뉴를 불러오고, hit가 높은 순으로 내림차순한다.
        self.make_ten_menus()
        all_menu = Menu.objects.all()
        hit_count_desc = all_menu.order_by('-hit')

        # When: update_hit_count_or_like_score()를 호출한다.
        hit_count_or_like_score = tasks.update_hit_count_or_like(
            hit_count_desc,
            settings.HIT_SCORE_WEIGHT
        )

        # Then: 10개 메뉴에 대해서 TOP5 메뉴는 (10~6점), 나머지는 5점을 받고,
        # 그 score_sum은 TOP5 Score 합계 * 가중치(1.5) + 나머지 Score 합계 * 가중치(1.5) 이다.
        self.assertEqual(
            hit_count_or_like_score,
            self.HIT_COUNT_OR_LIKE_SCORE_SUM
        )

    def test_update_order_count_score_should_return_0_when_queryset_is_not_exists(self):
        """
        update_order_count_score() 함수는 메뉴에 더해진 총 점수를 리턴하는데, 쿼리셋이 비어있으면 0을 리턴한다.
        """

        # Given: 현재 생성된 메뉴가 하나도 없는 상황에서 모든 메뉴 객체를 불러오고, 주문이 많은 순으로 id 값을 가져온다.
        all_menu = Menu.objects.all()
        order_count_desc = (Cart.objects
                            .prefetch_related('order')
                            .filter(order__delivery_status=DeliveryStatus.COMPLETE)
                            .values('cartitem__menu__name')
                            .annotate(
                                menu=F('cartitem__menu__name'),
                                quantity=Sum('cartitem__quantity')
                            )
                            .order_by('-quantity')
                            .values_list(
                                F('cartitem__menu__id'),
                                flat=True
                            ))

        # When: update_order_count_score()를 호출한다.
        order_count_score = tasks.update_order_count_score(
            all_menu,
            order_count_desc,
            settings.ORDER_SCORE_WEIGHT
        )

        # Then: 0을 리턴한다.
        self.assertEqual(order_count_score, 0)

    def test_update_order_count_score_should_return_added_score_sum(self):
        """
        update_order_count_score() 함수는 메뉴에 더해진 총 점수를 리턴한다.
        """

        # Given: 현재 메뉴가 10개 생성되어 있다.
        # cart 5개에 각각 메뉴 5개를 담고, 해당 Cart를 주문 한후,
        # 주문이 많은 메뉴 순으로 TOP5를 내림차순 정렬한다.
        self.make_ten_menus()
        self.make_cart()
        self.make_cart_item()
        self.make_order()
        all_menu = Menu.objects.all()
        order_count_desc = (Cart.objects
                            .prefetch_related('order')
                            .filter(order__delivery_status=DeliveryStatus.COMPLETE)
                            .values('cartitem__menu__name')
                            .annotate(
                                menu=F('cartitem__menu__name'),
                                quantity=Sum('cartitem__quantity')
                            )
                            .order_by('-quantity')
                            .values_list(
                                F('cartitem__menu__id'),
                                flat=True
                            ))

        # When: update_order_count_score()를 호출한다.
        order_count_score = tasks.update_order_count_score(
            all_menu,
            order_count_desc,
            settings.ORDER_SCORE_WEIGHT
        )

        # Then: 10개 메뉴에 대해서 주문된 TOP 5개의 메뉴의 Score_sum은 TOP5 Score 합계 * 가중치(2.5) 이다.
        self.assertEqual(
            order_count_score,
            self.ORDER_SCORE_SUM
        )

    def make_cart(self):
        """
        Cart 5개를 생성한다.
        """
        self.cart_1 = Cart.objects.create(
            user=self.user
        )
        self.cart_2 = Cart.objects.create(
            user=self.user
        )
        self.cart_3 = Cart.objects.create(
            user=self.user
        )
        self.cart_4 = Cart.objects.create(
            user=self.user
        )
        self.cart_5 = Cart.objects.create(
            user=self.user
        )

    def make_cart_item(self):
        """
        생성된 Cart에 Item을 넣는다.
        """
        CartItem.objects.create(
            cart=self.cart_1,
            menu=self.jjajangmyun,
            quantity=3
        )
        CartItem.objects.create(
            cart=self.cart_2,
            menu=self.jjambbong,
            quantity=2
        )
        CartItem.objects.create(
            cart=self.cart_3,
            menu=self.chinese_ddeokboke,
            quantity=2
        )
        CartItem.objects.create(
            cart=self.cart_4,
            menu=self.yangjangpi,
            quantity=5
        )
        CartItem.objects.create(
            cart=self.cart_5,
            menu=self.tangsuyook,
            quantity=4
        )

    def make_order(self):
        """
        생성된 Cart를 바탕으로 주문을 생성한다.
        """
        self.order_1 = Order.objects.create(
            user=self.user,
            cart=self.cart_1,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        self.order_2 = Order.objects.create(
            user=self.user,
            cart=self.cart_2,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        self.order_3 = Order.objects.create(
            user=self.user,
            cart=self.cart_3,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        self.order_4 = Order.objects.create(
            user=self.user,
            cart=self.cart_4,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )
        self.order_5 = Order.objects.create(
            user=self.user,
            cart=self.cart_5,
            restaurant=self.restaurant,
            address="주문자 주소",
            address_detail="주문자 상세 주소",
            status="1",
            delivery_status=DeliveryStatus.COMPLETE,
            phone_num="010-1234-1234"
        )

    def make_ten_menus(self):
        """
        임의의 메뉴 10개를 생성한다.
        """
        self.restaurant = Restaurant.objects.create(
            name='금룡',
            owner='권태형',
            title='금룡 한양대점',
            estimated_delivery_time='22:50',
            operation_start_hour='12:00',
            operation_end_hour='20:00',
            min_order_price=15000,
            delivery_charge=2000,
        )

        self.jjajangmyun = Menu.objects.create(
            restaurant=self.restaurant,
            name='짜장면',
            detail='맛있는 짜장면',
            price=3000,
            hit=10,
            type='인기메뉴',
            img='test.jpg',
        )
        self.jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='짬뽕',
            detail='맛있는 짬뽕',
            price=3000,
            hit=9,
            type='인기메뉴',
            img='test.jpg',
        )
        self.tangsuyook = Menu.objects.create(
            restaurant=self.restaurant,
            name='탕수육',
            detail='맛있는 탕수육',
            price=3000,
            hit=8,
            type='인기메뉴',
            img='test.jpg',
        )
        self.spicy_jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='매운 짬뽕',
            detail='맛있는 매운 짬뽕',
            price=3000,
            hit=7,
            type='인기메뉴',
            img='test.jpg',
        )
        self.gganpoongi = Menu.objects.create(
            restaurant=self.restaurant,
            name='깐풍기',
            detail='맛있는 깐풍기',
            price=3000,
            hit=6,
            type='인기메뉴',
            img='test.jpg',
        )
        self.yangjangpi = Menu.objects.create(
            restaurant=self.restaurant,
            name='양장피',
            detail='맛있는 양장피',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.chinese_ddeokboke = Menu.objects.create(
            restaurant=self.restaurant,
            name='중국식 떡볶이',
            detail='맛있는 중국식 떡볶이',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.chinese_woodong = Menu.objects.create(
            restaurant=self.restaurant,
            name='중국식 우동',
            detail='맛있는 중국식 우동',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.fried_jjambbong = Menu.objects.create(
            restaurant=self.restaurant,
            name='볶음짬봉',
            detail='맛있는 볶음짬봉',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
        self.jjabchaebob = Menu.objects.create(
            restaurant=self.restaurant,
            name='잡채밥',
            detail='맛있는 잡채밥',
            price=3000,
            type='인기메뉴',
            img='test.jpg',
        )
