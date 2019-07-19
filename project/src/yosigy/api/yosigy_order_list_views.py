import ast
from datetime import timedelta
from http import HTTPStatus

from django.db.models import F
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin
from accounts.models import User
from yosigy.models import YosigyTicket, YosigyTiketStatus


class YosigyOrderListAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user.pk
        now_time = timezone.now() + timedelta(hours=9)
        try:
            yosigy_pks = request.GET.get('yosigyPks')
            yosigy_pks = ast.literal_eval(yosigy_pks)
            yosigy_pks_list = [int(i) for i in yosigy_pks]
        except ValueError:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '체크된 요식이가 없습니다. 요식이를 체크 후 사용해주세요 !'
                }
            )
        user_info = (
            User.objects
                .values(
                    'id',
                    'username',
                    'phone',
                    'address',
                    'address_detail',
                )
                .get(pk=user)
        )

        yosigy_order_info = (
            YosigyTicket.objects
                .select_related('menu', 'yosigymenu', )
                .filter(
                    pk__in=yosigy_pks_list,
                    user=user,
                    status__in=[YosigyTiketStatus.PUBLISHED, ],
                    expire_time__gte=now_time,
                )
                .annotate(
                    yosigy_id=F('pk'),
                    expore_time=F('expire_time'),
                    menu_name=F('menu__name'),
                    menu_img=F('menu__img'),
                    menu_detail=F('menu__detail'),
                    price=F('yosigy_menu__discounted_price'),
                    restaurant_id=F('yosigy_menu__yosigy__restaurant__pk'),
                    restaurant_title=F('yosigy_menu__yosigy__restaurant__title')
                )
                .values(
                    'yosigy_id',
                    'expire_time',
                    'menu_name',
                    'menu_img',
                    'menu_detail',
                    'price',
                    'restaurant_id',
                    'restaurant_title',
                )
        )

        if not yosigy_order_info:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '해당 요식이가 없습니다. 확인 후 다시 사용해주세요 !'
                }
            )

        json_data = {
            'yosigy_order_info': list(yosigy_order_info),
            'user_info': user_info
        }

        return JsonResponse(
            json_data
        )
