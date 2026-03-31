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
            name='WalletCluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_label', models.CharField(max_length=120)),
                ('wallets', models.JSONField(default=list)),
                ('risk_score', models.FloatField(default=0.0)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_clusters', to='core.case')),
            ],
        ),
        migrations.CreateModel(
            name='CryptoLedgerEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blockchain', models.CharField(max_length=32)),
                ('tx_hash', models.CharField(max_length=255, unique=True)),
                ('wallet_from', models.CharField(max_length=255)),
                ('wallet_to', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=24)),
                ('amount_usd', models.DecimalField(decimal_places=2, default=0, max_digits=24)),
                ('occurred_at', models.DateTimeField()),
                ('suspicious_flags', models.JSONField(blank=True, default=list)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crypto_events', to='core.case')),
            ],
        ),
        migrations.CreateModel(
            name='IoTForensicArtifact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(max_length=120)),
                ('firmware_version', models.CharField(max_length=80)),
                ('extracted_logs', models.JSONField(default=list)),
                ('linked_persons', models.JSONField(blank=True, default=list)),
                ('captured_at', models.DateTimeField()),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iot_artifacts', to='core.case')),
            ],
        ),
        migrations.CreateModel(
            name='CloudLegalHold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=64)),
                ('account_reference', models.CharField(max_length=255)),
                ('retention_lock_until', models.DateTimeField()),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('RELEASED', 'Released'), ('EXPIRED', 'Expired')], default='ACTIVE', max_length=16)),
                ('deletion_events', models.JSONField(blank=True, default=list)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cloud_legal_holds', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
    ]
