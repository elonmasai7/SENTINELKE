from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.audit.models import AuditLog
from apps.compliance.models import Warrant
from apps.core.models import Agency, Case, UserProfile

User = get_user_model()


class AuditTrailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.agency = Agency.objects.create(name='Service DCI', code='DCI')
        self.user = User.objects.create_user(username='auditor_user', password='x')
        UserProfile.objects.create(user=self.user, agency=self.agency, role='LEGAL', clearance_level=4)

        self.case = Case.objects.create(
            case_number='AUD-1',
            title='Audit Case',
            summary='Audit validation',
            lead_agency=self.agency,
            created_by=self.user,
            required_clearance=2,
        )
        self.case.assigned_users.add(self.user)
        self.client.force_authenticate(self.user)

    def test_warrant_create_generates_signed_audit_log(self):
        payload = {
            'case': self.case.id,
            'warrant_number': 'AUD-W-1',
            'issuing_court': 'Milimani Law Courts',
            'issued_at': (timezone.now() - timezone.timedelta(hours=1)).isoformat(),
            'expires_at': (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            'status': Warrant.WarrantStatus.ACTIVE,
            'document_path': '/tmp/aud1.pdf',
            'created_by': self.user.id,
        }
        response = self.client.post('/api/compliance/warrants/', payload, format='json')
        self.assertEqual(response.status_code, 201)

        log = AuditLog.objects.filter(object_type='Warrant').order_by('-created_at').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.action, 'create')
        self.assertEqual(len(log.event_hash), 64)
        self.assertGreater(len(log.signature), 32)
