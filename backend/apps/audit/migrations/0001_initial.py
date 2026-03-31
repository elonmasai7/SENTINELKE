from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor_username', models.CharField(max_length=150)),
                ('actor_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('action', models.CharField(max_length=128)),
                ('object_type', models.CharField(max_length=120)),
                ('object_id', models.CharField(max_length=120)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('event_hash', models.CharField(max_length=64)),
                ('signature', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
