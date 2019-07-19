from django.shortcuts import render


def yosigy_list(request):
    return render(request, 'yosigy/yosigy_list.html')


def yosigy_detail(request, yosigy_id):
    return render(request, 'yosigy/yosigy_detail.html')


def yosigy_create(request):
    return render(request, 'yosigy/yosigy_create.html')


def yosigy_order_list(request):
    yosigy_check_str = request.GET.get('yosigy-check', '')
    yosigy_check_list = yosigy_check_str.split(',')

    context = {
        'yosigy_check_list': yosigy_check_list,
    }

    return render(request, 'yosigy/yosigy_order.html', context)
