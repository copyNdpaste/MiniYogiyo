from cart.models import Cart

USER_FIELDS = ['username', 'email']


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))

    if not fields:
        return
    user = strategy.create_user(**fields)
    Cart.objects.create(user=user)
    return {
        'is_new': True,
        'user': user,
    }
