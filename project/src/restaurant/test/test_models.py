from django.test import TestCase
from restaurant.models import Restaurant


class RestaurantTest(TestCase):
    def setUp(self):
        self.now = '2019-01-01 12:00:00.000000+00:00'
        self.restaurant = Restaurant(
            name='군내치킨',
            owner='박군내',
            title='군내치킨-서초점',
            tel='1234',
            min_order_price=10000,
            order_way='현장 결제',
            origin='닭:국내산',
            delivery_charge=2000,
            info='군내나지만 맛있습니다.',
            type='요기요 등록 음식점',
            img='media/restaurant/chicken.png',
            estimated_delivery_time=self.now,
            operation_start_hour=self.now,
            operation_end_hour=self.now,
        )
        self.restaurant.save()
        self.category = self.restaurant.category.create(name='1인분 주문')
        self.category.save()

    def test_restaurant_should_be_created_on_valid_data(self):
        '''
        유효한 데이터에 대해 레스토랑을 생성한다.
        '''
        # Given

        # When

        # Then
        self.assertEqual(self.restaurant.owner, '박군내')
        self.assertEqual(self.restaurant.title, '군내치킨-서초점')
        self.assertEqual(self.restaurant.tel, '1234')
        self.assertEqual(self.restaurant.min_order_price, 10000)
        self.assertEqual(self.restaurant.order_way, '현장 결제')
        self.assertEqual(self.restaurant.delivery_charge, 2000)
        self.assertEqual(self.restaurant.info, '군내나지만 맛있습니다.')
        self.assertEqual(self.restaurant.type, '요기요 등록 음식점')
        self.assertEqual(self.restaurant.estimated_delivery_time, self.now)
        self.assertEqual(self.restaurant.operation_start_hour, self.now)
        self.assertEqual(self.restaurant.operation_end_hour, self.now)
        self.assertIsNotNone(self.restaurant.img)
        self.assertIsInstance(self.restaurant, Restaurant)
        self.assertEqual(self.restaurant.__str__(), self.restaurant.name)
        self.assertEqual(self.restaurant.category.get(pk=self.category.pk), self.category)
        self.assertEqual(self.category.name, '1인분 주문')

    def test_restaurant_should_not_be_created_on_invalid_data(self):
        '''
        유효하지 않은 데이터에 대해 레스토랑을 생성하지 않는다.
        '''
        # Given

        # When

        # Then
        self.assertIsNot(self.restaurant.min_order_price, 1000)
        self.assertIsNot(self.restaurant.estimated_delivery_time, 'now')
        self.assertIsNot(self.restaurant.img, '-')
        self.assertNotIsInstance(self.category, Restaurant)
        self.assertIsNot(self.restaurant.__str__(), '굽굽치킨')
        self.assertIsNot(self.restaurant.category.get(pk=self.category.pk), self.restaurant)
