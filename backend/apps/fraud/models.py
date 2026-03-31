from django.db import models
from apps.core.models import Case


class FinancialTransaction(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='financial_transactions', null=True, blank=True)
    external_ref = models.CharField(max_length=120, unique=True)
    source_system = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=12)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    occurred_at = models.DateTimeField()


class FraudAlert(models.Model):
    transaction = models.ForeignKey(FinancialTransaction, on_delete=models.CASCADE, related_name='alerts')
    risk_score = models.FloatField(default=0.0)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
