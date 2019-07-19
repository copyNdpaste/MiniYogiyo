import datetime
import json
from http import HTTPStatus

from django.db.models import F, Q
from django.http import JsonResponse
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin
from yosigy.api.forms import YosigyTicketForm
from yosigy.models import YosigyMenu, YosigyTicket, YosigyTiketStatus, Yosigy, TicketPayment


class YosigyDetailAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        요식이 메뉴 리스트를 보여주는 API 
        """

        yosigy_obj = (
            Yosigy.objects.select_related('restaurant', 'user')
                .filter(
                Q(id=self.kwargs['yosigy_id']) &
                Q(deadline__gt=datetime.datetime.now())
            )
                .first()
        )

        if not yosigy_obj:
            return JsonResponse(
                status=HTTPStatus.NOT_FOUND,
                data={
                    'message': '해당하는 요식이가 존재하지 않습니다.'
                }
            )

        yosigy_menu_obj_list = list(
            YosigyMenu.objects.select_related(
                'yosigy',
                'menu',
                'menu__restaurant'
            ).filter(
                yosigy__id=yosigy_obj.id,
            ).annotate(
                is_set_menu=F('menu__is_set_menu')
            ).values(
                'id',
                'menu__id',
                'menu__name',
                'menu__detail',
                'menu__price',
                'menu__img',
                'discounted_price',
                'is_set_menu'
            )
        )

        if not yosigy_menu_obj_list:
            return JsonResponse(
                status=HTTPStatus.NOT_FOUND,
                data={
                    'message': '해당하는 요식이 메뉴가 없습니다.'
                }
            )

        restaurant = {
            'id': yosigy_obj.restaurant_id,
            'img': yosigy_obj.restaurant.img.url,
            'title': yosigy_obj.restaurant.title,
            'yosigy_min_order_price': yosigy_obj.min_price
        }

        owner_set_menu_list = [menu_obj for menu_obj in yosigy_menu_obj_list
                               if menu_obj['is_set_menu'] == True]
        user_custom_menu_list = [menu_obj for menu_obj in yosigy_menu_obj_list
                                 if menu_obj['is_set_menu'] == False]

        json_data = {
            'notice': yosigy_obj.notice,
            'restaurant': restaurant,
            'owner_set_menu_list': owner_set_menu_list,
            'user_custom_menu_list': user_custom_menu_list
        }

        return JsonResponse(
            status=HTTPStatus.OK,
            data=json_data
        )


class YosigyTicketCreateAPIView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        """
        요식이 티켓을 생성하는 API 
        """
        try:
            ticket_obj_list = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '잘못된 요청 입니다.'
                }
            )

        yosigy_menu_queryset = (
            YosigyMenu.objects.select_related(
                'yosigy',
                'menu__restaurant'
            ).filter(
                yosigy__restaurant_id=self.kwargs['restaurant_id'],
            )
        )

        yosigy_menu_id_set = yosigy_menu_queryset.values_list(
            'menu_id', flat=True)

        for ticket in ticket_obj_list:
            if int(ticket['menu_id']) not in yosigy_menu_id_set:
                return JsonResponse(
                    status=HTTPStatus.NOT_FOUND,
                    data={
                        'message': '해당하는 메뉴가 없습니다.'
                    }
                )

        for json_data in ticket_obj_list:
            form = YosigyTicketForm(json_data)
            if not form.is_valid():
                return JsonResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    data={
                        'error': form.errors
                    }
                )

        selected_yosigy_menu_queryset = yosigy_menu_queryset.filter(
            menu_id__in=yosigy_menu_id_set)
        min_order_price = selected_yosigy_menu_queryset.first().yosigy.min_price

        total_discounted_price = sum(
            [int(ticket['quantity']) * int(ticket['discounted_price']) for ticket in ticket_obj_list])

        if total_discounted_price < min_order_price:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    'message': '최소 주문 금액을 넘지 못하였습니다.'
                }
            )

        new_ticket_list = []
        for ticket in ticket_obj_list:
            for _ in range(ticket['quantity']):
                yosigy_ticket = YosigyTicket(
                    user=self.request.user,
                    yosigy_menu_id=int(ticket['yosigy_menu_id']),
                    menu_id=int(ticket['menu_id']),
                    status=YosigyTiketStatus.PUBLISHED,
                    expire_time=datetime.datetime.now() + datetime.timedelta(days=10)
                )
                new_ticket_list.append(yosigy_ticket)

        YosigyTicket.objects.bulk_create(new_ticket_list)

        ticket_payment_obj = TicketPayment.objects.create(
            restaurant_id=self.kwargs['restaurant_id'],
            user=self.request.user,
            total_price=total_discounted_price
        )
        ticket_payment_obj.yosigy_ticket.add(*new_ticket_list)

        return JsonResponse(
            status=HTTPStatus.CREATED,
            data={
                'message': 'e-ticket을 성공적으로 생성하였습니다.'
            }
        )
