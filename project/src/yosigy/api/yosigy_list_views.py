import enum
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import F, Count

from django.http import JsonResponse
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin

from restaurant.api.views import CategoryNum
from yosigy.models import Yosigy


class YosigyListInfo(enum.IntEnum):
    POST_TO_SHOW_IN_ONE_PAGE = 4
    PAGES_TO_SHOW = 3


class YosigyListAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs['category_id']
        today = datetime.now().date()
        tab_value = request.GET.get('tab_value', '')
        json_data = {}
        if kwargs['page']:
            self.page = kwargs['page']

        if not category_id or category_id == CategoryNum.ALL_ID:
            yosigy = (
                Yosigy.objects
                    .select_related('restaurant')
                    .prefetch_related('yosigymenu_set')
                    .filter(
                        restaurant__is_yosigy=True,
                        deadline__gte=today,
                    )
                    .values(
                        'restaurant',
                    )
                    .annotate(
                        is_yosigy_count=Count('yosigymenu__menu'),
                    )
                    .values(
                        'pk',
                        'is_yosigy_count',
                        restaurant_title=F('restaurant__title'),
                        restaurant_img=F('restaurant__img'),
                        yosigy_deadline=F('deadline'),
                        yosigy_notice=F('notice'),
                    )
                    .order_by('-created_time')
                )
        else:
            yosigy = (
                Yosigy.objects
                    .select_related('restaurant')
                    .prefetch_related('yosigymenu_set')
                    .filter(
                        restaurant__is_yosigy=True,
                        deadline__gte=today,
                        restaurant__category__pk=category_id,
                    )
                    .values(
                        'restaurant',
                    )
                    .annotate(
                        is_yosigy_count=Count('yosigymenu__menu'),
                    )
                    .values(
                        'pk',
                        'is_yosigy_count',
                        restaurant_title=F('restaurant__title'),
                        restaurant_img=F('restaurant__img'),
                        yosigy_deadline=F('deadline'),
                        yosigy_notice=F('notice'),
                    )
                    .order_by('-created_time')
                )
        yosigy_set = (
            Yosigy.objects
                .select_related('restaurant')
                .prefetch_related('yosigymenu_set')
                .filter(yosigymenu__menu__is_set_menu=True,)
                .annotate(
                    is_set_menu_count=Count('yosigymenu__menu'),
                )
                .values(
                    'is_set_menu_count',
                    'pk',
                )
            )
        for i in yosigy:
            for j in yosigy_set:
                if i['pk'] == j['pk']:
                    i['is_set_menu_count'] = j['is_set_menu_count']
        yosigy=list(yosigy)

        if not yosigy:
            json_data = {
                'message': '아직 공동 구매할 수 있는 메뉴가 없습니다.',
            }
        elif tab_value == 'deadline':
            yosigy=sorted(yosigy, key=lambda menu:menu['yosigy_deadline'])
            json_data = self.yosigy_paginator(yosigy)
            json_data['deadline'] = True
        elif tab_value == 'all' or tab_value == '':
            json_data = self.yosigy_paginator(yosigy)
            json_data['all'] = True

        return JsonResponse(
            json_data
        )

    def yosigy_paginator(self, yosigy):
        paginator = Paginator(yosigy, YosigyListInfo.POST_TO_SHOW_IN_ONE_PAGE)
        current_page = paginator.get_page(self.page)

        start = (self.page-1) // YosigyListInfo.PAGES_TO_SHOW * YosigyListInfo.PAGES_TO_SHOW + 1
        end = start + YosigyListInfo.PAGES_TO_SHOW

        last_page = len(paginator.page_range)

        if last_page < end:
            end = last_page

        yosigy_list = current_page.object_list

        page_range = range(start, end + 1)

        yosigy_list_data = {
            'yosigy_list': yosigy_list,
            'current_page': {
                'has_previous': current_page.has_previous(),
                'has_next': current_page.has_next(),
            },
            'page_range': [page_range[0], page_range[-1]],
        }

        if current_page.has_previous():
            yosigy_list_data['current_page']['previous_page_number'] = current_page.previous_page_number()
        if current_page.has_next():
            yosigy_list_data['current_page']['next_page_number'] = current_page.next_page_number()

        return yosigy_list_data
