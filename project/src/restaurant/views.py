from django.shortcuts import render


def restaurant_list(request, category_id,):
    context = {
        'category_id': category_id,
    }
    return render(request, 'restaurant/restaurant_list.html', context)


def restaurant_detail(request, category_id, restaurant_id):
    context = {
        'category_id': category_id,
        'restaurant_id': restaurant_id,
    }
    return render(request, 'restaurant/restaurant_detail.html', context)
