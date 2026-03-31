from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.compliance.models import Warrant
from apps.core.models import Agency, Case, UserProfile

User = get_user_model()


class V2WarrantScopeBlockTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.agency = Agency.objects.create(name='Joint Operations Command', code='JOC')
        self.user = User.objects.create_user(username='v2_operator', password='x')
        UserProfile.objects.create(user=self.user, agency=self.agency, role='INVESTIGATOR', clearance_level=5)

        self.case = Case.objects.create(
            case_number='V2-CASE-001',
            title='V2 Scope Compliance Case',
            summary='Validate scope gates across V2 modules',
            lead_agency=self.agency,
            created_by=self.user,
            required_clearance=3,
        )
        self.case.assigned_users.add(self.user)

        self.warrant = Warrant.objects.create(
            case=self.case,
            warrant_number='V2-W-001',
            issuing_court='High Court',
            issued_at=timezone.now() - timezone.timedelta(hours=3),
            expires_at=timezone.now() + timezone.timedelta(days=2),
            status=Warrant.WarrantStatus.ACTIVE,
            document_path='/tmp/v2_warrant.pdf',
            authorized_scope={'operation': ['summary_only']},
            proportionality_notes='Limited to summary and records triage.',
            created_by=self.user,
        )

        self.client.force_authenticate(self.user)

    def _assert_scope_block(self, url: str, payload: dict):
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('exceeds warrant scope', str(response.data).lower())

    def test_ai_intelligence_pattern_of_life_scope_blocked(self):
        payload = {
            'case': self.case.id,
            'warrant': self.warrant.id,
            'subject_ref': 'subject-a',
            'baseline_window_days': 30,
            'baseline_features': {'comm_freq': [4, 7, 6]},
            'deviation_score': 0.0,
            'anomaly_explanation': '',
            'timeline_graph': [],
            'requested_scope': {'operation': 'pattern_of_life'},
            'created_by': self.user.id,
        }
        self._assert_scope_block('/api/ai-intelligence/pattern-of-life/', payload)

    def test_operations_ar_overlay_scope_blocked(self):
        payload = {
            'case': self.case.id,
            'warrant': self.warrant.id,
            'overlay_type': 'suspect_profile',
            'target_ref': 'suspect-42',
            'payload': {'name': 'Target'},
            'requested_scope': {'operation': 'ar_overlay_push'},
            'expires_at': (timezone.now() + timezone.timedelta(hours=2)).isoformat(),
            'created_by': self.user.id,
        }
        self._assert_scope_block('/api/operations/ar-overlays/', payload)

    def test_federation_query_scope_blocked(self):
        payload = {
            'case': self.case.id,
            'warrant': self.warrant.id,
            'query_text': 'Cross-border financing entities',
            'partner_systems': ['Interpol'],
            'selective_visibility': {'fields': ['entity_ref', 'score']},
            'requested_scope': {'operation': 'federated_search'},
            'requested_by': self.user.id,
        }
        self._assert_scope_block('/api/federation/queries/', payload)

    def test_biometrics_fusion_query_scope_blocked(self):
        payload = {
            'case': self.case.id,
            'warrant': self.warrant.id,
            'subject_ref': 'person-884',
            'face_embedding_ref': 'face-emb-1',
            'gait_signature_ref': 'gait-1',
            'voiceprint_ref': 'voice-1',
            'fingerprint_ref': 'fp-1',
            'confidence': 0.0,
            'decision_support_notes': 'triage',
            'requested_scope': {'operation': 'biometric_fusion'},
            'queried_by': self.user.id,
        }
        self._assert_scope_block('/api/biometrics/fusion-queries/', payload)

    def test_evidence_automation_report_scope_blocked(self):
        payload = {
            'case': self.case.id,
            'warrant': self.warrant.id,
            'generated_by': self.user.id,
            'methodology': 'Automated forensic workflow summary',
            'timeline': [],
            'link_analysis_graph': {},
            'pdf_export_path': '/tmp/report.pdf',
            'signed_package_path': '/tmp/report.sig',
            'requested_scope': {'operation': 'automated_report_generation'},
        }
        self._assert_scope_block('/api/evidence-automation/automated-reports/', payload)
