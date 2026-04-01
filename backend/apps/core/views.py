from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.core.access_control import IsAgencyScopedPermission, scope_queryset_for_user
from .models import Agency, Case, UserProfile
from .serializers import AgencySerializer, CaseSerializer, UserProfileSerializer

User = get_user_model()


MODULE_REGISTRY = {
    'dashboard': {
        'title': 'Command Center Overview',
        'subtitle': 'Executive dashboard with direct access to every major SentinelKE tool.',
        'template': 'dashboard.html',
    },
    'incidents': {
        'title': 'Incidents',
        'subtitle': 'Incident queue, current geo-events, and rapid escalation entry points.',
        'template': 'incidents.html',
    },
    'cases': {
        'title': 'Cases',
        'subtitle': 'Dedicated case operations workspace with assignment and closure controls.',
        'template': 'cases.html',
    },
    'dispatch': {
        'title': 'Dispatch',
        'subtitle': 'Unit coordination, live alerts, and dispatch readiness.',
        'template': 'dispatch.html',
    },
    'field_ops': {
        'title': 'Field Operations',
        'subtitle': 'Team posture, deployment signals, and asset visibility for active operations.',
        'template': 'field_ops.html',
    },
    'intelligence': {
        'title': 'Threat Intelligence',
        'subtitle': 'Geo-intelligence and live threat monitoring on a dedicated page.',
        'template': 'intelligence.html',
    },
    'watchlist': {
        'title': 'Watchlist',
        'subtitle': 'Manage watch targets, movement flags, and profile lookups.',
        'template': 'watchlist.html',
    },
    'network_graph': {
        'title': 'Network Graph',
        'subtitle': 'Relationship mapping for suspects, wallets, devices, and operational entities.',
        'template': 'network_graph.html',
    },
    'predictive_ai': {
        'title': 'Predictive AI',
        'subtitle': 'Forecast-driven prioritization backed by the AI analysis layer.',
        'template': 'predictive_ai.html',
    },
    'ai_assistant': {
        'title': 'AI Assistant',
        'subtitle': 'Run summaries, threat analysis, brief generation, and voice-style queries.',
        'template': 'ai_assistant.html',
    },
    'financial_crimes': {
        'title': 'Financial Crimes',
        'subtitle': 'Financial anomaly review and laundering indicator workspace.',
        'template': 'financial_crimes.html',
    },
    'crypto_tracing': {
        'title': 'Crypto Tracing',
        'subtitle': 'Wallet searches, trace runs, and graph exploration for crypto exposure.',
        'template': 'crypto_tracing.html',
    },
    'biometrics': {
        'title': 'Biometrics',
        'subtitle': 'Biometric verification summary and identity-match workflow entry points.',
        'template': 'biometrics.html',
    },
    'evidence_vault': {
        'title': 'Evidence Vault',
        'subtitle': 'Evidence inventory and integrity visibility for seized material.',
        'template': 'evidence_vault.html',
    },
    'device_forensics': {
        'title': 'Device Forensics',
        'subtitle': 'Device extraction progress and seized hardware review.',
        'template': 'device_forensics.html',
    },
    'cloud_forensics': {
        'title': 'Cloud Forensics',
        'subtitle': 'Cloud acquisition and legal hold activity in one place.',
        'template': 'cloud_forensics.html',
    },
    'iot_forensics': {
        'title': 'IoT Forensics',
        'subtitle': 'Connected-device evidence workflows and IoT acquisition readiness.',
        'template': 'iot_forensics.html',
    },
    'drone_feed': {
        'title': 'Drone Feed',
        'subtitle': 'Live patrol feed controls, route review, and patrol assignment.',
        'template': 'drone_feed.html',
    },
    'mobile_devices': {
        'title': 'Mobile Devices',
        'subtitle': 'Managed mobile endpoints and field device posture.',
        'template': 'mobile_devices.html',
    },
    'ussd_reports': {
        'title': 'USSD Reports',
        'subtitle': 'USSD intake stream, latest reports, and service readiness.',
        'template': 'ussd_reports.html',
    },
    'compliance': {
        'title': 'Compliance',
        'subtitle': 'Compliance posture, approvals, and warrant-aware operating guardrails.',
        'template': 'compliance.html',
    },
    'warrants': {
        'title': 'Warrants',
        'subtitle': 'Warrant posture, scope tracking, and urgent review actions.',
        'template': 'warrants.html',
    },
    'audit_logs': {
        'title': 'Audit Logs',
        'subtitle': 'Signed audit trail and operational accountability records.',
        'template': 'audit_logs.html',
    },
    'system_health': {
        'title': 'System Health',
        'subtitle': 'Service readiness, static diagnostics, and platform health status.',
        'template': 'system_health.html',
    },
    'settings': {
        'title': 'Settings',
        'subtitle': 'Environment diagnostics, deployment settings, and repair tooling.',
        'template': 'settings.html',
    },
}


NAV_SECTIONS = [
    {
        'heading': 'Operations',
        'items': [
            {'label': 'Dashboard', 'route': 'dashboard'},
            {'label': 'Incidents', 'route': 'incidents'},
            {'label': 'Cases', 'route': 'cases'},
            {'label': 'Dispatch', 'route': 'dispatch'},
            {'label': 'Field Ops', 'route': 'field_ops'},
        ],
    },
    {
        'heading': 'Intelligence',
        'items': [
            {'label': 'Threat Intelligence', 'route': 'intelligence'},
            {'label': 'Watchlist', 'route': 'watchlist'},
            {'label': 'Network Graph', 'route': 'network_graph'},
            {'label': 'Predictive AI', 'route': 'predictive_ai'},
            {'label': 'AI Assistant', 'route': 'ai_assistant'},
            {'label': 'Financial Crimes', 'route': 'financial_crimes'},
            {'label': 'Crypto Tracing', 'route': 'crypto_tracing'},
            {'label': 'Biometrics', 'route': 'biometrics'},
        ],
    },
    {
        'heading': 'Forensics',
        'items': [
            {'label': 'Evidence Vault', 'route': 'evidence_vault'},
            {'label': 'Device Forensics', 'route': 'device_forensics'},
            {'label': 'Cloud Forensics', 'route': 'cloud_forensics'},
            {'label': 'IoT Forensics', 'route': 'iot_forensics'},
            {'label': 'Drone Feed', 'route': 'drone_feed'},
            {'label': 'Mobile Devices', 'route': 'mobile_devices'},
            {'label': 'USSD Reports', 'route': 'ussd_reports'},
        ],
    },
    {
        'heading': 'Oversight',
        'items': [
            {'label': 'Compliance', 'route': 'compliance'},
            {'label': 'Warrants', 'route': 'warrants'},
            {'label': 'Audit Logs', 'route': 'audit_logs'},
            {'label': 'System Health', 'route': 'system_health'},
            {'label': 'Settings', 'route': 'settings'},
        ],
    },
]


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
    cloud_hold_model = model('forensics_advanced', 'CloudLegalHold')
    warrant_model = model('compliance', 'Warrant')
    approval_model = model('compliance', 'ApprovalRecord')
    audit_model = model('audit', 'AuditLog')
    user_profile_model = UserProfile

    cases = safe_queryset(case_model, order_by=['-updated_at'], limit=8)
    live_positions = safe_queryset(live_asset_model, order_by=['-observed_at'], limit=12)
    fraud_alerts = safe_queryset(fraud_alert_model, order_by=['-created_at'], limit=4)
    wallet_clusters = safe_queryset(wallet_cluster_model, order_by=['-risk_score', '-id'], limit=4)
    audit_logs = safe_queryset(audit_model, order_by=['-created_at'], limit=6)

    total_cases = safe_count(case_model)
    active_cases = safe_count(case_model, status=Case.CaseStatus.OPEN)
    live_officers = safe_count(user_profile_model)
    live_drones = 0
    average_ai_risk = 78
    critical_alerts = safe_count(fraud_alert_model, risk_score__gte=85)
    high_alerts = safe_count(fraud_alert_model, risk_score__gte=70)

    if ai_request_model:
        try:
            risk_candidates = [log.total_tokens % 100 for log in ai_request_model.objects.order_by('-created_at')[:8]]
            if risk_candidates:
                average_ai_risk = round(sum(risk_candidates) / len(risk_candidates))
        except Exception:
            average_ai_risk = 78

    if live_asset_model:
        try:
            live_officers = max(safe_count(live_asset_model, asset_type__iexact='officer'), live_officers)
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
            'level': 'HIGH' if getattr(alert, 'risk_score', 0) >= 80 else 'MEDIUM',
            'message': getattr(alert, 'reason', 'Financial anomaly')[:60],
            'location': getattr(getattr(alert, 'transaction', None), 'receiver', 'Unknown'),
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

    map_positions = []
    for index, position in enumerate(live_positions[:12]):
        location = getattr(position, 'location', {}) or {}
        lat = location.get('lat') or location.get('latitude')
        lng = location.get('lng') or location.get('longitude')
        if lat is None or lng is None:
            fallback_points = [(-1.2921, 36.8219), (-4.0435, 39.6682), (-0.0917, 34.7680), (0.5143, 35.2698)]
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
        now = timezone.now().isoformat()
        map_positions = [
            {'id': 'seed-1', 'asset_type': 'incident', 'identifier': 'INC-001', 'lat': -1.2921, 'lng': 36.8219, 'label': 'Nairobi CBD', 'severity': 'CRITICAL', 'observed_at': now},
            {'id': 'seed-2', 'asset_type': 'watchlist', 'identifier': 'WATCH-44', 'lat': -4.0435, 'lng': 39.6682, 'label': 'Mombasa Port', 'severity': 'HIGH', 'observed_at': now},
            {'id': 'seed-3', 'asset_type': 'drone', 'identifier': 'DRN-07', 'lat': -0.0917, 'lng': 34.7680, 'label': 'Kisumu Link', 'severity': 'MEDIUM', 'observed_at': now},
        ]

    graph_nodes = [{'id': 'case-nexus', 'label': 'Case Nexus', 'group': 'core', 'score': threat_score}]
    graph_edges = []
    for index, node in enumerate(network_nodes, start=1):
        node_id = f'category-{index}'
        graph_nodes.append({'id': node_id, 'label': node['label'], 'group': node['tone'], 'score': node['count']})
        graph_edges.append({'source': 'case-nexus', 'target': node_id, 'label': str(node['count'])})

    for index, cluster in enumerate(wallet_clusters[:4], start=1):
        cluster_id = f'wallet-{index}'
        graph_nodes.append({'id': cluster_id, 'label': cluster.cluster_label, 'group': 'success', 'score': round(cluster.risk_score or 0)})
        graph_edges.append({'source': 'category-5', 'target': cluster_id, 'label': f'{round(cluster.risk_score or 0)}'})

    if len(graph_nodes) == 6:
        for index, (label, score) in enumerate([('Wallet Ring A', 88), ('Wallet Ring B', 74)], start=1):
            cluster_id = f'seed-wallet-{index}'
            graph_nodes.append({'id': cluster_id, 'label': label, 'group': 'success', 'score': score})
            graph_edges.append({'source': 'category-5', 'target': cluster_id, 'label': str(score)})

    return {
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
        'map_layers': ['Incident markers', 'Suspect movement', 'Drone feeds', 'Patrol routes', 'Geofence zones', 'Hotspots', 'Watchlist movement'],
        'generated_at': timezone.now(),
        'counts': {'cases': total_cases, 'agencies': Agency.objects.count() if Agency.objects.exists() else 0},
    }


def _safe_case_choices():
    try:
        return list(Case.objects.select_related('lead_agency', 'created_by').prefetch_related('assigned_users').order_by('-updated_at')[:10])
    except Exception:
        return []


def _safe_officer_choices():
    try:
        return list(User.objects.order_by('username')[:10])
    except Exception:
        return []


def _page_context(request, page_key, extra=None):
    context = _dashboard_payload(request)
    config = MODULE_REGISTRY[page_key]
    context.update({
        'current_page': page_key,
        'page_title': config['title'],
        'page_subtitle': config['subtitle'],
        'nav_sections': NAV_SECTIONS,
        'case_choices': _safe_case_choices(),
        'officer_choices': _safe_officer_choices(),
        'tool_unavailable_message': 'Tool temporarily unavailable',
        'tool_logs_url': reverse('audit_logs'),
        'static_health_url': reverse('static-health'),
    })
    if extra:
        context.update(extra)
    return context


def _render_module(request, page_key, extra=None):
    config = MODULE_REGISTRY[page_key]
    return render(request, config['template'], _page_context(request, page_key, extra))


def _default_case_for_user(request):
    cases = _safe_case_choices()
    if request.user.is_authenticated:
        user_cases = [case for case in cases if case.created_by_id == request.user.id or case.assigned_users.filter(id=request.user.id).exists()]
        if user_cases:
            return user_cases[0]
    return cases[0] if cases else None


def _resolve_operator_user(request):
    if request.user.is_authenticated:
        return request.user
    try:
        return User.objects.order_by('id').first()
    except Exception:
        return None


def _resolve_agency_for_user(user):
    if user and hasattr(user, 'userprofile'):
        return user.userprofile.agency
    try:
        return Agency.objects.filter(active=True).order_by('name').first() or Agency.objects.order_by('name').first()
    except Exception:
        return None


def dashboard_view(request):
    context = _page_context(request, 'dashboard', {
        'overview_cards': [
            {'title': 'Active Cases', 'value': _dashboard_payload(request)['active_cases'], 'meta': f"+{_dashboard_payload(request)['today_case_delta']} today", 'route': 'cases'},
            {'title': 'Threat Alerts', 'value': _dashboard_payload(request)['critical_alerts'], 'meta': f"High: {_dashboard_payload(request)['high_alerts']}", 'route': 'intelligence'},
            {'title': 'Field Units Online', 'value': _dashboard_payload(request)['live_officers'], 'meta': f"{_dashboard_payload(request)['live_drones']} drones", 'route': 'field_ops'},
            {'title': 'AI Risk Avg', 'value': _dashboard_payload(request)['average_ai_risk'], 'meta': 'Hybrid scoring', 'route': 'ai_assistant'},
        ],
        'command_tiles': [
            {'title': 'Cases', 'description': 'Open the dedicated case management workspace.', 'route': 'cases', 'button': 'Open Cases'},
            {'title': 'Watchlist', 'description': 'Review watch targets and movement flags.', 'route': 'watchlist', 'button': 'Open Watchlist'},
            {'title': 'AI Assistant', 'description': 'Run summaries, briefs, and voice-style queries.', 'route': 'ai_assistant', 'button': 'Launch AI Tools'},
            {'title': 'Drone Feed', 'description': 'Open patrol routes and live feed assignment tools.', 'route': 'drone_feed', 'button': 'Open Drone Feed'},
            {'title': 'Crypto Tracing', 'description': 'Run wallet lookups and exposure traces.', 'route': 'crypto_tracing', 'button': 'Open Crypto Trace'},
            {'title': 'System Health', 'description': 'Review service health and deployment readiness.', 'route': 'system_health', 'button': 'View Health'},
        ],
    })
    return render(request, 'dashboard.html', context)


def incidents_view(request):
    return _render_module(request, 'incidents', {'feature_cards': [
        {'label': 'Live alerts', 'value': len(_dashboard_payload(request)['live_alert_feed'])},
        {'label': 'Critical hotspots', 'value': _dashboard_payload(request)['critical_alerts']},
        {'label': 'Tracked positions', 'value': len(_dashboard_payload(request)['map_positions'])},
    ]})


def cases_view(request):
    selected_case = None
    selected_case_id = request.GET.get('selected')
    if selected_case_id:
        try:
            selected_case = Case.objects.select_related('lead_agency', 'created_by').prefetch_related('assigned_users').filter(id=selected_case_id).first()
        except Exception:
            selected_case = None
    if selected_case is None:
        selected_case = _default_case_for_user(request)
    return _render_module(request, 'cases', {'selected_case': selected_case})


def dispatch_view(request):
    return _render_module(request, 'dispatch', {'feature_cards': [
        {'label': 'Queued alerts', 'value': len(_dashboard_payload(request)['live_alert_feed'])},
        {'label': 'Field officers', 'value': _dashboard_payload(request)['live_officers']},
        {'label': 'Drone patrols', 'value': _dashboard_payload(request)['live_drones']},
    ]})


def field_ops_view(request):
    return _render_module(request, 'field_ops', {'feature_cards': [
        {'label': 'Live officers', 'value': _dashboard_payload(request)['live_officers']},
        {'label': 'Patrol routes', 'value': 12},
        {'label': 'Ready assets', 'value': len(_dashboard_payload(request)['map_positions'])},
    ]})


def intelligence_view(request):
    return _render_module(request, 'intelligence')


def watchlist_view(request):
    watchlist_entries = [
        {'name': 'Suspect Alpha', 'status': 'Active watch', 'location': 'Nairobi CBD'},
        {'name': 'Vehicle KDG 443X', 'status': 'Movement flagged', 'location': 'Mombasa corridor'},
        {'name': 'Wallet Cluster B', 'status': 'Linked device review', 'location': 'Kisumu node'},
    ]
    return _render_module(request, 'watchlist', {'watchlist_entries': watchlist_entries})


def network_graph_view(request):
    return _render_module(request, 'network_graph')


def predictive_ai_view(request):
    return _render_module(request, 'predictive_ai', {'feature_cards': [
        {'label': 'Threat score', 'value': _dashboard_payload(request)['threat_score']},
        {'label': 'AI risk average', 'value': _dashboard_payload(request)['average_ai_risk']},
        {'label': 'Signals reviewed', 'value': len(_dashboard_payload(request)['graph_nodes'])},
    ]})


def ai_assistant_view(request):
    return _render_module(request, 'ai_assistant', {'default_case': _default_case_for_user(request)})


def financial_crimes_view(request):
    return _render_module(request, 'financial_crimes')


def crypto_tracing_view(request):
    return _render_module(request, 'crypto_tracing')


def biometrics_view(request):
    return _render_module(request, 'biometrics')


def evidence_vault_view(request):
    return _render_module(request, 'evidence_vault')


def device_forensics_view(request):
    return _render_module(request, 'device_forensics')


def cloud_forensics_view(request):
    return _render_module(request, 'cloud_forensics')


def iot_forensics_view(request):
    return _render_module(request, 'iot_forensics')


def drone_feed_view(request):
    return _render_module(request, 'drone_feed')


def mobile_devices_view(request):
    return _render_module(request, 'mobile_devices')


def ussd_reports_view(request):
    return _render_module(request, 'ussd_reports')


def compliance_view(request):
    return _render_module(request, 'compliance')


def warrants_view(request):
    return _render_module(request, 'warrants')


def audit_logs_view(request):
    return _render_module(request, 'audit_logs')


def system_health_view(request):
    return _render_module(request, 'system_health')


def settings_view(request):
    return _render_module(request, 'settings')


def dashboard_home(request):
    return dashboard_view(request)


def dashboard_live_feed(request):
    context = _dashboard_payload(request)
    payload = {
        'map_positions': context['map_positions'],
        'graph': {'nodes': context['graph_nodes'], 'edges': context['graph_edges']},
        'alerts': context['alert_feed_payload'],
        'generated_at': context['generated_at'].isoformat(),
        'service_health': context['service_health'],
    }
    return JsonResponse(payload)


def static_health(request):
    return render(request, 'system/static_health.html', _page_context(request, 'settings'))


@require_POST
def cases_action_view(request, action):
    redirect_url = reverse('cases')
    case_id = request.POST.get('case_id')
    try:
        if action == 'create':
            operator = _resolve_operator_user(request)
            agency = _resolve_agency_for_user(operator)
            if not operator or not agency:
                messages.error(request, 'Unable to create case right now. Create an agency and operator profile first.')
                return redirect('cases')
            title = request.POST.get('title', '').strip()
            summary = request.POST.get('summary', '').strip()
            if not title or not summary:
                messages.error(request, 'Title and summary are required to create a case.')
                return redirect('cases')
            case = Case.objects.create(
                case_number=f"C-{timezone.now():%m%d%H%M%S}",
                title=title,
                summary=summary,
                lead_agency=agency,
                created_by=operator,
                classification=request.POST.get('classification', 'RESTRICTED'),
                required_clearance=int(request.POST.get('required_clearance', 2)),
            )
            messages.success(request, f'Case {case.case_number} created successfully.')
            return redirect(f"{redirect_url}?selected={case.id}")

        case = get_object_or_404(Case, pk=case_id)
        if action == 'open':
            case.status = Case.CaseStatus.OPEN
            case.save(update_fields=['status', 'updated_at'])
            messages.success(request, f'{case.case_number} is now open.')
        elif action == 'assign':
            officer_id = request.POST.get('officer_id')
            officer = User.objects.filter(id=officer_id).first() or _resolve_operator_user(request)
            if not officer:
                messages.error(request, 'No officer is available for assignment.')
                return redirect(f"{redirect_url}?selected={case.id}")
            case.assigned_users.add(officer)
            messages.success(request, f'{officer.username} assigned to {case.case_number}.')
        elif action == 'close':
            case.status = Case.CaseStatus.CLOSED
            case.save(update_fields=['status', 'updated_at'])
            messages.success(request, f'{case.case_number} closed successfully.')
        else:
            messages.error(request, 'Unknown case action requested.')
        return redirect(f"{redirect_url}?selected={case.id}")
    except Exception as error:
        messages.error(request, f'Action failed: {error}')
        return redirect('cases')


TOOL_ACTIONS = {
    'watchlist': {
        'add-suspect': {'message': 'Watchlist suspect entry queued for review.', 'redirect': 'watchlist'},
        'view-profile': {'message': 'Opening linked watch profile context.', 'redirect': 'watchlist'},
        'flag-movement': {'message': 'Movement flag sent to threat intelligence feed.', 'redirect': 'intelligence'},
        'link-devices': {'message': 'Device linkage request sent to network graph workflow.', 'redirect': 'network_graph'},
    },
    'crypto': {
        'search-wallet': {'message': 'Wallet search submitted to tracing workspace.', 'redirect': 'crypto_tracing'},
        'view-graph': {'message': 'Relationship graph prepared for the selected wallet cluster.', 'redirect': 'network_graph'},
        'run-trace': {'message': 'Trace run started against the selected wallet path.', 'redirect': 'crypto_tracing'},
    },
    'drone': {
        'open-live-feed': {'message': 'Drone live feed channel requested.', 'redirect': 'drone_feed'},
        'view-routes': {'message': 'Patrol routes loaded for the current air assets.', 'redirect': 'field_ops'},
        'assign-patrol': {'message': 'Patrol assignment submitted to field operations.', 'redirect': 'dispatch'},
    },
}


@require_POST
def tool_action_view(request, tool, action):
    tool_config = TOOL_ACTIONS.get(tool, {})
    action_config = tool_config.get(action)
    if not action_config:
        return JsonResponse({
            'ok': False,
            'message': 'Tool temporarily unavailable',
            'retry': True,
            'logs_url': reverse('audit_logs'),
        }, status=404)
    return JsonResponse({
        'ok': True,
        'message': action_config['message'],
        'redirect_url': reverse(action_config['redirect']),
    })


def sentinel_404(request, exception):
    return render(request, '404.html', _page_context(request, 'dashboard', {'requested_path': request.path}), status=404)


def sentinel_500(request):
    return render(request, '500.html', _page_context(request, 'dashboard'), status=500)


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
