from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('compliance', '0002_warrant_scope_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JointTaskWorkspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('participating_agencies', models.JSONField(default=list)),
                ('access_policy', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joint_workspaces', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LiveAssetPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(max_length=64)),
                ('identifier', models.CharField(max_length=120)),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('observed_at', models.DateTimeField()),
                ('threat_overlay', models.JSONField(blank=True, default=dict)),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='live_positions', to='core.case')),
            ],
        ),
        migrations.CreateModel(
            name='AROverlayPacket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overlay_type', models.CharField(max_length=64)),
                ('target_ref', models.CharField(max_length=255)),
                ('payload', models.JSONField(default=dict)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('expires_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ar_overlays', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
        migrations.CreateModel(
            name='TranscriptRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_audio_ref', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=32)),
                ('original_transcript', models.TextField()),
                ('translated_transcript', models.TextField(blank=True)),
                ('confidence_score', models.FloatField(default=0.0)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transcripts', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
        migrations.CreateModel(
            name='WorkspaceComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='operations.jointtaskworkspace')),
            ],
        ),
    ]
