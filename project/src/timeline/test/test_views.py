from http import HTTPStatus
from django.test import TestCase
from django.shortcuts import reverse
from accounts.models import User
from restaurant.models import Restaurant, RestaurantTimeline


class RestaurantTimelineListApiTestCase(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        self.restaurant = Restaurant.objects.create(
            name='test_restaurant',
            owner='test_owner',
            title='test_restaurant 요기요점',
            estimated_delivery_time='22:50',
            operation_start_hour='12:00',
            operation_end_hour='20:00',
            min_order_price=15000,
            delivery_charge=2000,
        )

    def _subscribe_restaurant(self, restaurant_id):
        self.client.post(
            path=reverse("restaurant_api:restaurant_subscribe_api", kwargs={'restaurant_id': restaurant_id}),
            content_type='application/json:charset=utf-8;'
        )

    def _update_restaurant_info(self, restaurant_id):
        restaurant_timeline = RestaurantTimeline.objects.create(
            restaurant_id=restaurant_id,
            status=2,
            timeline_type=2,
            changed_field='event',
            changed_data='이벤트합니다.'
        )
        return restaurant_timeline

    def test_anonymous_user_get_restaurant_timeline_list_api(self):
        # Given : user is anonymous

        # When : user get RestaurantTimelineListApi
        response = self.client.get(
            path=reverse('timeline_api:restaurant'),
            content_type='application/json:charset=utf-8;'
        )
        # Then: response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_who_has_no_subscribed_restaurant_get_restaurant_timeline_list_api(self):
        # Given 1 : user login
        self.client.login(username=self.username, password=self.password)
        # Given 2 : user haven't subscribe any restaurants
        # self._subscribe_restaurant(self.restaurant.id)

        # When : user get RestaurantTimelineListApi
        response = self.client.get(
            path=reverse('timeline_api:restaurant'),
            content_type='application/json:charset=utf-8;'
        )
        # Then: response should have HTTPStatus.NOT_FOUND & error 구독중인 restaurant가 없습니다
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['error'], '구독중인 restaurant가 없습니다.')

    def test_user_get_restaurant_timeline_list_api_when_subscribed_restaurant_have_not_updated(self):
        # Given 1 : user login
        self.client.login(username=self.username, password=self.password)
        # Given 2 : user subscribe a restaurant
        self._subscribe_restaurant(self.restaurant.id)
        # Given 3 : restaurant which user subscribed haven't updated data
        # restaurant_timeline = self.update_restaurant_info(self.restaurant.id)

        # When : user get RestaurantTimelineListApi
        response = self.client.get(
            path=reverse('timeline_api:restaurant'),
            content_type='application/json:charset=utf-8;'
        )

        # Then:response should have HTTPStatus.NOT_FOUND & error 구독중인 restaurant가 없습니다
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['error'], '업데이트 된 정보가 없습니다.')

    def test_user_get_restaurant_timeline_list_api(self):
        # Given 1 : user login
        self.client.login(username=self.username, password=self.password)
        # Given 2 : user subscribe a restaurant
        self._subscribe_restaurant(self.restaurant.id)
        # Given 3 : restaurant which user subscribed updated data
        restaurant_timeline = self._update_restaurant_info(self.restaurant.id)

        # When : user get RestaurantTimelineListApi
        response = self.client.get(
            path=reverse('timeline_api:restaurant'),
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should have HTTPStatus.OK & have updated restaurants data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()[0]['post_info'], restaurant_timeline.changed_data)
