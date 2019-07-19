from django.shortcuts import render
from .models import Category


def category_list(request):
    category_list = Category.objects.all()

    context = {
        'category_list': category_list,
    }
    return render(request, 'home/home.html', context)
