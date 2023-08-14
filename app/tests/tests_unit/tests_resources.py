"""File to unit test files with views (controllers)"""
from pathlib import Path

from django.conf import settings
from django.test import TestCase, tag
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory

from app.api.resources import TransactionView, ReportView
from app.models import Transaction


class TestTransactionsView(TestCase):
    """Class to test transactions view"""

    @tag('unit')
    def test_post_correct(self):
        """
        test correct request
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_10_correct.csv')
        with open(path, 'rb') as file:
            request = APIRequestFactory().post('/transactions',
                                               {'data': SimpleUploadedFile(file.name, file.read(),
                                                                           content_type='multipart/form-data')})
            response = TransactionView.as_view()(request)
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.data, {'count': 10})
            self.assertEqual(Transaction.objects.all().count(), 10)

    @tag('unit')
    def test_post_correct_empty_file(self):
        """
        test correct file with only one record with mistake
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_correct_empty.csv')
        with open(path, 'rb') as file:
            request = APIRequestFactory().post('/transactions',
                                               {'data': SimpleUploadedFile(file.name, file.read(),
                                                                           content_type='multipart/form-data')})
            response = TransactionView.as_view()(request)
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.data, {'count': 0})
            self.assertEqual(Transaction.objects.all().count(), 0)

    @tag('unit')
    def test_post_empty_file(self):
        """
        test sending empty file
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_empty_file.csv')
        with open(path, 'rb') as file:
            request = APIRequestFactory().post('/transactions',
                                               {'data': SimpleUploadedFile(file.name, file.read(),
                                                                           content_type='multipart/form-data')})
            response = TransactionView.as_view()(request)
            self.assertEqual(response.status_code, 400)

    @tag('unit')
    def test_post_without_file(self):
        """
        test request without file
        :return: None
        """
        request = APIRequestFactory().post('/transactions')
        response = TransactionView.as_view()(request)
        self.assertEqual(response.status_code, 400)


class TestReportView(TestCase):
    """Class to test report view"""

    @tag('unit')
    def test_get(self):
        """
        test get request
        :return: None
        """
        request = APIRequestFactory().get('/report')
        response = ReportView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {
            "gross-revenue": 0,
            "expenses": 0,
            "net-revenue": 0,
        })
