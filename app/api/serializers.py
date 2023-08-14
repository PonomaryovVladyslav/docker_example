"""File to develop serializers"""
from rest_framework import serializers

from app.api.exceptions import InvalidInput
from app.api.utils import validate_and_prepare_transaction_row
from app.models import Transaction


class TransactionFileSerializer(serializers.Serializer):
    """Class serializer for file with transactions.
    Methods create and update not implemented because I'm not going to use it"""

    data = serializers.FileField()

    def __init__(self, *args, **kwargs):
        """
        initial method
        :param args: standard options for unnamed parameters
        :param kwargs: standard options for named parameters
        """
        super().__init__(*args, **kwargs)
        self.transactions = []

    def create_transactions(self):
        """
        method to remove old transactions and create list of new
        :return: count of new created objects
        """
        if self.transactions:
            Transaction.objects.all().delete()
            transactions_list = Transaction.objects.bulk_create(self.transactions)
            return len(transactions_list)
        return 0

    def validate(self, attrs):
        """
        method which validate data in serializer
        :param attrs: all input data, in our case only file by name 'data'
        :return: attrs: dict with input data
        because we're validating file content and don't need to change it
        """
        data = attrs.get('data')
        for row in data:
            try:
                result = validate_and_prepare_transaction_row(row)
            except InvalidInput:
                continue
            self.transactions.append(Transaction(**result))
        return attrs
