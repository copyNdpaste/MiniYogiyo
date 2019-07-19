from django.db.models import Count, Prefetch, Q
from django.http import JsonResponse
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin
from menu.models import MenuTimeLine
from yosigy.models import YosigyMenu
from timeline.models import MenuTimelineComment


class MenuTimeLineAPIView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user

        menu_timeline_queryset = (
            MenuTimeLine.objects
            .select_related(
                'menu',
                'menu__restaurant',
            ).prefetch_related(
                'like',
                'menu__tastes',
                Prefetch('menutimelinecomment_set',
                         queryset=(
                             MenuTimelineComment.objects
                             .select_related('menu_timeline')
                             .filter(is_active=True)
                                )
                         )
            ).filter(
                Q(menu__restaurant__subscribers=user) &
                (~Q(menutimelinecomment__id=None) |
                 Q(menutimelinecomment=None))
            ).annotate(
                comment=Count('menutimelinecomment'),
            )
            .order_by('-created_time')
        )

        yosigymenus = (
            YosigyMenu.objects.all()
        )

        if menu_timeline_queryset:
            last_created_cart = user.cart_set.order_by(
                '-created_time').values_list('id', flat=True)[0]

            liked_menu_timeline= [timeline['id'] for timeline in list(user.menutimeline_set.values('id'))]

            menutimeline_json_data = [
                {
                    'timeline_id': menutimeline_obj.id,
                    'menu_id': menutimeline_obj.menu.id,
                    'menu_name': menutimeline_obj.menu.name,
                    'restaurant_title': menutimeline_obj.menu.restaurant.title,
                    'delivery_charge': menutimeline_obj.menu.restaurant.delivery_charge,
                    'min_order_price': menutimeline_obj.menu.restaurant.min_order_price,
                    'restaurant_img': menutimeline_obj.menu.restaurant.img.url,
                    'status': menutimeline_obj.status,
                    'prior_menu_price': menutimeline_obj.prior_menu_price,
                    'prior_menu_detail': menutimeline_obj.prior_menu_detail,
                    'prior_menu_img': menutimeline_obj.prior_menu_img.url if menutimeline_obj.prior_menu_img else '',
                    'prior_menu_is_yosigy': menutimeline_obj.prior_menu_is_yosigy,
                    'prior_menu_is_set_menu': menutimeline_obj.prior_menu_is_set_menu,
                    'post_menu_price': menutimeline_obj.post_menu_price,
                    'post_menu_detail': menutimeline_obj.post_menu_detail,
                    'post_menu_img': menutimeline_obj.post_menu_img.url if menutimeline_obj.post_menu_img else '',
                    'post_menu_is_yosigy': menutimeline_obj.post_menu_is_yosigy,
                    'post_menu_is_set_menu': menutimeline_obj.post_menu_is_set_menu,
                    'is_recommended': menutimeline_obj.is_recommended,
                    'created_time': menutimeline_obj.created_time.strftime('%Y.%m.%d %H:%M:%S'),
                    'like': (True if menutimeline_obj.id in liked_menu_timeline else False),
                    'like_count': menutimeline_obj.like.count(),
                    'comment_count': menutimeline_obj.menutimelinecomment_set.count(),
                }
                for menutimeline_obj in menu_timeline_queryset
            ]

            for index, menutimeline_obj in enumerate(menu_timeline_queryset):
                temp_taste_list = []
                for taste in menutimeline_obj.menu.tastes.all():
                    temp_taste_list.append(taste.name)
                menutimeline_json_data[index]['tastes'] = temp_taste_list

                for yosigymenu in yosigymenus:
                    if yosigymenu.menu.pk == menutimeline_obj.menu.pk:
                        menutimeline_json_data[index]['yosigy_id'] = yosigymenu.yosigy.pk
                        break

            json_data = {
                'menutimeline': menutimeline_json_data,
                'cart_id': last_created_cart,
            }
        else:
            json_data = {
                'message': '구독 중인 레스토랑이 없거나 전해드릴 메뉴 알림이 없습니다.'
            }
        return JsonResponse(
            data=json_data
        )
