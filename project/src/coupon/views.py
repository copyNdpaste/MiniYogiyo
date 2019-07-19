import datetime
from django.shortcuts import render, reverse


def gift_coupon(request):
    return render(request, 'coupon/gift_coupon.html', {'page': 'present'})


def register_coupon(request):
    return render(request, 'coupon/register_coupon.html', {'page': 'register'})


def register_coupon_code(request, coupon_code):

    response = render(request, 'coupon/register_coupon.html', {'page': 'register'})

    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=60*10),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie('coupon_code',
                        coupon_code,
                        expires=expires)
    return response


def my_coupon(request):
    return render(request, 'coupon/index.html', {'page': 'coupon_list'})


def received_coupon(request):
    return render(request, 'coupon/received_coupon_list.html', {'page': 'coupon_list'})


def sent_coupon(request):
    return render(request, 'coupon/sent_coupon_list.html', {'page': 'coupon_list'})


def available_coupon(request):
    return render(request, 'coupon/available_coupon_list.html', {'page': 'coupon_list'})
