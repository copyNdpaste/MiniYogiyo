from django.views.generic import View

from accounts.mixins import LoginRequiredMixin


class GroupPurChaseDetailAPIView(LoginRequiredMixin, View):
    """
    
    """

    def get(self, request, *args, **kwargs):
        pass
