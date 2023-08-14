"""File with my api urls"""
from django.urls import path

from app.api.resources import TransactionView, ReportView

urlpatterns = [
    path('transactions', TransactionView.as_view()),
    path('report', ReportView.as_view()),
]
