from random import randint

from django.conf import settings
from django.db.models import Count, F, Sum

from django_bulk_update.helper import bulk_update
from django.http import JsonResponse

from background_task import background

from cart.models import Cart
from menu.models import Menu
from order.models import DeliveryStatus


def calc_score(menu_queryset, weight):
    """
    조회수, 좋아요 점수 부여하는 부분에서 겹치는 부분을 함수로 구현
    """
    score_sum = 0
    if not menu_queryset.exists():
        return False, score_sum, menu_queryset

    for index, menu in enumerate(menu_queryset):
        if index >= settings.TOP_FIVE:
            score = weight * settings.DEFAULT_SCORE
            menu.score += score
        else:
            score = weight * (settings.TOP_SCORE - index)
            menu.score += score
        score_sum += score

    return True, score_sum, menu_queryset


def update_random_score(query, weight):
    """
    랜덤으로 점수를 생성하고, 합 한다.
    """
    added_score = 0
    score_sum = 0
    if query.exists():
        for menu in query:
            added_score = randint(
                settings.DEFAULT_SCORE + 1,
                settings.TOP_SCORE) * weight
            menu.score = added_score
            score_sum += added_score
        bulk_update(query, update_fields=['score'])
    return score_sum


def update_hit_count_or_like(hit_or_like_desc_menu_queryset, weight):
    """
    조회수, 좋아요에 대해서 TOP 5 순위를 매겨서, 점수를 생성하고 합한다.
    """
    exists, score_sum, result_menu_queryset = calc_score(
        hit_or_like_desc_menu_queryset, weight)
    if exists:
        bulk_update(result_menu_queryset, update_fields=['score'])
    return score_sum


def update_order_count_score(all_menu, order_desc_menu_id, weight):
    """
    주문수 TOP 5 순위를 매겨서, 점수를 생성하고 합한다.
    """
    order_desc_menu_queryset = all_menu.filter(id__in=order_desc_menu_id)
    exists, score_sum, result_menu_queryset = calc_score(
        order_desc_menu_queryset, weight)
    if exists:
        bulk_update(result_menu_queryset, update_fields=['score'])
    return score_sum


def update_is_recommended_or_not(recommended, weight):
    """
    사장님 추천 메뉴인지를 확인하고, 점수를 생성해서 합한다.
    """

    is_recommended_menu = Menu.objects.filter(is_recommended=recommended)
    score_sum = 0
    if is_recommended_menu.exists():
        if recommended:
            is_recommended_menu.update(
                score=F('score') + (settings.TOP_SCORE * weight))
            score_sum += settings.TOP_SCORE * weight
        else:
            is_recommended_menu.update(
                score=F('score') + (settings.DEFAULT_SCORE * weight))
            score_sum += settings.DEFAULT_SCORE * weight
    return score_sum


@background
def update_score():
    """
    위의 점수를 update 하는 함수들을 실행한다.
    """
    all_menu = Menu.objects.all()
    hit_count_desc = all_menu.order_by('-hit')
    like_count_desc = (all_menu
                       .annotate(num_like=Count('like'))
                       .order_by('-num_like'))
    order_count_desc = (Cart.objects
                        .prefetch_related('order')
                        .filter(order__delivery_status=DeliveryStatus.COMPLETE)
                        .values('cartitem__menu__name')
                        .annotate(
                            menu=F('cartitem__menu__name'),
                            quantity=Sum('cartitem__quantity')
                        )
                        .order_by('-quantity')
                        .values_list(
                            F('cartitem__menu__id'),
                            flat=True
                        ))

    random_score = update_random_score(
        all_menu,
        settings.RANDOM_SCORE_WEIGHT
    )
    hit_score = update_hit_count_or_like(
        hit_count_desc,
        settings.HIT_SCORE_WEIGHT
    )
    like_score = update_hit_count_or_like(
        like_count_desc,
        settings.LIKE_SCORE_WEIGHT
    )
    order_score = update_order_count_score(
        all_menu,
        order_count_desc,
        settings.ORDER_SCORE_WEIGHT
    )
    is_recommend_score = update_is_recommended_or_not(
        True,
        settings.RECOMMENDED_SCORE_WEIGHT
    )
    is_not_recommend_score = update_is_recommended_or_not(
        False,
        settings.RECOMMENDED_SCORE_WEIGHT
    )
    result_score_sum = (
        random_score +
        hit_score +
        like_score +
        order_score +
        is_recommend_score +
        is_not_recommend_score
    )

    return result_score_sum
