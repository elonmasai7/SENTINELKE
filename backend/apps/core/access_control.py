from django.db.models import Q
from rest_framework.permissions import BasePermission

from apps.core.models import Case

CLASSIFICATION_CLEARANCE = {
    'PUBLIC': 1,
    'RESTRICTED': 2,
    'CONFIDENTIAL': 3,
    'SECRET': 4,
    'TOP_SECRET': 5,
}


def _profile(user):
    return getattr(user, 'userprofile', None)


def required_clearance(case: Case) -> int:
    explicit = getattr(case, 'required_clearance', None)
    if explicit:
        return explicit
    return CLASSIFICATION_CLEARANCE.get(case.classification, 2)


def user_can_access_case(user, case: Case) -> bool:
    if user.is_superuser:
        return True
    profile = _profile(user)
    if not profile:
        return False
    if case.lead_agency_id != profile.agency_id:
        return False
    if profile.clearance_level < required_clearance(case):
        return False
    if user.is_staff:
        return True
    return case.created_by_id == user.id or case.assigned_users.filter(id=user.id).exists()


def _resolve_case(obj):
    if isinstance(obj, Case):
        return obj

    paths = [
        'case',
        'warrant.case',
        'device.case',
        'task.case',
        'report.case',
        'transaction.case',
        'surveillance_request.case',
        'incident.case',
        'workspace.case',
        'query.case',
    ]
    for path in paths:
        current = obj
        ok = True
        for part in path.split('.'):
            current = getattr(current, part, None)
            if current is None:
                ok = False
                break
        if ok:
            return current
    return None


def _case_filter(prefix: str, user, profile):
    p = f'{prefix}__' if prefix else ''
    base = Q(**{f'{p}lead_agency_id': profile.agency_id}) & Q(**{f'{p}required_clearance__lte': profile.clearance_level})
    if user.is_staff:
        return base
    return base & (Q(**{f'{p}created_by': user}) | Q(**{f'{p}assigned_users': user}))


def scope_queryset_for_user(queryset, user):
    if user.is_superuser:
        return queryset
    profile = _profile(user)
    if not profile:
        return queryset.none()

    model_name = queryset.model.__name__
    if model_name == 'Agency':
        return queryset.filter(id=profile.agency_id)
    if model_name == 'UserProfile':
        return queryset.filter(agency_id=profile.agency_id)
    if model_name == 'Case':
        return queryset.filter(_case_filter('', user, profile)).distinct()
    if model_name in {'Warrant', 'ApprovalRecord', 'SeizedDevice', 'ChainOfCustodyEvent', 'ForensicTask', 'ForensicIngestion',
                      'IntelReport', 'ThreatSignal', 'FinancialTransaction', 'FraudAlert', 'IncidentLocation', 'GeospatialAlert',
                      'SurveillanceRequest', 'InterceptMetadataRecord', 'WorkspaceNote', 'SharedEvidence', 'PatternOfLifeProfile',
                      'PredictiveThreatScore', 'AISummary', 'SyntheticMediaScan', 'AROverlayPacket', 'TranscriptRecord',
                      'JointTaskWorkspace', 'WalletCluster', 'CryptoLedgerEvent', 'IoTForensicArtifact', 'CloudLegalHold',
                      'BiometricFusionQuery', 'EvidenceIntegrityAnchor', 'AutomatedForensicReport', 'WitnessRedactionJob',
                      'DroneFeed', 'OfflineSyncIntegrityLog', 'FederatedQuery', 'InternationalPartnerExchange'}:
        if model_name == 'Warrant':
            return queryset.filter(_case_filter('case', user, profile)).distinct()
        if model_name == 'ApprovalRecord':
            return queryset.filter(_case_filter('warrant__case', user, profile)).distinct()
        if model_name == 'SeizedDevice':
            return queryset.filter(_case_filter('case', user, profile)).distinct()
        if model_name == 'ChainOfCustodyEvent':
            return queryset.filter(_case_filter('device__case', user, profile)).distinct()
        if model_name == 'ForensicTask':
            return queryset.filter(_case_filter('case', user, profile)).distinct()
        if model_name == 'ForensicIngestion':
            return queryset.filter(_case_filter('task__case', user, profile)).distinct()
        if model_name == 'IntelReport':
            return queryset.filter(_case_filter('case', user, profile)).distinct()
        if model_name == 'ThreatSignal':
            return queryset.filter(_case_filter('report__case', user, profile)).distinct()
        if model_name == 'FinancialTransaction':
            return queryset.filter(_case_filter('case', user, profile)).distinct()
        if model_name == 'FraudAlert':
            return queryset.filter(_case_filter('transaction__case', user, profile)).distinct()
        if model_name == 'IncidentLocation':
            return queryset.filter(_case_filter('case', user, profile)).distinct()
        if model_name == 'GeospatialAlert':
            return queryset.filter(_case_filter('incident__case', user, profile)).distinct()
        if model_name == 'SurveillanceRequest':
            return queryset.filter(_case_filter('case', user, profile)).distinct()
        if model_name == 'InterceptMetadataRecord':
            return queryset.filter(_case_filter('surveillance_request__case', user, profile)).distinct()
        if model_name == 'WorkspaceNote':
            return queryset.filter(_case_filter('case', user, profile)).distinct()
        if model_name == 'SharedEvidence':
            return queryset.filter(_case_filter('case', user, profile)).distinct()
        if model_name in {'PatternOfLifeProfile', 'PredictiveThreatScore', 'AISummary', 'SyntheticMediaScan', 'AROverlayPacket',
                          'TranscriptRecord', 'JointTaskWorkspace', 'WalletCluster', 'CryptoLedgerEvent', 'IoTForensicArtifact',
                          'CloudLegalHold', 'BiometricFusionQuery', 'EvidenceIntegrityAnchor', 'AutomatedForensicReport',
                          'WitnessRedactionJob', 'DroneFeed', 'OfflineSyncIntegrityLog', 'FederatedQuery',
                          'InternationalPartnerExchange'}:
            return queryset.filter(_case_filter('case', user, profile)).distinct()
    if model_name == 'WorkspaceComment':
        return queryset.filter(_case_filter('workspace__case', user, profile)).distinct()
    if model_name == 'FederatedResult':
        return queryset.filter(_case_filter('query__case', user, profile)).distinct()
    if model_name == 'SecureMessage':
        return queryset.filter(Q(sender=user) | Q(receiver=user))
    if model_name == 'BehavioralBiometricProfile':
        return queryset.filter(profile__agency_id=profile.agency_id)
    if model_name == 'LiveAssetPosition':
        return queryset.filter(_case_filter('case', user, profile)).distinct()

    if user.is_staff:
        return queryset
    return queryset.none()


class IsAgencyScopedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return _profile(request.user) is not None

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        profile = _profile(request.user)
        if not profile:
            return False

        model_name = obj.__class__.__name__
        if model_name == 'Agency':
            return obj.id == profile.agency_id
        if model_name == 'UserProfile':
            return obj.agency_id == profile.agency_id and (request.user.is_staff or obj.user_id == request.user.id)
        if model_name == 'SecureMessage':
            return obj.sender_id == request.user.id or obj.receiver_id == request.user.id
        if model_name == 'BehavioralBiometricProfile':
            return obj.profile.agency_id == profile.agency_id

        case = _resolve_case(obj)
        if case is None:
            return request.user.is_staff
        return user_can_access_case(request.user, case)
