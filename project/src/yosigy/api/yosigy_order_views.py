import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin
from yosigy.forms import YosigyOrderModelForm
from yosigy.models import YosigyTicket, YosigyTiketStatus


class YosigyOrderAPIView (LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            yosigy_order_data = json.loads(request.body)
            yosigy_ticket_list = yosigy_order_data['yosigy_ticket']
            not_used_yosigy = self.yosigy_ticket_is_used_check(yosigy_ticket_list)
            if not not_used_yosigy:
                return JsonResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    data={
                        'message': '사용할 수 없는 요식이가 있습니다.'
                    }
                )
        except json.JSONDecodeError:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '잘못된 요청 입니다.'
                }
            )

        form = YosigyOrderModelForm(yosigy_order_data)

        if form.is_valid():
            self.yosigy_ticket_update(yosigy_ticket_list)
            yosigy_order_obj = form.save()
            json_data = {
                'yosigy_order_id': yosigy_order_obj.id,
                'message': '요식이를 사용했습니다.'
            }
            return JsonResponse(
                status=HTTPStatus.CREATED,
                data=json_data
            )
        else:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '폼이 유효하지 않습니다.',
                    'error': form.errors
                }
            )

    def yosigy_ticket_update(self, yosigy_ticket_list):
        for yosigy_id in yosigy_ticket_list:
            (YosigyTicket.objects
                .filter(
                    pk=yosigy_id
                ).update(
                    status=YosigyTiketStatus.USED
                )
            )

    def yosigy_ticket_is_used_check(self, yosigy_ticket_list):
        not_used_yosigy = YosigyTicket.objects.filter(pk__in=yosigy_ticket_list, status=YosigyTiketStatus.PUBLISHED)

        if not not_used_yosigy:
            return False
        else:
            return True
