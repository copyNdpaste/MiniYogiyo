import uuid

from django.conf import settings
from django.db import models
from django.db.models import F, IntegerField, Sum
from django.utils.functional import cached_property

from config.common_models import TimeStampedModel
from menu.models import Menu

User = settings.AUTH_USER_MODEL


class Cart(TimeStampedModel):
    id = models.UUIDField(
        verbose_name="Cart 식별번호",
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        verbose_name='주문자',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.user.username) + " - " + str(self.id)

    @cached_property
    def total_price(self):
        '''
        주문함에 담긴 메뉴들의 총 가격을 리턴
        '''
        total = 0
        cart_items = CartItem.objects.select_related('menu').filter(cart=self)

        for cart_item in cart_items:
            total += (cart_item.menu.price * cart_item.quantity)
        return total

    @cached_property
    def total_quantity(self):
        '''
        주문함에 담긴 메뉴들의 총 메뉴 개수를 리턴
        '''
        return sum(list(self.cartitem_set.all().values_list(
            'quantity',
            flat=True
        )))


class CartItemQuerySet(models.QuerySet):
    def filtering_user(self, logged_in_user):
        return (self.select_related(
            'menu',
            'cart'
        ).annotate(
            user=F('cart__user'),
            subtotal_price=Sum(
                F('menu__price') * F('quantity'),
                output_field=IntegerField()
            )
        ).filter(
            user=logged_in_user.id
        ).values(
            'cart_id',
            'menu__id',
            'menu__name',
            'menu__detail',
            'menu__img',
            'quantity',
            'menu__price',
            'subtotal_price'
        )
        )


class CartItemManager(models.Manager):
    def get_queryset(self):
        return CartItemQuerySet(
            self.model,
            using=self._db
        )

    def filtering_user(self, logged_in_user):
        return self.get_queryset().filtering_user(logged_in_user)


class CartItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        verbose_name="Cart에 담긴 메뉴",
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Cart,
        verbose_name="Cart Item 들을 담는 카트",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        "특정 Menu의 개수",
        default=1
    )
    objects = CartItemManager()

    def __str__(self):
        return self.menu.name + ' - ' + str(self.quantity)

    @cached_property
    def subtotal_price(self):
        '''
        주문함에 담긴 특정 메뉴들 가격을 리턴
        '''
        return self.menu.price * self.quantity
