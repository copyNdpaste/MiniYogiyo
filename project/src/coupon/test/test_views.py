# test_views.py
import datetime
from http import HTTPStatus
from django.core import mail
from django.test import TestCase
from django.shortcuts import reverse
from accounts.models import User
from coupon import helper
from coupon.models import GiftCoupon, UserGiftCoupon


class GiftCouponApiCreateTestCase(TestCase):

    def setUp(self):
        self.username = 'coupon_user',
        self.password = 'coupon_password'

        self.user = User.objects.create_user(
            username=self.username, password=self.password)

        self.gift_coupon_data = {
            'receiver_name': '홍길동',
            'receiver_email': 'test190508@gmail.com',
            'receiver_phone': '',
            'sender_msg': '선물입니다.^^',
            'price': '10000',
        }

    def test_user_create_gift_coupon_with_valid_gift_coupon_data(self):
        # Given : user login & gift_coupon_data is given
        self.client.login(username=self.username, password=self.password)
        gift_coupon_data = self.gift_coupon_data

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('create_gift_coupon_api'),
            data=gift_coupon_data,
            content_type='application/json:charset=utf-8;'
        )
        created_gift_coupon = GiftCoupon.objects.filter(sender=self.user).order_by('-created_time')[0]
        msg = mail.outbox[0]
        title, message = helper.set_email_msg(self.user, created_gift_coupon)

        # Then: response should have HTTPStatus.OK & message gift card 발급 완료
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['message'], 'gift card 발급 완료')

        # Then: GiftCoupon was created
        self.assertEqual(created_gift_coupon.receiver_name, self.gift_coupon_data['receiver_name'])

        # Then: mail was sent to receiver_email with intended message
        self.assertEqual(msg.recipients()[0], self.gift_coupon_data['receiver_email'])
        self.assertEqual(msg.subject, title)
        self.assertEqual(msg.body, message)

    def test_anonymous_user_create_gift_coupon(self):
        # Given : user is anonymous

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('create_gift_coupon_api'),
            data={},
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_creat_gift_coupon_with_no_gift_coupon_data(self):
        # Given : user login & no gift_coupon_data
        self.client.login(username=self.username, password=self.password)
        gift_coupon_data = {}

        # When : user try to buy a gift coupon with no gift coupon data
        response = self.client.post(
            path=reverse('create_gift_coupon_api'),
            data=gift_coupon_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.BAD_REQUEST & error 'no content'
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'no content')

    def test_user_create_gift_coupon_with_invalid_gift_coupon_price(self):
        # Given : user login & invalid gift_coupon_data is given
        self.client.login(username=self.username, password=self.password)
        gift_coupon_data = self.gift_coupon_data
        gift_coupon_data['price'] = 6800

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('create_gift_coupon_api'),
            data=gift_coupon_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should have HTTPStatus.BAD_REQUEST
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        # Then: error key: price, value: 천원단위로 금액을 선택해 주세요.
        self.assertEqual(list(response.json()['error'].keys())[0], 'price')
        self.assertEqual(response.json()['error']['price'][0], '천원단위로 금액을 선택해 주세요.')

    def test_user_create_gift_coupon_with_invalid_gift_coupon_email(self):
        # Given : user login & invalid gift_coupon_data is given
        self.client.login(username=self.username, password=self.password)
        gift_coupon_data = self.gift_coupon_data
        gift_coupon_data['receiver_email'] = 'test@gmail'

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('create_gift_coupon_api'),
            data=gift_coupon_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then: response should have HTTPStatus.BAD_REQUEST
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        # Then: error key: email, value: 잘못된 이메일 입나다.
        self.assertEqual(list(response.json()['error'].keys())[0], 'receiver_email')
        self.assertEqual(response.json()['error']['receiver_email'][0], '잘못된 이메일 입나다.')


class GiftCouponRegisterApiTestCase(TestCase):

    def setUp(self):
        self.username = 'coupon_user',
        self.password = 'coupon_password'

        self.user = User.objects.create_user(
            username=self.username, password=self.password)

        self.gift_coupon_data = {
            'receiver_name': '홍길동',
            'receiver_email': 'test190508@gmail.com',
            'receiver_phone': '',
            'sender_msg': '선물입니다.^^',
            'price': '10000',
        }

        self.client.login(username=self.username, password=self.password)
        self.client.post(
            path=reverse('create_gift_coupon_api'),
            data=self.gift_coupon_data,
            content_type='application/json:charset=utf-8;'
        )
        self.client.logout()

        self.created_gift_coupon = GiftCoupon.objects.filter(sender=self.user).order_by('-created_time')[0]

        self.coupon_code_data = {
            'coupon_code': self.created_gift_coupon.coupon_code
        }

    def test_anonymous_user_register_gift_coupon(self):
        # Given : user is anonymous & gift_coupon_code was given
        coupon_code_data = self.coupon_code_data

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('register_gift_coupon_api'),
            data=coupon_code_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_register_gift_coupon_with_valid_coupon_code(self):
        # Given : user login & gift_coupon_code is given
        self.client.login(username=self.username, password=self.password)
        coupon_code_data = self.coupon_code_data

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('register_gift_coupon_api'),
            data=coupon_code_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.OK & message gift card 등록 성공
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['message'], 'gift card 등록 성공')

    def test_user_register_gift_coupon_with_no_coupon_code_data(self):
        # Given : user login & no coupon_code_data
        self.client.login(username=self.username, password=self.password)
        coupon_code_data = {}

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('register_gift_coupon_api'),
            data=coupon_code_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.BAD_REQUEST & error no content
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'no content')

    def test_user_register_gift_coupon_with_invalid_coupon_code(self):
        # Given : user login & no coupon_code_data
        self.client.login(username=self.username, password=self.password)
        invalid_coupon_code_data = {
            'coupon_code': ''.join(reversed(str(self.created_gift_coupon.coupon_code)))
        }

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('register_gift_coupon_api'),
            data=invalid_coupon_code_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.NOT_FOUND & error 해당 gift card 번호는 존재하지 않습니다
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['error'], '해당 gift card 번호는 존재하지 않습니다.')

    def test_user_register_gift_coupon_with_already_registered_coupon(self):
        # Given : user login & coupon_code is already registered
        self.client.login(username=self.username, password=self.password)
        self.client.post(
            path=reverse('register_gift_coupon_api'),
            data=self.coupon_code_data,
            content_type='application/json:charset=utf-8;'
        )

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('register_gift_coupon_api'),
            data=self.coupon_code_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.HTTPStatus.CONFLICT & error '이미 등록된 gift card 입니다.'
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertEqual(response.json()['error'], '이미 등록된 gift card 입니다.')

    def test_user_register_gift_coupon_with_already_used_coupon_code(self):
        # Given : user login & coupon_code is already used
        self.client.login(username=self.username, password=self.password)
        self.created_gift_coupon.is_used = True
        self.created_gift_coupon.save()

        # When : user try to buy a gift coupon
        response = self.client.post(
            path=reverse('register_gift_coupon_api'),
            data=self.coupon_code_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.HTTPStatus.CONFLICT & error '해당 gift card는 이미 사용 되었습니다.'
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertEqual(response.json()['error'], '해당 gift card는 이미 사용 되었습니다.')


class CouponUseApiTestCase(TestCase):

    def setUp(self):
        self.username = 'coupon_user',
        self.password = 'coupon_password'
        self.email = 'coupon_user@gmail.com'

        self.user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email)

        self.sender_name = 'sender_name'
        self.sender_password = 'sender_password'

        User.objects.create_user(
            username=self.sender_name, password=self.sender_password)

        self.receiver = User.objects.create_user(
            username='receiver',
            password='receiver_password',
            email='receiver_email@gmail.com',
        )

        self.receiver_data = {
            'username': self.receiver.username,
            'email': self.receiver.email
        }

    def send_coupon(self):
        sender_name = self.sender_name
        gift_coupon_data = {
            'receiver_name': '아무개',
            'receiver_email': 'test190508@gmail.com',
            'receiver_phone': '',
            'sender_msg': '',
            'price': '30000',
        }

        self.client.login(username=self.sender_name, password=self.sender_password)

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

        registered_coupon_id = UserGiftCoupon.objects.all().order_by('-created_time')[0].id
        return registered_coupon_id

    def test_anonymous_user_handover_coupon(self):
        # Given : user is anonymous & receiver data is given
        receiver_data = self.receiver_data

        # When : user try to hand over coupon
        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': 1}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_handover_coupon(self):
        # Given : sender send coupon & user is login & register coupon & receiver data is given
        coupon_code = self.send_coupon()
        self.client.login(username=self.username, password=self.password)
        registered_coupon_id = self.register_coupon(coupon_code)
        receiver_data = self.receiver_data

        # When : user try to hand over coupon
        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': registered_coupon_id}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.Ok & receiver_name receiver_data's username & message gift card를 양도하였습니다.
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['receiver_name'], receiver_data['username'])
        self.assertEqual(response.json()['message'], 'gift card를 양도하였습니다.')

        # Then : new usergiftcoupon whose prior user is user& user is receiver was created
        usergiftcoupon = UserGiftCoupon.objects.all().order_by('-created_time')[0]
        self.assertEqual(usergiftcoupon.prior_user, self.user)
        self.assertEqual(usergiftcoupon.user, self.receiver)

    def test_user_handover_coupon_with_no_receiver_data(self):
        # Given : sender send coupon & register coupon & user is login & no receiver data
        coupon_code = self.send_coupon()
        self.client.login(username=self.username, password=self.password)
        registered_coupon_id = self.register_coupon(coupon_code)
        receiver_data = {}

        # When : user try to hand over coupon
        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': registered_coupon_id}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.BAD_REQUEST & error no content.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'no content')

    def test_user_handover_coupon_to_no_mini_ygy_user(self):
        '''
        미니 요기요 사이트에 없는 유저에게 gift card 양도 요청을 보내는 경우
        '''
        # Given : sender send coupon & user is login & register coupon & receiver_data has non user
        coupon_code = self.send_coupon()
        self.client.login(username=self.username, password=self.password)
        registered_coupon_id = self.register_coupon(coupon_code)
        receiver_data = {
            'username': 'not_user',
            'email': 'not_user@gmail.com'
        }

        # When : user try to hand over coupon
        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': registered_coupon_id}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.NOT Found
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['error'], '해당 유저가 존재하지 않습니다.')

    def test_user_handover_coupon_with_invalid_email(self):
        # Given : sender send coupon & user is login & register coupon & receiver_data has invalid email
        coupon_code = self.send_coupon()
        self.client.login(username=self.username, password=self.password)
        registered_coupon_id = self.register_coupon(coupon_code)
        self.receiver_data['email'] = 'invalid.email'
        receiver_data = self.receiver_data

        # When : user try to hand over coupon
        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': registered_coupon_id}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.BAD_REQUEST & error email Enter a valid email address.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error']['email'][0], 'Enter a valid email address.')

    def test_user_handover_already_used_coupon(self):
        # Given : sender send coupon & user is login & register coupon & receiver_data is given
        coupon_code = self.send_coupon()
        self.client.login(username=self.username, password=self.password)
        registered_coupon_id = self.register_coupon(coupon_code)
        receiver_data = self.receiver_data

        # Given : coupon which will be handed over was already used
        is_used = True
        GiftCoupon.objects.filter(usergiftcoupon=registered_coupon_id).update(is_used=is_used)

        # When : user try to hand over coupon
        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': registered_coupon_id}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.BAD_REQUEST & error is_used 이미 사용된 gift card입니다.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error']['is_used'][0], '이미 사용된 gift card입니다.')

    def test_user_handover_unavailable_coupon(self):
        # Given : sender send coupon & user is login & register coupon & receiver_data is given
        coupon_code = self.send_coupon()
        self.client.login(username=self.username, password=self.password)
        registered_coupon_id = self.register_coupon(coupon_code)
        receiver_data = self.receiver_data

        # Given : coupon is not available to hand over because user do not own the coupon(is_owner=False)
        UserGiftCoupon.objects.filter(pk=registered_coupon_id).update(is_owner=False)

        # When : user try to hand over coupon
        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': registered_coupon_id}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.NOT_FOUND & error 양도할 수 있는 gift card가 없습니다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json()['error'], '양도할 수 있는 gift card가 없습니다.')

    def test_user_handover_coupon_whose_expire_date_is_already_over(self):
        # Given : sender send coupon & user is login & register coupon & receiver_data is given
        coupon_code = self.send_coupon()
        self.client.login(username=self.username, password=self.password)
        registered_coupon_id = self.register_coupon(coupon_code)
        receiver_data = self.receiver_data

        # Given : coupon's expire_date is already over - expire_date was yesterday
        gift_coupon_obj = GiftCoupon.objects.filter(usergiftcoupon=registered_coupon_id)
        over_expire_date = datetime.datetime.now()-datetime.timedelta(days=1)
        gift_coupon_obj.update(expire_date=over_expire_date)

        # When : user try to hand over coupon
        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': registered_coupon_id}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.BAD_REQUEST & error expire_date 이미 사용된 gift card입니다.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error']['expire_date'][0], '만료된 gift card입니다.')

    def test_user_handover_to_himself(self):
        # Given : sender send coupon & user is login & register coupon & receiver_data has user's username
        coupon_code = self.send_coupon()
        self.client.login(username=self.username, password=self.password)
        registered_coupon_id = self.register_coupon(coupon_code)
        receiver_data = {
            'username': self.username,
            'email': self.email
        }

        # When : user try to hand over coupon
        response = self.client.post(
            path=reverse('coupon_use_api', kwargs={'registered_coupon_id': registered_coupon_id}),
            data=receiver_data,
            content_type='application/json:charset=utf-8;'
        )

        # Then : response should have HTTPStatus.NOT_FOUND & error 해당 유저가 존재하지 않습니다.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error'], '본인에게는 양도할 수 없습니다.')
