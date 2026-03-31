from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.core.models import Agency, Case, UserProfile
from apps.fraud.models import FinancialTransaction

User = get_user_model()


class RBACAndClearanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.agency_a = Agency.objects.create(name='Agency A', code='A')
        self.agency_b = Agency.objects.create(name='Agency B', code='B')

        self.user_a = User.objects.create_user(username='user_a', password='x')
        self.user_b = User.objects.create_user(username='user_b', password='x')
        self.low_clearance = User.objects.create_user(username='low_clear', password='x')

        UserProfile.objects.create(user=self.user_a, agency=self.agency_a, role='ANALYST', clearance_level=4)
        UserProfile.objects.create(user=self.user_b, agency=self.agency_b, role='ANALYST', clearance_level=4)
        UserProfile.objects.create(user=self.low_clearance, agency=self.agency_a, role='ANALYST', clearance_level=1)

        self.case_a = Case.objects.create(
            case_number='CASE-A',
            title='Case A',
            summary='Agency A case',
            lead_agency=self.agency_a,
            created_by=self.user_a,
            required_clearance=2,
        )
        self.case_a.assigned_users.add(self.user_a)

        self.case_b = Case.objects.create(
            case_number='CASE-B',
            title='Case B',
            summary='Agency B case',
            lead_agency=self.agency_b,
            created_by=self.user_b,
            required_clearance=2,
        )
        self.case_b.assigned_users.add(self.user_b)

        self.high_case = Case.objects.create(
            case_number='CASE-HIGH',
            title='Top secrecy',
            summary='High clearance case',
            lead_agency=self.agency_a,
            created_by=self.user_a,
            required_clearance=5,
        )
        self.high_case.assigned_users.add(self.user_a)

        self.tx_b = FinancialTransaction.objects.create(
            case=self.case_b,
            external_ref='TX-B-1',
            source_system='bank',
            amount='1000.00',
            currency='KES',
            sender='X',
            receiver='Y',
            occurred_at=timezone.now(),
        )

    def test_case_list_scoped_to_agency(self):
        self.client.force_authenticate(self.user_a)
        response = self.client.get('/api/core/cases/')
        self.assertEqual(response.status_code, 200)
        case_numbers = {item['case_number'] for item in response.data}
        self.assertIn('CASE-A', case_numbers)
        self.assertNotIn('CASE-B', case_numbers)

    def test_case_hidden_when_clearance_insufficient(self):
        self.high_case.assigned_users.add(self.low_clearance)
        self.client.force_authenticate(self.low_clearance)
        response = self.client.get('/api/core/cases/')
        self.assertEqual(response.status_code, 200)
        case_numbers = {item['case_number'] for item in response.data}
        self.assertNotIn('CASE-HIGH', case_numbers)

    def test_cross_agency_transaction_detail_denied(self):
        self.client.force_authenticate(self.user_a)
        response = self.client.get(f'/api/fraud/transactions/{self.tx_b.id}/')
        self.assertEqual(response.status_code, 404)
