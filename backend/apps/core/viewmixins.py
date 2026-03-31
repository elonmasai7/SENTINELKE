from apps.audit.services import record_audit_event
from apps.core.access_control import IsAgencyScopedPermission, scope_queryset_for_user
from rest_framework import viewsets


class AgencyScopedQuerysetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return scope_queryset_for_user(queryset, self.request.user)


class AuditedSecureModelViewSet(AgencyScopedQuerysetMixin, viewsets.ModelViewSet):
    permission_classes = [IsAgencyScopedPermission]

    def _audit(self, action: str, obj):
        record_audit_event(
            actor_username=self.request.user.username,
            actor_ip=self.request.META.get('REMOTE_ADDR'),
            action=action,
            object_type=obj.__class__.__name__,
            object_id=str(obj.pk),
        )

    def perform_create(self, serializer):
        obj = serializer.save()
        self._audit('create', obj)

    def perform_update(self, serializer):
        obj = serializer.save()
        self._audit('update', obj)

    def perform_destroy(self, instance):
        self._audit('delete', instance)
        super().perform_destroy(instance)
