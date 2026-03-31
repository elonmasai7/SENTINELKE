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
            name='PatternOfLifeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_ref', models.CharField(max_length=255)),
                ('baseline_window_days', models.PositiveIntegerField(default=30)),
                ('baseline_features', models.JSONField(default=dict)),
                ('deviation_score', models.FloatField(default=0.0)),
                ('anomaly_explanation', models.TextField(blank=True)),
                ('timeline_graph', models.JSONField(blank=True, default=list)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pattern_profiles', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
        migrations.CreateModel(
            name='PredictiveThreatScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_ref', models.CharField(max_length=255)),
                ('score', models.PositiveSmallIntegerField()),
                ('level', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')], max_length=16)),
                ('explanation', models.TextField()),
                ('factor_breakdown', models.JSONField(default=dict)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictive_scores', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
        migrations.CreateModel(
            name='AISummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_type', models.CharField(max_length=64)),
                ('source_reference', models.CharField(max_length=255)),
                ('executive_summary', models.TextField()),
                ('key_entities', models.JSONField(blank=True, default=list)),
                ('named_locations', models.JSONField(blank=True, default=list)),
                ('action_recommendations', models.TextField(blank=True)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_summaries', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
        migrations.CreateModel(
            name='SyntheticMediaScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evidence_ref', models.CharField(max_length=255)),
                ('authenticity_confidence', models.FloatField(default=0.0)),
                ('manipulation_likelihood', models.FloatField(default=0.0)),
                ('flagged_regions', models.JSONField(blank=True, default=list)),
                ('findings', models.JSONField(blank=True, default=dict)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='synthetic_scans', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
    ]
