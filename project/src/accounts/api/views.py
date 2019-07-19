import json
from http import HTTPStatus
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.generic import View
from accounts.mixins import LoginRequiredMixin
from accounts.models import Taste, User
from accounts.forms import MyPageForm


class LogoutApiView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        logout(request)
        data = {
            'message': '로그아웃',
        }
        return JsonResponse(data, status=HTTPStatus.OK)


class MyPageApiView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        user_tastes = request.user.tastes.all()
        all_tastes = Taste.objects.all()
        tastes = [
            {'id': taste.id,
             'name': taste.name,
             'checked': taste in user_tastes} for taste in all_tastes]

        data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'address_detail': user.address_detail,
            'tastes': tastes,
        }

        return JsonResponse(data, status=HTTPStatus.OK)

    def put(self, request, *args, **kwargs):
        try:
            put_data = json.loads(request.body)
            phone = put_data['phone']
            address = put_data['address']
            address_detail = put_data['address_detail']
        except (json.JSONDecodeError, KeyError):
            data = {
               'error': 'no content'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        mypage_form = MyPageForm(
            data=put_data
        )

        if not mypage_form.is_valid():
            if mypage_form.errors:
                data = {
                    'error': mypage_form.errors.as_json(),
                }
                return JsonResponse(
                    data, status=HTTPStatus.BAD_REQUEST)

        user = request.user
        user.phone = phone
        user.address = address
        user.address_detail = address_detail
        user.save()

        try:
            user.tastes.clear()

            tastes_data = put_data['tastes']

            if isinstance(tastes_data, str):
                user.tastes.add(put_data['tastes'])

            elif isinstance(tastes_data, list):
                user.tastes.add(*put_data['tastes'])

        except KeyError:
            pass

        data = {
            'message': '수정완료',
        }
        return JsonResponse(data, status=HTTPStatus.OK)
