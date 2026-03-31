from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SeizedDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_tag', models.CharField(max_length=64, unique=True)),
                ('device_type', models.CharField(max_length=64)),
                ('manufacturer', models.CharField(blank=True, max_length=120)),
                ('model', models.CharField(blank=True, max_length=120)),
                ('serial_number', models.CharField(blank=True, max_length=120)),
                ('seized_at', models.DateTimeField()),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seized_devices', to='core.case')),
                ('seized_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForensicTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_lab', models.CharField(max_length=255)),
                ('instructions', models.TextField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('RUNNING', 'Running'), ('COMPLETE', 'Complete')], default='PENDING', max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forensic_tasks', to='core.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='forensics.seizeddevice')),
            ],
        ),
        migrations.CreateModel(
            name='ForensicIngestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_system', models.CharField(max_length=120)),
                ('payload_format', models.CharField(max_length=16)),
                ('payload', models.JSONField(default=dict)),
                ('sha256', models.CharField(max_length=64)),
                ('ingested_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingestions', to='forensics.forensictask')),
            ],
        ),
        migrations.CreateModel(
            name='ChainOfCustodyEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_actor', models.CharField(max_length=120)),
                ('to_actor', models.CharField(max_length=120)),
                ('event_type', models.CharField(max_length=120)),
                ('notes', models.TextField(blank=True)),
                ('occurred_at', models.DateTimeField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custody_events', to='forensics.seizeddevice')),
            ],
        ),
    ]
