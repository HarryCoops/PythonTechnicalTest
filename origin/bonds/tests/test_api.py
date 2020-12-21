import json
from unittest import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
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
        self.user = User(username="test", password="Test_123!")
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

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
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(models.Bond.objects.filter(user=self.user, isin=payload["isin"])) > 0)

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
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(models.Bond.objects.filter(user=self.user, isin=payload["isin"])), 0)

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
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(len(models.Bond.objects.filter(user=self.user, isin=payload["isin"])), 0)

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
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(models.Bond.objects.filter(user=self.user, isin=payload["isin"])), 0)

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
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(models.Bond.objects.filter(user=self.user, isin=payload["isin"])), 0)
    
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
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        response = self.client.post(
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(models.Bond.objects.filter(user=self.user, isin=payload["isin"])), 1)


class ListBondsTestCase(TestCase):

    @mock.patch("requests.get")
    def setUp(self, gleif_get):
        self.user = User(username="test", password="Test_123!")
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
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
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        payload = {
            "isin": "123451232514",
            "size": 50,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        self.client.post(
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        payload = {
            "isin": "123451232515",
            "size": 100,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P84",
            "maturity": "2021-12-25"
        }
        self.client.post(
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        payload = {
            "isin": "123451232516",
            "size": 50,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P84",
            "maturity": "2022-12-25"
        }
        self.client.post(
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )

    def test_list__all(self):
        response = self.client.get(
            reverse("bonds-list")
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 4)

    def test_list__filter_by_size(self):
        response = self.client.get(
            reverse("bonds-list"), {"size": 50}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 2)

    def test_list__all_by_isin(self):
        response = self.client.get(
            reverse("bonds-list"), {"isin": "123451232516"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 1)

    def test_list__all_isin_not_present(self):
        response = self.client.get(
            reverse("bonds-list"), {"isin": "123451232517"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 0)

    def test_list__all_different_user(self):
        new_user = User(username="test-2", password="Test_123!")
        new_user.save()
        client = APIClient()
        client.force_authenticate(new_user)
        response = client.get(
            reverse("bonds-list")
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 0)

    def test_list__all_by_currency_and_size(self):
        response = self.client.get(
            reverse("bonds-list"), {"currency": "EUR", "size": 50}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 2)

    def test_list__all_by_maturity(self):
        response = self.client.get(
            reverse("bonds-list"), {"maturity": "2021-12-25"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 1)


class DeleteBondsTestCase(TestCase):

    @mock.patch("requests.get")
    def setUp(self, gleif_get):
        self.user = User(username="test", password="Test_123!")
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
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
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        payload = {
            "isin": "123451232514",
            "size": 50,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "maturity": "2020-12-25"
        }
        self.client.post(
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        payload = {
            "isin": "123451232515",
            "size": 100,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P84",
            "maturity": "2021-12-25"
        }
        self.client.post(
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )
        payload = {
            "isin": "123451232516",
            "size": 50,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P84",
            "maturity": "2022-12-25"
        }
        self.client.post(
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )

    def test_delete__invalid_isin(self):
        response = self.client.delete(
            reverse("bonds-detail", kwargs={"pk": "232131"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete__valid(self):
        response = self.client.delete(
            reverse("bonds-detail", kwargs={"pk": "123451232516"})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(
            len(models.Bond.objects.filter(user=self.user, isin="123451232516")) == 0
        )

    def test_delete__users_cannot_delete_each_others_bonds(self):
        new_user = User(username="test-2", password="Test_123!")
        new_user.save()
        client = APIClient()
        client.force_authenticate(new_user)
        payload = {
            "isin": "123451232511",
            "size": 50,
            "currency": "EUR",
            "lei": "R0MUWSFPU8MPRO8K5P84",
            "maturity": "2022-12-25"
        }
        client.post(
            reverse("bonds-list"), json.dumps(payload), content_type="application/json"
        )


        response = self.client.delete(
            reverse("bonds-detail", kwargs={"pk": "123451232511"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)