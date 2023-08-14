"""File to test utility functions"""
from datetime import datetime
from decimal import Decimal

from django.test import TestCase, tag

from app.api.exceptions import InvalidInput
from app.api.utils import validate_and_prepare_transaction_row, get_report_data
from app.models import Transaction


class TestUtilsValidateTransactionRow(TestCase):
    """Class to test function which validate and transform rows from file"""
    @tag('unit')
    def test_correct_row_expense(self):
        """
        test correct data with type expense
        :return: None
        """
        row = b"2020-07-01, Expense, 18.77, Fuel"
        result = validate_and_prepare_transaction_row(row)
        self.assertDictEqual(result, {'date': datetime(2020, 7, 1, 0, 0),
                                      'type': 'e',
                                      'expense_category': 'Fuel',
                                      'value': Decimal('18.77')})

    @tag('unit')
    def test_correct_row_income(self):
        """
        test correct data with type income
        :return: None
        """
        row = b"2020-10-13, Income, 12.12, some string"
        result = validate_and_prepare_transaction_row(row)
        self.assertDictEqual(result, {'date': datetime(2020, 10, 13, 0, 0), 'type': 'i',
                                      'job_address': 'some string', 'value': Decimal('12.12')})

    @tag('unit')
    def test_not_bytes_row(self):
        """
        test not bytes type input
        :return: None
        """
        row = "1,2,3,4,5"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_3_elements_row(self):
        """
        test incorrect elements count
        :return: None
        """
        row = b"2020-07-01, Expense, 18.77"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_5_elements_row(self):
        """
        test incorrect elements count
        :return: None
        """
        row = b"2020-07-01, Expense, 18.77, test, test"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_empty_string(self):
        """
        test empty string
        :return: None
        """
        row = b""
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_incorrect_type(self):
        """
        test incorrect type
        :return: None
        """
        row = b"2020-10-13, Wrong, 12.12, some string"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_incorrect_date1(self):
        """
        test incorrect date type
        :return: None
        """
        row = b"Wrong, Expense, 12.12, some string"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_incorrect_date2(self):
        """
        test incorrect date type
        :return: None
        """
        row = b"12-12-2002, Expense, 12.12, some string"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_incorrect_date3(self):
        """
        test incorrect date type
        :return: None
        """
        row = b"Sep 12 2022, Expense, 12.12, some string"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_incorrect_date4(self):
        """
        test incorrect date type
        :return: None
        """
        row = b"2022-02-30, Expense, 12.12, some string"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_incorrect_value1(self):
        """
        test incorrect value format
        :return: None
        """
        row = b"2022-02-30, Expense, 2020-02-29, some string"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_incorrect_value2(self):
        """
        test incorrect value format
        :return: None
        """
        row = b"2022-02-30, Expense, 123asd, some string"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_incorrect_value3(self):
        """
        test incorrect value format
        :return: None
        """
        row = b"2022-02-30, Expense, True, some string"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_incorrect_value4(self):
        """
        test incorrect value format
        :return: None
        """
        row = b"2022-02-30, Expense, {1, 2, 3}, some string"
        with self.assertRaises(InvalidInput):
            validate_and_prepare_transaction_row(row)

    @tag('unit')
    def test_convert_value_round1(self):
        """
        test rounding
        :return: None
        """
        row = b"2022-02-10, Expense, 11.11111, some string"
        result = validate_and_prepare_transaction_row(row)
        self.assertEqual(result.get('value'), Decimal('11.11'))

    @tag('unit')
    def test_convert_value_round2(self):
        """
        test rounding
        :return: None
        """
        row = b"2022-02-10, Expense, 55.555, some string"
        result = validate_and_prepare_transaction_row(row)
        self.assertEqual(result.get('value'), Decimal('55.56'))

    @tag('unit')
    def test_convert_value_round3(self):
        """
        test rounding
        :return: None
        """
        row = b"2022-02-10, Expense, 999.9999, some string"
        result = validate_and_prepare_transaction_row(row)
        self.assertEqual(result.get('value'), Decimal('1000.00'))


class TestUtilsGetReportData(TestCase):
    """Test function to prepare data from database"""
    @tag('unit')
    def test_empty_dict(self):
        """
        test if database is empty
        :return: None
        """
        data = get_report_data()
        self.assertDictEqual(data, {
            "gross-revenue": 0,
            "expenses": 0,
            "net-revenue": 0,
        })

    @tag('unit')
    def test_add_income(self):
        """
        test if database has only one record type income
        :return: None
        """
        Transaction.objects.create(date=datetime.now(), type='i', value=Decimal('12.34'), job_address='test address')
        data = get_report_data()
        self.assertDictEqual(data, {
            "gross-revenue": Decimal('12.34'),
            "expenses": 0,
            "net-revenue": Decimal('12.34'),
        })

    @tag('unit')
    def test_add_expense(self):
        """
        test if database has only one record type expense
        :return: None
        """
        Transaction.objects.create(date=datetime.now(), type='e', value=Decimal('12.34'),
                                   expense_category='test category')
        data = get_report_data()
        self.assertDictEqual(data, {
            "gross-revenue": 0,
            "expenses": Decimal('12.34'),
            "net-revenue": Decimal('-12.34'),
        })

    @tag('unit')
    def test_add_expenses_and_incomes(self):
        """
        test if database has many records
        :return: None
        """
        transactions = [
            Transaction(date=datetime.now(), type='e', value=Decimal('12.34'),
                        expense_category='test category'),
            Transaction(date=datetime.now(), type='e', value=Decimal('23.45'),
                        expense_category='test category'),
            Transaction(date=datetime.now(), type='i', value=Decimal('34.56'),
                        job_address='test address'),
            Transaction(date=datetime.now(), type='i', value=Decimal('45.67'),
                        job_address='test address')
        ]
        Transaction.objects.bulk_create(transactions)
        data = get_report_data()
        self.assertDictEqual(data, {'gross-revenue': Decimal('80.23'),
                                    'expenses': Decimal('35.79'),
                                    'net-revenue': Decimal('44.44')})
