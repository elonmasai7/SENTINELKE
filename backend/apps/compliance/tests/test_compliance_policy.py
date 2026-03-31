from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.compliance.models import Warrant
from apps.core.models import Agency, Case, UserProfile
from apps.surveillance.models import SurveillanceRequest

User = get_user_model()


class SurveillanceComplianceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.agency = Agency.objects.create(name='National Police Service', code='NPS')
        self.user = User.objects.create_user(username='investigator', password='x')
        UserProfile.objects.create(user=self.user, agency=self.agency, role='INVESTIGATOR', clearance_level=4)

        self.case = Case.objects.create(
            case_number='CASE-001',
            title='Counter-terrorism lead',
            summary='Sensitive case',
            lead_agency=self.agency,
            created_by=self.user,
            required_clearance=3,
        )
        self.case.assigned_users.add(self.user)
        self.client.force_authenticate(self.user)

    def test_surveillance_create_blocked_without_active_warrant(self):
        warrant = Warrant.objects.create(
            case=self.case,
            warrant_number='W-100',
            issuing_court='High Court',
            issued_at=timezone.now() - timezone.timedelta(days=5),
            expires_at=timezone.now() - timezone.timedelta(days=1),
            status=Warrant.WarrantStatus.EXPIRED,
            document_path='/tmp/w100.pdf',
            created_by=self.user,
        )

        payload = {
            'case': self.case.id,
            'warrant': warrant.id,
            'target_identifier': '+254700000001',
            'provider': 'LawfulTel',
            'request_metadata': {'channel': 'metadata-only'},
            'status': 'DRAFT',
            'created_by': self.user.id,
        }
        response = self.client.post('/api/surveillance/requests/', payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('active warrant required', str(response.data).lower())
        self.assertEqual(SurveillanceRequest.objects.count(), 0)

    def test_surveillance_create_allowed_with_active_warrant(self):
        warrant = Warrant.objects.create(
            case=self.case,
            warrant_number='W-200',
            issuing_court='High Court',
            issued_at=timezone.now() - timezone.timedelta(hours=1),
            expires_at=timezone.now() + timezone.timedelta(days=1),
            status=Warrant.WarrantStatus.ACTIVE,
            document_path='/tmp/w200.pdf',
            created_by=self.user,
        )

        payload = {
            'case': self.case.id,
            'warrant': warrant.id,
            'target_identifier': '+254700000002',
            'provider': 'LawfulTel',
            'request_metadata': {'channel': 'metadata-only'},
            'status': 'DRAFT',
            'created_by': self.user.id,
        }
        response = self.client.post('/api/surveillance/requests/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SurveillanceRequest.objects.count(), 1)
