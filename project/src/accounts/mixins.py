from http import HTTPStatus

from django.http import JsonResponse


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                status=HTTPStatus.UNAUTHORIZED,
                data={
                    'message': '로그인이 필요합니다.',
                }
            )
        return super().dispatch(request, *args, **kwargs)
