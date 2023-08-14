"""File to develop 'Views' which is controller in Django terms."""
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.serializers import TransactionFileSerializer
from app.api.utils import get_report_data


class TransactionView(APIView):
    """Class controller for /transactions endpoint."""

    def post(self, request):
        """
        method to process post request
        :param request: request object
        :return: Response with count of new objects and 200 status code or
        Response with errors list and 400+ status code
        """
        serializer = TransactionFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        count = serializer.create_transactions()
        return Response(data={"count": count})


class ReportView(APIView):
    """Class controller for /report endpoint."""

    def get(self, request):
        """
        method to process get request
        :param request: request object
        :return: Response with json which contain gross, net and expenses and 200 status code
        """
        data = get_report_data()
        return Response(data=data)
