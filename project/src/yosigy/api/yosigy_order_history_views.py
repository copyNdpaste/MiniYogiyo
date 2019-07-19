from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin


class YosigyOrderHistoryAPIView(LoginRequiredMixin, View):
    pass
