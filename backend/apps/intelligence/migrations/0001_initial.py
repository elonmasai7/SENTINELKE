from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraphEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_type', models.CharField(max_length=64)),
                ('external_id', models.CharField(max_length=120, unique=True)),
                ('properties', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='IntelReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_type', models.CharField(choices=[('OSINT', 'OSINT'), ('HUMINT', 'HUMINT'), ('SIGINT', 'SIGINT'), ('CITIZEN', 'Citizen Report')], max_length=16)),
                ('language', models.CharField(default='en', max_length=32)),
                ('content', models.TextField()),
                ('source_ref', models.CharField(blank=True, max_length=255)),
                ('reported_at', models.DateTimeField()),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intel_reports', to='core.case')),
            ],
        ),
        migrations.CreateModel(
            name='GraphRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(max_length=64)),
                ('properties', models.JSONField(default=dict)),
                ('from_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_relations', to='intelligence.graphentity')),
                ('to_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_relations', to='intelligence.graphentity')),
            ],
        ),
        migrations.CreateModel(
            name='ThreatSignal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=120)),
                ('score', models.FloatField(default=0.0)),
                ('explanation', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signals', to='intelligence.intelreport')),
            ],
        ),
    ]
