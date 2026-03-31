from django.contrib.gis.db import models
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geofence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('zone', models.PolygonField(geography=True, srid=4326)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('location', models.PointField(geography=True, srid=4326)),
                ('occurred_at', models.DateTimeField()),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incident_locations', to='core.case')),
            ],
        ),
        migrations.CreateModel(
            name='GeospatialAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('geofence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='geo.geofence')),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='geo.incidentlocation')),
            ],
        ),
    ]
