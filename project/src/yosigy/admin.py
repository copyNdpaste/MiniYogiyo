from django.contrib import admin
from yosigy.models import Yosigy, YosigyMenu, YosigyTicket, TicketPayment


admin.site.register(Yosigy)
admin.site.register(YosigyMenu)
admin.site.register(YosigyTicket)
admin.site.register(TicketPayment)
