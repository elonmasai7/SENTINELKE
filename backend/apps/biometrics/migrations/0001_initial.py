from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('compliance', '0002_warrant_scope_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BiometricFusionQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_ref', models.CharField(max_length=255)),
                ('face_embedding_ref', models.CharField(blank=True, max_length=255)),
                ('gait_signature_ref', models.CharField(blank=True, max_length=255)),
                ('voiceprint_ref', models.CharField(blank=True, max_length=255)),
                ('fingerprint_ref', models.CharField(blank=True, max_length=255)),
                ('confidence', models.FloatField(default=0.0)),
                ('decision_support_notes', models.TextField(blank=True)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biometric_queries', to='core.case')),
                ('queried_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
        migrations.CreateModel(
            name='BehavioralBiometricProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typing_rhythm', models.JSONField(blank=True, default=dict)),
                ('touchscreen_behavior', models.JSONField(blank=True, default=dict)),
                ('interaction_anomaly_score', models.FloatField(default=0.0)),
                ('last_validated_at', models.DateTimeField(blank=True, null=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='behavioral_biometrics', to='core.userprofile')),
            ],
        ),
    ]
