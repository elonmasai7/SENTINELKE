from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Agency(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=32, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT)
    role = models.CharField(max_length=80)
    clearance_level = models.PositiveSmallIntegerField(default=1)
    verified_device_id = models.CharField(max_length=128, blank=True)
    trusted_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} ({self.role})'


class Case(models.Model):
    class CaseStatus(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        HOLD = 'HOLD', 'On Hold'
        CLOSED = 'CLOSED', 'Closed'

    case_number = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    status = models.CharField(max_length=16, choices=CaseStatus.choices, default=CaseStatus.OPEN)
    lead_agency = models.ForeignKey(Agency, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_cases')
    assigned_users = models.ManyToManyField(User, related_name='assigned_cases', blank=True)
    classification = models.CharField(max_length=32, default='RESTRICTED')
    required_clearance = models.PositiveSmallIntegerField(default=2)
    retention_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.case_number
