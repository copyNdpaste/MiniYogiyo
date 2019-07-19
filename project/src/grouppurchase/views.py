from django.shortcuts import render


def grouppurchase_list(request):
    return render(request, 'grouppurchase/grouppurchase_list.html')


def grouppurchase_detail(request, grouppurchase_id):
    return render(request, 'grouppurchase/grouppurchase_detail.html')


def grouppurchase_create(request):
    return render(request, 'grouppurchase/grouppurchase_create.html')
