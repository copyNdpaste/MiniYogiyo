from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin


class BoardAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pass
