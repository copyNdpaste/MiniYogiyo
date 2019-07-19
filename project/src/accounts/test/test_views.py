# test_views.py
from http import HTTPStatus
from django.test import TestCase
from django.shortcuts import reverse
from accounts.models import User, Taste


class LoginLogoutTestCase(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password!'

        self.user = User.objects.create_user(
            username=self.username, password=self.password)

        response = self.client.get(reverse('home'))
        self.csrf_token = response.cookies.get('csrftoken')

    def test_social_login_view(self):
        # Given : social login
        backend = 'google-oauth2'
        login_url = reverse('social:begin', args=[backend])

        # When : client get social login url
        response = self.client.get(login_url)

        # Then : client will be redirected
        # response should have HTTPStatus.Found
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_logout(self):
        # Given: user Login
        self.client.login(username=self.username, password=self.password)

        # When : User Logout
        response = self.client.get(reverse('logout_api'))

        # Then : response should have message '로그아웃' & HTTPStatus.OK
        self.assertEqual(response.json()['message'], '로그아웃')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_no_login_user_logout(self):
        # Given: user is anonymous

        # When : user Logout
        response = self.client.get(reverse('logout_api'))

        # Then : response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


class MyPageTestCase(TestCase):

    def setUp(self):
        self.username = 'mypage_user'
        self.password = 'mypage_password!'

        self.user = User.objects.create_user(
            username=self.username, password=self.password)

        self.taste_first = Taste.objects.create(name='spicy')
        self.taste_second = Taste.objects.create(name='healthy')
        self.user.tastes.add(self.taste_first, self.taste_second)
        self.user_tastes = self.user.tastes.all()
        self.tastes = Taste.objects.all()

        self.update_data = {
            'phone': '010-1111-2222',
            'address': '서울시 서초구 효령로 332 ',
            'address_detail': '힐스테이트 101동 101호',
            'tastes': [taste['id'] for taste in list(Taste.objects.all().values('id'))],
        }

    @staticmethod
    def user_tastes_out_of_tastes(user_tastes, tastes):
        tastes = [
            {'id': taste.id,
             'name': taste.name,
             'checked': taste in user_tastes} for taste in tastes]
        return tastes

    def test_no_login_user_get_mypage_api_view(self):
        # Given : user is anonymous

        # When : user go to my page
        response = self.client.get(reverse('my_page_api'))

        # Then : response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_get_mypage_api_view(self):
        # Given : user login
        self.client.login(username=self.username, password=self.password)

        # When : user go to my page
        response = self.client.get(reverse('my_page_api'))

        # Then : response should have HTTPStatus.OK
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_user_data(self):
        # Given: user login
        self.client.login(username=self.username, password=self.password)

        # When : user go to my page
        response = self.client.get(reverse('my_page_api'))

        # Then: response should have username and tastes(which inform user's tastes)
        self.assertEqual(response.json()['username'], self.username)
        self.assertEqual(response.json()['tastes'],
                         self.user_tastes_out_of_tastes(self.user_tastes, self.tastes))

    def test_no_login_user_update_mypage(self):
        # Given: user is anonymous

        # When: user update my page
        response = self.client.put(
            path=reverse('my_page_api'),
            data=self.update_data,
            content_type='application/json;charset=utf-8;'
        )

        # Then: response should have HTTPStatus.UNAUTHORIZED
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_update_mypage_with_invalid_form(self):
        # Given: user login
        self.client.login(username=self.username, password=self.password)

        # When: user update my page with invalid form
        response = self.client.put(
            path=reverse('my_page_api'),
            data={
                'phone': '11111-11111-11111111',
                'address': '',
                'address_detail': '',
                'tastes': [self.tastes[0].id],
            },
            content_type='application/json;charset=utf-8;'
        )

        # Then: response should have HTTPStatus.BAD_REQUEST
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_mypage_with_unchecked_tastes(self):
        # Given: user login
        self.client.login(username=self.username, password=self.password)

        # When: user update my page and didn't check his tastes( all tastes are unchecked)
        response = self.client.put(
            path=reverse('my_page_api'),
            data={
                'phone': '1111-1111-1111',
                'address': '',
                'address_detail': '',
                # 'tastes': [self.tastes[0].id],
            },
            content_type='application/json;charset=utf-8;'
        )

        # Then: response should have HTTPStatus.OK & message '수정완료'
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['message'], '수정완료')

    def test_update_mypage_with_update_data(self):
        # Given: user login
        self.client.login(username=self.username, password=self.password)

        # When: user update my page with update_data
        self.client.put(
            path=reverse('my_page_api'),
            data=self.update_data,
            content_type='application/json;charset=utf-8;'
        )

        # Then: user's data is updated
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.phone, self.update_data['phone'])
        self.assertEqual(
            [taste['id'] for taste in list(user.tastes.values())],
            self.update_data['tastes'])

    def test_update_mypage_with_no_update_data(self):
        # Given: user login
        self.client.login(username=self.username, password=self.password)

        # When: user update my page with no data
        response = self.client.put(
            path=reverse('my_page_api'),
            data={},
            content_type='application/json;charset=utf-8;'
        )

        # Then: response should have HTTPStatus.BAD_REQUEST
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'no content')

