"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),

    path('api/category/', include('category.api.urls')),

    path('', include('restaurant.urls')),
    path('', include('restaurant.api.urls')),

    path('', include('menu.urls')),
    path('', include('menu.api.urls')),

    path('cart/', include('cart.urls')),
    path('api/cart/', include('cart.api.urls')),

    path('accounts/', include('accounts.urls')),
    path('api/accounts/', include('accounts.api.urls')),

    path('coupon/', include('coupon.urls')),
    path('api/coupon/', include('coupon.api.urls')),

    path('auth/', include('social_django.urls', namespace='social')),

    path('order/', include('order.urls')),
    path('api/order/', include('order.api.urls')),

    path('timeline/', include('timeline.urls')),
    path('api/timeline/', include('timeline.api.urls')),

    path('grouppurchase/', include('grouppurchase.urls')),
    path('api/grouppurchase/', include('grouppurchase.api.urls')),

    path('yosigy/', include('yosigy.urls')),
    path('api/yosigy/', include('yosigy.api.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
