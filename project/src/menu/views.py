from django.shortcuts import render


def menu_list(request, category_id):
    context = {
        'category_id': category_id,
    }
    return render(request, 'menu/menu_list.html', context)


def menu_detail(request, category_id, restaurant_id, menu_id):
    context = {
        'category_id': category_id,
        'restaurant_id': restaurant_id,
        'menu_id': menu_id,
    }
    return render(request, 'menu/menu_detail.html', context)


def random_menu_pick_list(request):
    return render(request, 'menu/random_menu_pick_list.html', {})
