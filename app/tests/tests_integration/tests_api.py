"""Integration tests for API"""
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, tag
from rest_framework.test import APIClient

from app.models import Transaction


class TestTransactionsPost(TestCase):
    """Class to test post method of /transactions url"""

    def setUp(self):
        """
        Change default client to APIClient
        :return: None
        """
        self.client = APIClient()

    @tag('integration')
    def test_correct_file(self):
        """
        test api with correct file
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_10_correct.csv')
        with open(path, 'rb') as file:
            response = self.client.post('/transactions',
                                        {'data': SimpleUploadedFile(file.name, file.read(),
                                                                    content_type='multipart/form-data')})
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.data, {'count': 10})

    @tag('integration')
    def test_correct_empty_file(self):
        """
        test file with only one record with mistake
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_correct_empty.csv')
        with open(path, 'rb') as file:
            response = self.client.post('/transactions',
                                        {'data': SimpleUploadedFile(file.name, file.read(),
                                                                    content_type='multipart/form-data')})
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.data, {'count': 0})

    @tag('integration')
    def test_empty_file(self):
        """
        test sending empty file
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_empty_file.csv')
        with open(path, 'rb') as file:
            response = self.client.post('/transactions',
                                        {'data': SimpleUploadedFile(file.name, file.read(),
                                                                    content_type='multipart/form-data')})
            self.assertEqual(response.status_code, 400)

    @tag('integration')
    def test_not_file_in_data(self):
        """
        test send not a file through 'data' attribute
        :return: None
        """
        response = self.client.post('/transactions',
                                    {'data': 'some_string'})
        self.assertEqual(response.status_code, 400)

    @tag('integration')
    def test_without_file(self):
        """
        test request without 'data' attribute
        :return: None
        """
        response = self.client.post('/transactions')
        self.assertEqual(response.status_code, 400)


class TestReportGet(TestCase):
    """Class to test GET method of /report API"""

    def setUp(self):
        """Change default client to APIClient"""
        self.client = APIClient()

    @tag('integration')
    def test_empty_report(self):
        """
        test endpoint without setting up any data
        :return: None
        """
        response = self.client.get('/report')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'gross-revenue': Decimal('0.00'),
                                             'expenses': Decimal('0.00'),
                                             'net-revenue': Decimal('0.00')})

    @tag('integration')
    def test_one_transaction_report(self):
        """
        test api after set only 1 transaction record
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_1_correct.csv')
        with open(path, 'rb') as file:
            response = self.client.post('/transactions',
                                        {'data': SimpleUploadedFile(file.name, file.read(),
                                                                    content_type='multipart/form-data')})
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/report')
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.data, {'gross-revenue': Decimal('0.00'),
                                                 'expenses': Decimal('18.77'),
                                                 'net-revenue': Decimal('-18.77')})

    @tag('integration')
    def test_many_transactions_report(self):
        """
        test api after set many transaction records
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_10_correct.csv')
        with open(path, 'rb') as file:
            response = self.client.post('/transactions',
                                        {'data': SimpleUploadedFile(file.name, file.read(),
                                                                    content_type='multipart/form-data')})
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/report')
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.data, {'gross-revenue': Decimal('225.00'),
                                                 'expenses': Decimal('72.93'),
                                                 'net-revenue': Decimal('152.07')})

    @tag('integration')
    def test_many_requests_before_report(self):
        """
        test behaviour if we have more than 1 transaction requests
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_10_correct.csv')
        with open(path, 'rb') as file:
            self.client.post('/transactions',
                             {'data': SimpleUploadedFile(file.name, file.read(),
                                                         content_type='multipart/form-data')})
            self.client.post('/transactions',
                             {'data': SimpleUploadedFile(file.name, file.read(),
                                                         content_type='multipart/form-data')})
            self.client.post('/transactions',
                             {'data': SimpleUploadedFile(file.name, file.read(),
                                                         content_type='multipart/form-data')})
            response = self.client.get('/report')
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.data, {'gross-revenue': Decimal('225.00'),
                                                 'expenses': Decimal('72.93'),
                                                 'net-revenue': Decimal('152.07')})

    def tearDown(self):
        """To clean up database between tests"""
        Transaction.objects.all().delete()
