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
            name='FederatedQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_text', models.TextField()),
                ('partner_systems', models.JSONField(default=list)),
                ('selective_visibility', models.JSONField(blank=True, default=dict)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='federated_queries', to='core.case')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
        migrations.CreateModel(
            name='InternationalPartnerExchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.CharField(max_length=120)),
                ('endpoint', models.CharField(max_length=255)),
                ('consent_reference', models.CharField(max_length=255)),
                ('response_status', models.PositiveIntegerField(default=0)),
                ('payload_hash', models.CharField(max_length=64)),
                ('requested_scope', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='international_exchanges', to='core.case')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
        migrations.CreateModel(
            name='FederatedResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.CharField(max_length=120)),
                ('result_reference', models.CharField(max_length=255)),
                ('relevance', models.FloatField(default=0.0)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='federation.federatedquery')),
            ],
        ),
    ]
