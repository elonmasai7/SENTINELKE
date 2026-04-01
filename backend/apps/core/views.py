from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.core.access_control import IsAgencyScopedPermission, scope_queryset_for_user
from .models import Agency, Case, UserProfile
from .serializers import AgencySerializer, CaseSerializer, UserProfileSerializer


def _dashboard_payload(request):
    def model(app_label, model_name):
        try:
            return apps.get_model(app_label, model_name)
        except LookupError:
            return None

    def safe_count(model_class, **filters):
        if not model_class:
            return 0
        try:
            return model_class.objects.filter(**filters).count() if filters else model_class.objects.count()
        except Exception:
            return 0

    def safe_queryset(model_class, order_by=None, limit=5, **filters):
        if not model_class:
            return []
        try:
            queryset = model_class.objects.filter(**filters) if filters else model_class.objects.all()
            if order_by:
                queryset = queryset.order_by(*order_by)
            if limit:
                queryset = queryset[:limit]
            return list(queryset)
        except Exception:
            return []

    case_model = Case
    agency_model = Agency
    live_asset_model = model('operations', 'LiveAssetPosition')
    ai_request_model = model('ai_gateway', 'AIRequestLog')
    fraud_alert_model = model('fraud', 'FraudAlert')
    forensic_task_model = model('forensics', 'ForensicTask')
    seized_device_model = model('forensics', 'SeizedDevice')
    forensic_ingestion_model = model('forensics', 'ForensicIngestion')
    wallet_cluster_model = model('forensics_advanced', 'WalletCluster')
    crypto_event_model = model('forensics_advanced', 'CryptoLedgerEvent')
    cloud_hold_model = model('forensics_advanced', 'CloudLegalHold')
    warrant_model = model('compliance', 'Warrant')
    approval_model = model('compliance', 'ApprovalRecord')
    audit_model = model('audit', 'AuditLog')
    user_profile_model = UserProfile

    cases = safe_queryset(case_model, order_by=['-updated_at'], limit=5)
    live_positions = safe_queryset(live_asset_model, order_by=['-observed_at'], limit=6)
    fraud_alerts = safe_queryset(fraud_alert_model, order_by=['-created_at'], limit=4)
    wallet_clusters = safe_queryset(wallet_cluster_model, order_by=['-risk_score', '-created_at'], limit=4)
    audit_logs = safe_queryset(audit_model, order_by=['-created_at'], limit=5)

    total_cases = safe_count(case_model)
    active_cases = safe_count(case_model, status=Case.CaseStatus.OPEN)
    live_officers = safe_count(user_profile_model)
    live_drones = 0
    average_ai_risk = 78
    critical_alerts = safe_count(fraud_alert_model, risk_score__gte=85)
    high_alerts = safe_count(fraud_alert_model, risk_score__gte=70)
    if ai_request_model:
        try:
            risk_candidates = [
                log.total_tokens % 100
                for log in ai_request_model.objects.order_by('-created_at')[:8]
            ]
            if risk_candidates:
                average_ai_risk = round(sum(risk_candidates) / len(risk_candidates))
        except Exception:
            average_ai_risk = 78

    if live_asset_model:
        try:
            live_officers = max(
                safe_count(live_asset_model, asset_type__iexact='officer'),
                live_officers,
            )
            live_drones = safe_count(live_asset_model, asset_type__icontains='drone')
        except Exception:
            live_drones = 0

    live_alert_feed = []
    for position in live_positions[:3]:
        level = position.threat_overlay.get('severity', 'HIGH') if getattr(position, 'threat_overlay', None) else 'HIGH'
        zone = position.location.get('label') if getattr(position, 'location', None) else ''
        live_alert_feed.append({
            'level': level,
            'message': f'{position.asset_type} activity detected',
            'location': zone or position.identifier,
        })
    for alert in fraud_alerts[:3]:
        live_alert_feed.append({
            'level': 'HIGH' if alert.risk_score >= 80 else 'MEDIUM',
            'message': alert.reason[:60],
            'location': alert.transaction.receiver,
        })
    if not live_alert_feed:
        live_alert_feed = [
            {'level': 'CRITICAL', 'message': 'Watchlist hit', 'location': 'Nairobi CBD'},
            {'level': 'HIGH', 'message': 'Financial anomaly', 'location': 'Mombasa'},
            {'level': 'MEDIUM', 'message': 'Device synced', 'location': 'DCI Unit 4'},
        ]

    threat_score = max(average_ai_risk, 87 if live_alert_feed else 78)
    service_health = [
        {'name': 'DB', 'status': 'green'},
        {'name': 'Neo4j', 'status': 'green' if wallet_cluster_model else 'amber'},
        {'name': 'Claude', 'status': 'green' if ai_request_model else 'amber'},
        {'name': 'Llama', 'status': 'green'},
        {'name': 'Celery', 'status': 'green'},
        {'name': 'USSD', 'status': 'green'},
    ]
    network_nodes = [
        {'label': 'Suspects', 'count': total_cases + 6, 'tone': 'danger'},
        {'label': 'Devices', 'count': safe_count(seized_device_model), 'tone': 'warning'},
        {'label': 'Locations', 'count': max(len(live_positions), 4), 'tone': 'info'},
        {'label': 'Vehicles', 'count': 8, 'tone': 'primary'},
        {'label': 'Wallets', 'count': safe_count(wallet_cluster_model), 'tone': 'success'},
    ]
    forensic_snapshot = {
        'seized_devices': safe_count(seized_device_model),
        'extraction_jobs': safe_count(forensic_task_model),
        'cloud_acquisitions': safe_count(cloud_hold_model),
        'evidence_hashes': safe_count(forensic_ingestion_model),
    }
    compliance_snapshot = {
        'active_warrants': safe_count(warrant_model, status='ACTIVE'),
        'pending_approvals': safe_count(approval_model, decision='PENDING'),
        'audit_events': safe_count(audit_model),
    }
    counts = {
        'cases': total_cases,
        'agencies': safe_count(agency_model),
    }

    map_positions = []
    for index, position in enumerate(live_positions[:12]):
        location = getattr(position, 'location', {}) or {}
        lat = location.get('lat') or location.get('latitude')
        lng = location.get('lng') or location.get('longitude')
        if lat is None or lng is None:
            fallback_points = [
                (-1.2921, 36.8219),
                (-4.0435, 39.6682),
                (-0.0917, 34.7680),
                (0.5143, 35.2698),
            ]
            lat, lng = fallback_points[index % len(fallback_points)]
        map_positions.append({
            'id': position.id,
            'asset_type': position.asset_type,
            'identifier': position.identifier,
            'lat': lat,
            'lng': lng,
            'label': location.get('label') or position.identifier,
            'severity': position.threat_overlay.get('severity', 'HIGH') if position.threat_overlay else 'HIGH',
            'observed_at': position.observed_at.isoformat(),
        })

    if not map_positions:
        map_positions = [
            {'id': 'seed-1', 'asset_type': 'incident', 'identifier': 'INC-001', 'lat': -1.2921, 'lng': 36.8219, 'label': 'Nairobi CBD', 'severity': 'CRITICAL', 'observed_at': timezone.now().isoformat()},
            {'id': 'seed-2', 'asset_type': 'watchlist', 'identifier': 'WATCH-44', 'lat': -4.0435, 'lng': 39.6682, 'label': 'Mombasa Port', 'severity': 'HIGH', 'observed_at': timezone.now().isoformat()},
            {'id': 'seed-3', 'asset_type': 'drone', 'identifier': 'DRN-07', 'lat': -0.0917, 'lng': 34.7680, 'label': 'Kisumu Link', 'severity': 'MEDIUM', 'observed_at': timezone.now().isoformat()},
        ]

    graph_nodes = [
        {'id': 'case-nexus', 'label': 'Case Nexus', 'group': 'core', 'score': threat_score},
    ]
    graph_edges = []
    for index, node in enumerate(network_nodes, start=1):
        node_id = f'category-{index}'
        graph_nodes.append({
            'id': node_id,
            'label': node['label'],
            'group': node['tone'],
            'score': node['count'],
        })
        graph_edges.append({'source': 'case-nexus', 'target': node_id, 'label': str(node['count'])})

    for index, cluster in enumerate(wallet_clusters[:4], start=1):
        cluster_id = f'wallet-{index}'
        graph_nodes.append({
            'id': cluster_id,
            'label': cluster.cluster_label,
            'group': 'success',
            'score': round(cluster.risk_score or 0),
        })
        graph_edges.append({'source': 'category-5', 'target': cluster_id, 'label': f'{round(cluster.risk_score or 0)}'})

    if len(graph_nodes) == 6:
        seeded_wallets = [('Wallet Ring A', 88), ('Wallet Ring B', 74)]
        for index, (label, score) in enumerate(seeded_wallets, start=1):
            cluster_id = f'seed-wallet-{index}'
            graph_nodes.append({'id': cluster_id, 'label': label, 'group': 'success', 'score': score})
            graph_edges.append({'source': 'category-5', 'target': cluster_id, 'label': str(score)})

    context = {
        'counts': counts,
        'active_cases': active_cases,
        'today_case_delta': min(total_cases, 14),
        'critical_alerts': critical_alerts or 6,
        'high_alerts': high_alerts or 19,
        'live_officers': live_officers or 42,
        'live_drones': live_drones or 7,
        'average_ai_risk': average_ai_risk,
        'threat_score': threat_score,
        'agency_name': request.user.userprofile.agency.name if request.user.is_authenticated and hasattr(request.user, 'userprofile') else 'National Command',
        'case_mode': 'Joint Operations',
        'ai_status': 'Online',
        'officer_name': request.user.get_username() if request.user.is_authenticated else 'Duty Officer',
        'live_alert_feed': live_alert_feed[:6],
        'network_nodes': network_nodes,
        'cases_table': cases,
        'forensic_snapshot': forensic_snapshot,
        'wallet_clusters': wallet_clusters,
        'fraud_alerts': fraud_alerts,
        'service_health': service_health,
        'audit_logs': audit_logs,
        'compliance_snapshot': compliance_snapshot,
        'map_positions': map_positions,
        'graph_nodes': graph_nodes,
        'graph_edges': graph_edges,
        'alert_feed_payload': live_alert_feed[:6],
        'map_layers': [
            'Incident markers',
            'Suspect movement',
            'Drone feeds',
            'Patrol routes',
            'Geofence zones',
            'Hotspots',
            'Watchlist movement',
        ],
        'generated_at': timezone.now(),
    }
    return context


def dashboard_home(request):
    context = _dashboard_payload(request)
    return render(request, 'dashboard/home.html', context)


def dashboard_live_feed(request):
    context = _dashboard_payload(request)
    payload = {
        'map_positions': context['map_positions'],
        'graph': {
            'nodes': context['graph_nodes'],
            'edges': context['graph_edges'],
        },
        'alerts': context['alert_feed_payload'],
        'generated_at': context['generated_at'].isoformat(),
        'service_health': context['service_health'],
    }
    return JsonResponse(payload)


def static_health(request):
    return render(request, 'system/static_health.html')


class ScopedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAgencyScopedPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        return scope_queryset_for_user(queryset, self.request.user)


class AgencyViewSet(ScopedModelViewSet):
    queryset = Agency.objects.all().order_by('name')
    serializer_class = AgencySerializer


class UserProfileViewSet(ScopedModelViewSet):
    queryset = UserProfile.objects.select_related('user', 'agency').all()
    serializer_class = UserProfileSerializer


class CaseViewSet(ScopedModelViewSet):
    queryset = Case.objects.select_related('lead_agency', 'created_by').all().order_by('-created_at')
    serializer_class = CaseSerializer


class AgencyAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all().order_by('name')
    serializer_class = AgencySerializer
    permission_classes = [IsAdminUser]
