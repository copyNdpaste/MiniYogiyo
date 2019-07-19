import datetime
import json
from operator import eq
from http import HTTPStatus
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.generic import View
from django.core.mail import BadHeaderError
from django.core.exceptions import ValidationError
from smtplib import SMTPConnectError
from accounts.mixins import LoginRequiredMixin
from accounts.models import User
from accounts.forms import UserForm
from coupon.models import GiftCoupon, UserGiftCoupon
from coupon.forms import GiftCouponForm, AvailableGiftCouponForm
from coupon import helper
from config.settings import base as settings


class GiftCouponApiCreate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            post_data = json.loads(request.body)
            receiver_name = post_data['receiver_name']
            receiver_email = post_data['receiver_email']
            receiver_phone = post_data['receiver_phone']
            sender_msg = post_data['sender_msg']
            price = post_data['price']
        except (json.JSONDecodeError, KeyError):
            data = {
                'error': 'no content'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        coupon_form = GiftCouponForm(
            data=post_data
        )

        if not coupon_form.is_valid():
            if coupon_form.errors:
                data = {
                    'error': coupon_form.errors,
                }
                return JsonResponse(
                    data, status=HTTPStatus.BAD_REQUEST
                )
        user = request.user
        expire_date = datetime.datetime.now() + datetime.timedelta(days=settings.EXPIRATION_PERIOD)
        gift_coupon = GiftCoupon.objects.create(
            sender=user,
            receiver_name=receiver_name,
            receiver_email=receiver_email,
            receiver_phone=receiver_phone,
            sender_msg=sender_msg,
            price=price,
            expire_date=expire_date)

        try:
            helper.send_coupon_email(user, gift_coupon)
        except (BadHeaderError, SMTPConnectError):
            data = {
                'error': 'gift card 발송에 실패했습니다'
            }
            return JsonResponse(data, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        data = {
            'message': 'gift card 발급 완료',
        }

        return JsonResponse(data, status=HTTPStatus.OK)


class GiftCouponRegisterApi(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            post_data = json.loads(request.body)
            coupon_code = post_data['coupon_code']
        except (json.JSONDecodeError, KeyError):
            data = {
                'error': 'no content'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        gift_coupon_obj = GiftCoupon.objects.filter(coupon_code=coupon_code)
        try:
            gift_coupon = gift_coupon_obj[0]
            if gift_coupon.is_used:
                data = {
                    'error': '해당 gift card는 이미 사용 되었습니다.'
                }
                return JsonResponse(data, status=HTTPStatus.CONFLICT)

            registered_coupon = UserGiftCoupon.objects.filter(gift_coupon__coupon_code=coupon_code)
            if registered_coupon.exists():
                data = {
                    'error': '이미 등록된 gift card 입니다.'
                }
                return JsonResponse(data, status=HTTPStatus.CONFLICT)

            UserGiftCoupon.objects.create(
                gift_coupon=gift_coupon,
                user=request.user,
            )

            data = {
                'message': 'gift card 등록 성공'
            }
            return JsonResponse(data, status=HTTPStatus.OK)

        except (IndexError, ValidationError):
            data = {
                'error': '해당 gift card 코드는 존재하지 않습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)


class ReceivedCouponListApi(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        received_coupons = (UserGiftCoupon.objects.select_related('gift_coupon')
                            .filter(user=user).order_by('-created_time'))

        coupons_values = received_coupons.values(
            'id', 'gift_coupon__id', 'gift_coupon__coupon_code', 'gift_coupon__is_used', 'is_owner',
            'prior_user', 'prior_user__username', 'gift_coupon__sender__username', 'gift_coupon__expire_date',
            'gift_coupon__price', 'gift_coupon__created_time', 'created_time',
            )

        today_date = datetime.datetime.now().date()
        coupons = []
        for coupon in coupons_values:
            is_expired = True
            is_available = False
            is_handover = False

            expire_date = coupon['gift_coupon__expire_date']
            is_used = coupon['gift_coupon__is_used']

            if today_date <= expire_date:
                is_expired = False
                if coupon['is_owner'] and not is_used:
                    is_available = True

            if coupon['prior_user'] is None:
                sender_name = coupon['gift_coupon__sender__username']
            else:
                sender_name = coupon['prior_user__username']
                is_handover = True

            coupons += [{
                'registered_coupon_id': coupon['id'],
                'coupon_id': coupon['gift_coupon__id'],
                'coupon_code': coupon['gift_coupon__coupon_code'],
                'price': coupon['gift_coupon__price'],
                'is_used': is_used,
                'is_owner': coupon['is_owner'],
                'sender_name': sender_name,
                'expire_date': expire_date,
                'create_date': coupon['gift_coupon__created_time'].date(),
                'register_date': coupon['created_time'].date(),
                'is_expired': is_expired,
                'is_available': is_available,
                'is_handover': is_handover,
            }]

        if not coupons:
            data = {
                'message': '받은 gift card가 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        data = {
            'coupons': coupons
        }
        return JsonResponse(data, status=HTTPStatus.OK)


class SentCouponListApi(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        sent_coupons = (GiftCoupon.objects
                        .filter(Q(sender=user) | Q(usergiftcoupon__prior_user=user))
                        .order_by('-created_time', '-usergiftcoupon'))

        sent_coupons_values = (
            sent_coupons.annotate(
                coupon_user=F('usergiftcoupon__user__username'),
                prior_user=F('usergiftcoupon__prior_user'),
                prior_username=F('usergiftcoupon__prior_user__username'),
                is_registrant=F('usergiftcoupon__is_registrant')
            ).values('receiver_name', 'price', 'created_time', 'expire_date', 'coupon_code', 'is_registrant',
                     'sender', 'is_used', 'coupon_user', 'prior_user', 'prior_username'))

        coupons = []
        for coupon in sent_coupons_values:
            coupon_user = coupon['coupon_user']
            prior_user = coupon['prior_user']

            is_buyer = False
            is_registered = False
            receiver_name = coupon['receiver_name']

            if coupon['sender'] == user.id and not prior_user:
                is_buyer = True

            if coupon['coupon_user']:
                is_registered = True
                if prior_user:
                    receiver_name = coupon_user

            coupons += [{
                'coupon_code': coupon['coupon_code'],
                'receiver_name': receiver_name,
                'price': coupon['price'],
                'create_date': coupon['created_time'].date(),
                'expire_date': coupon['expire_date'],
                'is_used': coupon['is_used'],
                'is_registrant': coupon['is_registrant'] if is_registered else False,
                'is_registered': is_registered,
                'is_buyer': is_buyer
            }]

        if not coupons:
            data = {
                'message': '보낸 gift card가 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        data = {
            'coupons': coupons
        }
        return JsonResponse(data, status=HTTPStatus.OK)


class AvailableCouponListApi(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user

        available_coupons = (
            UserGiftCoupon.objects.select_related('gift_coupon')
            .filter(
                user=user,
                is_owner=True,
                gift_coupon__is_used=False,
                gift_coupon__expire_date__gte=datetime.datetime.now().date())
            .annotate(
                price=F('gift_coupon__price'),
                create_date=F('gift_coupon__created_time'),
                expire_date=F('gift_coupon__expire_date'),
                coupon_code=F('gift_coupon__coupon_code'),
                prior_username=F('prior_user__username'),
            ).values())

        available_coupon_list = list(available_coupons)

        if not available_coupon_list:
            data = {
                'message': '사용가능한 gift card가 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        data = {
            'coupons': available_coupon_list
        }
        return JsonResponse(data, status=HTTPStatus.OK)


class CouponUseApi(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            post_data = json.loads(request.body)
            receiver_username = post_data['username']
            receiver_email = post_data['email']

        except (KeyError, ValueError):
            data = {
                'error': 'no content'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        user = request.user

        if eq(receiver_username, user.username) or eq(receiver_email, user.email):
            data = {
                'error': '본인에게는 양도할 수 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        user_form = UserForm(data=post_data)

        if not user_form.is_valid():
            if user_form.errors:
                data = {
                    'error': user_form.errors,
                }
                return JsonResponse(
                    data, status=HTTPStatus.BAD_REQUEST
                )

        try:
            receiver = User.objects.exclude(pk=user.pk).get(Q(username=receiver_username) | Q(email=receiver_email))

        except User.MultipleObjectsReturned:
            data = {
                'error': 'username 또는 email을 잘못 입력하였습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.CONFLICT)

        except User.DoesNotExist:
            data = {
                'error': '해당 유저가 존재하지 않습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        try:
            registered_coupon_id = self.kwargs['registered_coupon_id']
            registered_coupon = (UserGiftCoupon.objects.select_related('gift_coupon')
                                 .filter(pk=registered_coupon_id)
                                 .filter(user=user)
                                 .filter(is_owner=True))

            gift_coupon = registered_coupon[0].gift_coupon
            coupon_form = AvailableGiftCouponForm(
                data={
                    'is_used': gift_coupon.is_used,
                    'expire_date': gift_coupon.expire_date,
                    'user': receiver
                }
            )

            if not coupon_form.is_valid():
                data = {
                    'error': coupon_form.errors,
                }
                return JsonResponse(
                    data, status=HTTPStatus.BAD_REQUEST
                )

        except IndexError:
            data = {
                'error': '양도할 수 있는 gift card가 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        registered_coupon.update(is_owner=False)
        UserGiftCoupon.objects.create(
            prior_user=user,
            user=receiver,
            gift_coupon=gift_coupon,
            is_registrant=False,
        )

        data = {
            'receiver_name': receiver.username,
            'coupon_code': gift_coupon.coupon_code,
            'message': 'gift card를 양도하였습니다.'
        }
        return JsonResponse(data, status=HTTPStatus.OK)


class UncheckedHandoverCouponListApi(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        unchecked_handover_coupon_list = (
            UserGiftCoupon.objects.select_related('gift_coupon')
            .filter(
                user=user,
                is_checked=False,
                is_owner=True,
                is_registrant=False)
            .annotate(
                coupon_code=F('gift_coupon__coupon_code'),
                price=F('gift_coupon__price'),
                sender_name=F('prior_user__username'),
                create_time=F('gift_coupon__created_time'),
                expire_date=F('gift_coupon__expire_date')
            ).values())

        if unchecked_handover_coupon_list:
            data = {
                'message': '확인 안한 gift card가 있습니다.',
                'coupons': list(unchecked_handover_coupon_list)
            }

        else:
            data = {
                'message': '확인 안한 gift card가 없습니다.',
                'coupons': ''
            }

        return JsonResponse(data, status=HTTPStatus.OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        unchecked_handover_coupon = (
            UserGiftCoupon.objects.select_related('gift_coupon')
            .filter(
                user=user,
                is_checked=False,
                is_owner=True,
                is_registrant=False))

        result = unchecked_handover_coupon.update(is_checked=True)

        if result == 0:
            data = {
                'message': '이미 확인하였습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        data = {
            'message': '양도 받은 gift card를 확인하였습니다.'
        }
        return JsonResponse(data, status=HTTPStatus.OK)
