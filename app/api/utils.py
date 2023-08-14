"""File with utilities, in this case only one function"""
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.db.models import Sum, Q

from app.api.exceptions import InvalidInput
from app.models import Transaction


def validate_and_prepare_transaction_row(row):
    """
    method to validate row from file and transform to dict which will be fit to database
    :param row: row from input file
    :return: dict prepared to be put in database
    """
    if not isinstance(row, bytes):
        raise InvalidInput
    try:
        date, transaction_type, value, additional_info = row.decode().strip().split(',')
    except ValueError as error:
        raise InvalidInput from error
    result = {}
    try:
        result['date'] = datetime.strptime(date.strip(), '%Y-%m-%d')
    except ValueError as error:
        raise InvalidInput from error
    if transaction_type.strip() == 'Expense':
        result['type'] = 'e'
        result['expense_category'] = additional_info.strip()
    elif transaction_type.strip() == 'Income':
        result['type'] = 'i'
        result['job_address'] = additional_info.strip()
    else:
        raise InvalidInput
    try:
        result['value'] = Decimal(str(value).strip()).quantize(Decimal('.01'))
    except InvalidOperation as error:
        raise InvalidInput from error
    return result


def get_report_data():
    """
    function to get values from database
    :return: dict with
    gross-revenue - sum of all incomes
    expenses - sum of all expenses
    net-revenue - gross-revenue minus expenses
    """
    expense_sum_filter = Sum('value', filter=Q(type='e'))
    income_sum_filter = Sum('value', filter=Q(type='i'))
    aggregation = Transaction.objects.aggregate(expenses=expense_sum_filter,
                                                incomes=income_sum_filter)
    incomes = aggregation.get('incomes') if aggregation.get('incomes') else Decimal(0)
    expenses = aggregation.get('expenses') if aggregation.get('expenses') else Decimal(0)
    net = incomes - expenses
    data = {
        "gross-revenue": incomes.quantize(Decimal('.01')),
        "expenses": expenses.quantize(Decimal('.01')),
        "net-revenue": net.quantize(Decimal('.01')),
    }
    return data
