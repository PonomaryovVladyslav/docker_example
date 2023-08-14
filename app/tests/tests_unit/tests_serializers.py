"""Test serialization process"""
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import TestCase, tag
from rest_framework.exceptions import ValidationError

from app.api.serializers import TransactionFileSerializer
from app.models import Transaction


class TestTransactionFileSerializer(TestCase):
    """Class to test file validation via serializer"""

    @tag('unit')
    def test_correct_data_10_rows(self):
        """
        test correct data with 10 rows
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_10_correct.csv')
        with open(path, 'rb') as file:
            serializer = TransactionFileSerializer(data={'data': SimpleUploadedFile(file.name, file.read())})
            serializer.is_valid(raise_exception=True)
            self.assertEqual(len(serializer.transactions), 10)

    @tag('unit')
    def test_correct_data_1_rows(self):
        """
        test correct data with 1 row
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_1_correct.csv')
        with open(path, 'rb') as file:
            serializer = TransactionFileSerializer(data={'data': SimpleUploadedFile(file.name, file.read())})
            serializer.is_valid(raise_exception=True)
            self.assertEqual(len(serializer.transactions), 1)

    @tag('unit')
    def test_correct_data_0_rows(self):
        """
        test correct data without any rows
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_correct_empty.csv')
        with open(path, 'rb') as file:
            serializer = TransactionFileSerializer(data={'data': SimpleUploadedFile(file.name, file.read())})
            serializer.is_valid(raise_exception=True)
            self.assertEqual(len(serializer.transactions), 0)

    @tag('unit')
    def test_emptyfile(self):
        """
        test empty file
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_empty_file.csv')
        with open(path, 'rb') as file:
            serializer = TransactionFileSerializer(data={'data': SimpleUploadedFile(file.name, file.read())})
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    @tag('unit')
    def test_not_a_file(self):
        """
        test if input not a file
        :return: None
        """
        serializer = TransactionFileSerializer(data={'data': "12312"})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestCreateTransactions(TestCase):
    """Test method to put data to the database"""

    @tag('unit')
    def test_not_provided_data(self):
        """
        test if file correct but not contains data
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_correct_empty.csv')
        with open(path, 'rb') as file:
            serializer = TransactionFileSerializer(data={'data': SimpleUploadedFile(file.name, file.read())})
            serializer.is_valid(raise_exception=True)
            serializer.create_transactions()
            self.assertEqual(Transaction.objects.all().count(), 0)

    @tag('unit')
    def test_create_10_objects(self):
        """
        test correct file with 10 rows
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_10_correct.csv')
        with open(path, 'rb') as file:
            serializer = TransactionFileSerializer(data={'data': SimpleUploadedFile(file.name, file.read())})
            serializer.is_valid(raise_exception=True)
            serializer.create_transactions()
            self.assertEqual(Transaction.objects.all().count(), 10)

    @tag('unit')
    def test_create_1_object(self):
        """
        test correct file with only 1 row
        :return: None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_1_correct.csv')
        with open(path, 'rb') as file:
            serializer = TransactionFileSerializer(data={'data': SimpleUploadedFile(file.name, file.read())})
            serializer.is_valid(raise_exception=True)
            serializer.create_transactions()
            self.assertEqual(Transaction.objects.all().count(), 1)

    @tag('unit')
    def test_create_transactions_multiple_times_times(self):
        """
        test running the same method multiple times
        :return:None
        """
        path = Path(settings.BASE_DIR, 'app', 'tests', 'test_files', 'test_data_10_correct.csv')
        with open(path, 'rb') as file:
            serializer = TransactionFileSerializer(data={'data': SimpleUploadedFile(file.name, file.read())})
            serializer.is_valid(raise_exception=True)
            serializer.create_transactions()
            serializer.create_transactions()
            serializer.create_transactions()
            self.assertEqual(Transaction.objects.all().count(), 10)
