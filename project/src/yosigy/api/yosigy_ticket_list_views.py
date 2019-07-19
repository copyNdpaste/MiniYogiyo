from datetime import timedelta
from http import HTTPStatus

from django.db.models import F
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin
from yosigy.models import YosigyTicket, YosigyTiketStatus


class YosigyTicketListAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user.pk
        now_time = timezone.now() + timedelta(hours=9)
        yosigy_ticket = (
            YosigyTicket.objects
                .select_related('yosigy_menu', 'menu', 'user')
                .filter(
                    user=user,
                    status__in=[YosigyTiketStatus.PUBLISHED, YosigyTiketStatus.USED, ],
                    expire_time__gte=now_time,
                )
                .annotate(
                    price=F('yosigy_menu__discounted_price'),
                    restaurant_title=F('yosigy_menu__yosigy__restaurant__title'),
                    restaurant_id=F('yosigy_menu__yosigy__restaurant__pk')
                )
                .values(
                    'pk',
                    'menu__name',
                    'menu__img',
                    'status',
                    'expire_time',
                    'price',
                    'restaurant_title',
                    'restaurant_id',
                )
                .order_by('-created_time')
        )

        if not yosigy_ticket:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '소유하신 요식이가 없습니다. 요식이를 구매 후 이용하세요 !'
                }
            )

        yosigy_ticket_rest = (
            YosigyTicket.objects
                .select_related('yosigy_menu', 'user')
                .filter(user=user, status__in=[YosigyTiketStatus.PUBLISHED, ], expire_time__gte=now_time,)
        )

        json_data = {
            'yosigy_ticket_list': list(yosigy_ticket),
            'yosigy_ticket_rest': len(yosigy_ticket_rest),
        }

        return JsonResponse(
            json_data
        )
