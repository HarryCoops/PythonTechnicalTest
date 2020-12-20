import json
from unittest import mock

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from bonds import models

class MockResponse:
    def __init__(self, status_code, json_dict):
        self.status_code = status_code
        self.json_dict = json_dict

    def json(self):
        return self.json_dict


class CreateBondTestCase(TestCase):

    def setUp(self):
        user = User(username="test", password="Test_123!")
        user.save()
        self.client = APIClient()
        self.client.force_authenticate(user)

    @mock.patch("requests.get")
    def test_create_bond__valid(self, gleif_get):
        gleif_get.return_value = MockResponse(
            status.HTTP_200_OK, 
            [{"Entity":{"LegalName":{"$":"Test"}}}]
        )
        payload = {
            "isin": "123451232513",
            "size": 100,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        response = self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(models.Bond.objects.filter(isin=payload["isin"])) > 0)

    @mock.patch("requests.get")
    def test_create_bond__invalid_lei_api_gives_400(self, gleif_get):
        gleif_get.return_value = MockResponse(
            status.HTTP_400_BAD_REQUEST, 
            {"message": "400 Bad Request", "status_code": status.HTTP_400_BAD_REQUEST}
        )
        payload = {
            "isin": "123451232514",
            "size": 100,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        response = self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(models.Bond.objects.filter(isin=payload["isin"])), 0)

    @mock.patch("requests.get")
    def test_create_bond__invalid_lei_api_gives_500(self, gleif_get):
        gleif_get.return_value = MockResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR, 
            {
                "message": "500 Internal Server Error", 
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )
        payload = {
            "isin": "123451232514",
            "size": 100,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        response = self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(len(models.Bond.objects.filter(isin=payload["isin"])), 0)

    @mock.patch("requests.get")
    def test_create_bond__invalid_lei_missing_field(self, gleif_get):
        gleif_get.return_value = MockResponse(
            status.HTTP_200_OK, 
            [{"Entity":{"LegalName":{"$":"Test"}}}]
        )
        payload = {
            "isin": "123451232513",
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        response = self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(models.Bond.objects.filter(isin=payload["isin"])), 0)

    @mock.patch("requests.get")
    def test_create_bond__invalid_lei_invalid_isin(self, gleif_get):
        gleif_get.return_value = MockResponse(
            status.HTTP_200_OK, 
            [{"Entity":{"LegalName":{"$":"Test"}}}]
        )
        payload = {
            "isin": "akdjslakda",
            "size": 100,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        response = self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(models.Bond.objects.filter(isin=payload["isin"])), 0)
    
    @mock.patch("requests.get")
    def test_create_bond__invalid_lei_duplicate_isin(self, gleif_get):
        gleif_get.return_value = MockResponse(
            status.HTTP_200_OK, 
            [{"Entity":{"LegalName":{"$":"Test"}}}]
        )
        payload = {
            "isin": "123451232513",
            "size": 100,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        response = self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(models.Bond.objects.filter(isin=payload["isin"])), 1)


class ListBondsTestCase(TestCase):

    @mock.patch("requests.get")
    def setUp(self, gleif_get):
        user = User(username="test", password="Test_123!")
        user.save()
        self.client = APIClient()
        self.client.force_authenticate(user)
        gleif_get.return_value = MockResponse(
            status.HTTP_200_OK, 
            [{"Entity":{"LegalName":{"$":"Test"}}}]
        )
        payload = {
            "isin": "123451232513",
            "size": 100,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        payload = {
            "isin": "123451232514",
            "size": 50,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        payload = {
            "isin": "123451232515",
            "size": 100,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P84",
            "maturity": "2021-12-25"
        }
        self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )
        payload = {
            "isin": "123451232516",
            "size": 50,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P84",
            "maturity": "2022-12-25"
        }
        self.client.post(
            reverse("bonds"), json.dumps(payload), content_type="application/json"
        )

    def test_list_all(self):
        response = self.client.get(
            reverse("bonds")
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 4)

    def test_list_filter_by_size(self):
        response = self.client.get(
            reverse("bonds"), {"size": 50}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 2)

    def test_list_all_by_isin(self):
        response = self.client.get(
            reverse("bonds"), {"isin": "123451232516"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 1)

    def test_list_all_isin_not_present(self):
        response = self.client.get(
            reverse("bonds"), {"isin": "123451232517"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 0)

    def test_list_all_different_user(self):
        new_user = User(username="test-2", password="Test_123!")
        new_user.save()
        client = APIClient()
        client.force_authenticate(new_user)
        response = client.get(
            reverse("bonds")
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 0)

    def test_list_all_by_currency_and_size(self):
        response = self.client.get(
            reverse("bonds"), {"currency": "EUR", "size": 50}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 2)

    def test_list_all_by_maturity(self):
        response = self.client.get(
            reverse("bonds"), {"maturity": "2021-12-25"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 1)