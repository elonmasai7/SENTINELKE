from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=32, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_number', models.CharField(max_length=64, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('HOLD', 'On Hold'), ('CLOSED', 'Closed')], default='OPEN', max_length=16)),
                ('classification', models.CharField(default='RESTRICTED', max_length=32)),
                ('required_clearance', models.PositiveSmallIntegerField(default=2)),
                ('retention_until', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_cases', to=settings.AUTH_USER_MODEL)),
                ('lead_agency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.agency')),
                ('assigned_users', models.ManyToManyField(blank=True, related_name='assigned_cases', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=80)),
                ('clearance_level', models.PositiveSmallIntegerField(default=1)),
                ('verified_device_id', models.CharField(blank=True, max_length=128)),
                ('trusted_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.agency')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
