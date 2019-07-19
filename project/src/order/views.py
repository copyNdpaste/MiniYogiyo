from django.views.generic import TemplateView


class OrderView(TemplateView):
    template_name = 'order/order.html'


class OrderHistoryListView(TemplateView):
    template_name = 'order/order_history_list.html'
