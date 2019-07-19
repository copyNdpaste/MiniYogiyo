import json
from http import HTTPStatus
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from django.db.models import Count, F, Prefetch
from accounts.mixins import LoginRequiredMixin
from yosigy.models import TicketPayment, YosigyTicket
from yosigy.helpers import DateTimeFormatEncoder


class YosigyTicketPaymentListAPIView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        user_ticket_payment = (
            user.ticketpayment_set.select_related('restaurant').all()
                .annotate(
                    restaurant_name=F('restaurant__title'),
                    restaurant_img=F('restaurant__img'),
                    ticket_count=Count('yosigy_ticket')
                )
            .order_by('-created_time').values(
            ))

        if not user_ticket_payment:
            data = {
                'username': user.username,
                'error': '구매한 티켓이 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        data = {
            'username': user.username,
            'ticket_payments': list(user_ticket_payment)
        }
        return HttpResponse(
            content=json.dumps(data, cls=DateTimeFormatEncoder),
            status=HTTPStatus.OK,
            content_type='application/json')


class YosigyTicketPaymentDetailAPIView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user

        ticket_payment_qs = TicketPayment.objects.filter(user=user, id=kwargs['ticket_payment_id'])

        tickets_qs = (
            ticket_payment_qs
            .select_related('restaurant')
            .prefetch_related(
                Prefetch(
                    'yosigy_ticket',
                    queryset=YosigyTicket.objects.select_related('menu', 'yosigy_menu'))))

        try:
            ticket_payment = list(tickets_qs)[0]

        except IndexError:
            data = {
                'error': '해당 구매 내역이 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        ticket_payment_info = {
            'id': ticket_payment.id,
            'restaurant_id': ticket_payment.restaurant.id,
            'restaurant_img': str(ticket_payment.restaurant.img),
            'restaurant_name': ticket_payment.restaurant.title,
            'total_price': ticket_payment.total_price,
            'created_time': ticket_payment.created_time.strftime('%Y-%m-%d %H:%M'),
            'yosigy_tickets': [
                {
                    'yosigy_ticket_id': yosigy_ticket.id,
                    'ticket_menu': yosigy_ticket.menu.name,
                    'menu_id': yosigy_ticket.menu.id,
                    'menu_price': yosigy_ticket.menu.price,
                    'menu_img': str(yosigy_ticket.menu.img),
                    'ticket_menu_price': yosigy_ticket.yosigy_menu.discounted_price,
                    'ticket_expire_time': yosigy_ticket.expire_time.strftime('%Y-%m-%d %H:%M')
                }
                for yosigy_ticket in ticket_payment.yosigy_ticket.all()
            ]
        }

        return JsonResponse(data=ticket_payment_info, status=HTTPStatus.OK)
