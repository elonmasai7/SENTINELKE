from django.db import migrations, models
import django.db.models.deletion
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DroneFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_identifier', models.CharField(max_length=120, unique=True)),
                ('gps_route', django.contrib.gis.db.models.fields.LineStringField(blank=True, geography=True, null=True, srid=4326)),
                ('aerial_imagery_reference', models.CharField(blank=True, max_length=255)),
                ('mapping_3d_reference', models.CharField(blank=True, max_length=255)),
                ('last_seen', models.DateTimeField()),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drone_feeds', to='core.case')),
            ],
        ),
        migrations.CreateModel(
            name='OfflineSyncIntegrityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=128)),
                ('action_type', models.CharField(max_length=64)),
                ('payload_hash', models.CharField(max_length=64)),
                ('signature', models.CharField(max_length=256)),
                ('queued_at', models.DateTimeField()),
                ('synced_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(default='QUEUED', max_length=32)),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offline_sync_logs', to='core.case')),
            ],
        ),
    ]
