from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class CategoryTestClass(TestCase):
    def test_home_page_should_be_opened_on_request(self):
        # Given
        url = reverse("home")
        # When
        response = self.client.get(url)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_category_should_be_shown_on_request(self):
        # Given
        url = reverse("category_api:category_list_api")
        # When
        response = self.client.get(url)
        # Then
        self.assertEqual(response.status_code, HTTPStatus.OK)
