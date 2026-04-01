from django.test import TestCase
from django.urls import reverse


class NavigationRouteTests(TestCase):
    def test_named_routes_load(self):
        route_names = [
            'dashboard', 'incidents', 'cases', 'dispatch', 'field_ops', 'intelligence',
            'watchlist', 'network_graph', 'predictive_ai', 'ai_assistant', 'financial_crimes',
            'crypto_tracing', 'biometrics', 'evidence_vault', 'device_forensics',
            'cloud_forensics', 'iot_forensics', 'drone_feed', 'mobile_devices',
            'ussd_reports', 'compliance', 'warrants', 'audit_logs', 'system_health',
            'settings', 'static-health'
        ]
        for route_name in route_names:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)

    def test_primary_pages_do_not_render_dead_hash_links(self):
        for route_name in ['dashboard', 'cases', 'ai_assistant', 'watchlist', 'crypto_tracing', 'drone_feed']:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertNotContains(response, 'href="#"', html=False)

    def test_tool_action_missing_returns_graceful_error(self):
        response = self.client.post(reverse('tool_action', args=['watchlist', 'missing-action']))
        self.assertEqual(response.status_code, 404)
        self.assertIn('Tool temporarily unavailable', response.json()['message'])
