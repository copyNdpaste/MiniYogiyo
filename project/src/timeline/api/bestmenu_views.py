import json
from datetime import datetime
from http import HTTPStatus

from django.db.models import Sum, F
from django.http import JsonResponse
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin
from cart.models import CartItem
from order.models import DeliveryStatus
from menu.helpers import get_dong


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
           return obj.strftime('%Y:%m:%d:%H:%M:%S')


class BestSellingAPIView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.address == '':
            return JsonResponse(
                data={"message": "mypage에서 사용자 주소를 입력하세요."},
                status=HTTPStatus.BAD_REQUEST
            )
        user_address = get_dong(request.user.address)
        if user_address is None:
            return JsonResponse(
                data={"message": "mypage에서 주소의 동 입력하세요."},
                status=HTTPStatus.BAD_REQUEST
            )
        try:
            cart_obj = self.request.user.cart_set.order_by('-created_time')[0]
            cart_id = cart_obj.id
        except IndexError:
            return JsonResponse(
                data={"message": "cart가 없습니다."},
                status=HTTPStatus.BAD_REQUEST
            )
        today = datetime.now().date()
        one_hour = 1
        current_hour = datetime.now().hour
        created_hour = current_hour - one_hour
        try:
            order = (
                CartItem.objects
                    .select_related('cart', 'menu')
                    .values(
                    address=F('cart__order__address'),
                    delivery_completed=F('cart__order__delivery_status'),
                    created_time=F('cart__order__created_time'),
                )
                    .filter(
                    address__contains=user_address,
                    delivery_completed=DeliveryStatus.COMPLETE,
                    created_time__date=today,
                    created_time__hour=created_hour,
                )
                    .values(
                    'menu__name',
                )
                    .annotate(
                    menu=F('menu__name'),
                    menu_quantity=Sum('quantity')
                )
                    .values(
                    'menu',
                    'menu_quantity',
                    'menu_id',
                    'menu__img',
                )
                    .order_by('-menu_quantity')[:1]
            )
            order[0]  # check_order_for_except_or_not
            json_data = {
                'order': list(order),
                'address': user_address,
                'start_hour': created_hour,
                'end_hour': current_hour,
                'cart_id': cart_id,
            }
            return JsonResponse(
                json_data
            )
        except:
            return JsonResponse(
                data={
                    "message": "아직 주문이 많은 메뉴가 없습니다. 어서 주문하세요.",
                    "address": user_address,
                },
                status=HTTPStatus.BAD_REQUEST
            )
