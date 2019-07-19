# test_list_api.py
from http import HTTPStatus
from django.test import TestCase
from django.shortcuts import reverse
from accounts.models import User
from coupon.models import GiftCoupon, UserGiftCoupon


class GiftCouponListApiTestCase(TestCase):

    def setUp(self):
        self.username = 'coupon_user',
        self.password = 'coupon_password'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

        self.sender_name = 'sender_name'
        self.sender_password = 'sender_password'
        self.sender = User.objects.create_user(
            username=self.sender_name, password=self.sender_password
        )

        self.coupon_code = self.send_coupon(self.sender_name, self.sender_password)

    def send_coupon(self, sender_name, sender_password):

        self.client.login(username=sender_name, password=sender_password)

        gift_coupon_data = {
            'receiver_name': '홍길동',
            'receiver_email': 'test190508@gmail.com',
            'receiver_phone': '',
            'sender_msg': '선물입니다.^^',
            'price': '10000',
        }

        self.client.post(
            path=reverse('create_gift_coupon_api'),
            data=gift_coupon_data,
            content_type='application/json:charset=utf-8;'
        )
        self.client.logout()

        coupon_code = GiftCoupon.objects.filter(sender__username=sender_name).order_by('-created_time')[0].coupon_code
        return coupon_code

    def register_coupon(self, coupon_code):
        self.client.post(
            path=reverse('register_gift_coupon_api'),
            data={
                'coupon_code': coupon_code
            },
            content_type='application/json:charset=utf-8;'
        )

    def test_user_who_has_no_coupon_get_received_coupon_list(self):
        # Given : user login
        self.client.login(username=self.username, password=self.password)

        # When : user try to see received coupon list
        response = self.client.get(
            path=reverse('received_coupon_list_api'),
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should have HTTPStatus.NOT_FOUND & message 받은 gift card가 없습니다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['message'], '받은 gift card가 없습니다.')

    def test_anonymous_user_get_received_coupon_list(self):
        # Given : user is anonymous

        # When : user try to see received coupon list
        response = self.client.get(
            path=reverse('received_coupon_list_api'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_get_received_coupon_list(self):
        # Given : user login & register coupon
        self.client.login(username=self.username, password=self.password)
        self.register_coupon(self.coupon_code)

        # When : user try to see received coupon list
        response = self.client.get(
            path=reverse('received_coupon_list_api'),
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should have HTTPStatus.OK  & coupons data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        coupons_data = response.json()['coupons']
        self.assertEqual(coupons_data[0]['coupon_code'], str(self.coupon_code))
        self.assertEqual(coupons_data[0]['sender_name'], self.sender_name)

    def test_anonymous_user_get_sent_coupon_list(self):
        # Given : user is anonymous

        # When : user try to see sent coupon list
        response = self.client.get(
            path=reverse('sent_coupon_list_api'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_who_did_not_send_coupon_get_sent_coupon_list(self):
        # Given : user login
        self.client.login(username=self.username, password=self.password)

        # When : user try to see sent coupon list
        response = self.client.get(
            path=reverse('sent_coupon_list_api'),
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should have HTTPStatus.NOT_FOUND & message 보낸 gift card가 없습니다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['message'], '보낸 gift card가 없습니다.')

    def test_user_get_sent_coupon_list(self):
        # Given : user send coupon & user login
        coupon_code = self.send_coupon(self.username, self.password)
        self.client.login(username=self.username, password=self.password)

        # When : user try to see sent coupon list
        response = self.client.get(
            path=reverse('sent_coupon_list_api'),
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should have HTTPStatus.OK & sent coupons data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        coupons_data = response.json()['coupons']
        self.assertEqual(coupons_data[0]['coupon_code'], str(coupon_code))

    def test_anonymous_user_get_available_coupon_list(self):
        # Given : user is anonymous

        # When : user try to see available coupon list
        response = self.client.get(
            path=reverse('available_coupon_list_api'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_who_have_not_received_coupon_get_available_coupon_list(self):
        # Given : user login & user haven't received coupon
        self.client.login(username=self.username, password=self.password)
        UserGiftCoupon.objects.filter(user=self.user).delete()

        # When : user try to see available coupon list
        response = self.client.get(
            path=reverse('available_coupon_list_api'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.NOT_FOUND & message 사용가능한 gift card가 없습니다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['message'], '사용가능한 gift card가 없습니다.')

    def test_user_get_available_coupon_list(self):
        # Given : user login & user received coupon
        self.client.login(username=self.username, password=self.password)
        self.register_coupon(self.coupon_code)

        # When : user try to see available coupon list
        response = self.client.get(
            path=reverse('available_coupon_list_api'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.OK & available coupon data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        coupons_data = response.json()['coupons']
        self.assertEqual(coupons_data[0]['coupon_code'], str(self.coupon_code))


class UncheckedHandoverCouponListApiTestCase(TestCase):

    def setUp(self):
        self.username = 'user_username'
        self.password = 'user_password'
        self.user = {
            'username': self.username,
            'password': self.password
        }
        User.objects.create_user(
            username=self.user['username'], password=self.user['password'])

        self.sender = {
            'username': 'sender_name',
            'password': 'sender_password'
        }
        User.objects.create_user(
            username=self.sender['username'], password=self.sender['password'])

        self.receiver = {
            'username': 'receiver_name',
            'password': 'receiver_password'
        }
        User.objects.create_user(
            username=self.receiver['username'], password=self.receiver['password'])

    def send_coupon(self, sender):
        self.client.login(username=sender['username'], password=sender['password'])

        gift_coupon_data = {
            'receiver_name': '홍길동',
            'receiver_email': 'test190508@gmail.com',
            'receiver_phone': '',
            'sender_msg': '선물입니다.^^',
            'price': '10000'
        }

        self.client.post(
            path=reverse('create_gift_coupon_api'),
            data=gift_coupon_data,
            content_type='application/json:charset=utf-8;'
        )

        coupon_code = (GiftCoupon.objects
                       .filter(sender__username=sender['username'])
                       .order_by('-created_time')[0].coupon_code)

        self.client.logout()

        return coupon_code

    def register_coupon(self, receiver, coupon_code):
        self.client.login(username=receiver['username'], password=receiver['password'])

        self.client.post(
            path=reverse('register_gift_coupon_api'),
            data={
                'coupon_code': coupon_code
            },
            content_type='application/json:charset=utf-8;'
        )

        registered_coupon_id = UserGiftCoupon.objects.all().order_by('-created_time')[0].id

        self.client.logout()

        return registered_coupon_id

    def handover_coupon(self, sender, receiver, registered_coupon_id):
        self.client.login(username=sender['username'], password=sender['password'])

        receiver_data = {
            'username': receiver['username'],
            'email': 'test@email.co.kr'
        }

        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': registered_coupon_id}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        coupon_code = response.json()['coupon_code']

        self.client.logout()

        return coupon_code

    def test_anonymous_user_get_UncheckedHandoverCouponListApi(self):
        # Given : user is anonymous

        # When : user try to get UncheckedHandoverCouponListApi
        response = self.client.get(
            path=reverse('unchecked_coupon_list'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_who_has_no_received_coupons_get_UncheckedHandoverCouponListApi(self):
        # Given : user login
        self.client.login(username=self.username, password=self.password)

        # When : user try to get UncheckedHandoverCouponListApi
        response = self.client.get(
            path=reverse('unchecked_coupon_list'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.OK
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['coupons'], '')
        self.assertEqual(response.json()['message'], '확인 안한 gift card가 없습니다.')

    def test_user_get_UncheckedHandoverCouponListApi(self):
        # Given : sender send coupon to receiver
        coupon_code = self.send_coupon(self.sender)
        # Given : receiver register coupon which he received
        registered_coupon_id = self.register_coupon(self.receiver, coupon_code)
        # Given : receiver handover coupon to user
        coupon_code = self.handover_coupon(self.receiver, self.user, registered_coupon_id)
        # Given : user login
        self.client.login(username=self.username, password=self.password)

        # When : user try to get UncheckedHandoverCouponListApi
        response = self.client.get(
            path=reverse('unchecked_coupon_list'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.OK & message 확인 안한 gift card가 있습니다.
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['message'], '확인 안한 gift card가 있습니다.')
        # Then : response should have unchecked coupon data
        unchecked_coupon_data = response.json()['coupons'][0]
        self.assertEqual(unchecked_coupon_data['coupon_code'], coupon_code)

    def test_anonymous_user_put_UncheckedHandoverCouponListApi(self):
        # Given : user is anonymous

        # When : user try to put UncheckedHandoverCouponListApi
        response = self.client.put(
            path=reverse('unchecked_coupon_list'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.v
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_an_put_UncheckedHandoverCouponListApi(self):
        # Given : sender send coupon to receiver
        coupon_code = self.send_coupon(self.sender)
        # Given : receiver register coupon which he received
        registered_coupon_id = self.register_coupon(self.receiver, coupon_code)
        # Given : receiver handover coupon to user
        coupon_code = self.handover_coupon(self.receiver, self.user, registered_coupon_id)
        # Given : user login
        self.client.login(username=self.username, password=self.password)

        # When : user try to put UncheckedHandoverCouponListApi
        response = self.client.put(
            path=reverse('unchecked_coupon_list'),
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.OK & message 양도 받은 gift card을 확인하였습니다.
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['message'], '양도 받은 gift card을 확인하였습니다.')
