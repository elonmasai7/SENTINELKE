from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('compliance', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveillanceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_identifier', models.CharField(max_length=255)),
                ('provider', models.CharField(max_length=120)),
                ('request_metadata', models.JSONField(default=dict)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING', 'Pending Approval'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('EXECUTED', 'Executed')], default='DRAFT', max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveillance_requests', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
        ),
        migrations.CreateModel(
            name='InterceptMetadataRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_reference', models.CharField(max_length=120)),
                ('payload', models.JSONField(default=dict)),
                ('collected_at', models.DateTimeField()),
                ('surveillance_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metadata_records', to='surveillance.surveillancerequest')),
            ],
        ),
    ]
