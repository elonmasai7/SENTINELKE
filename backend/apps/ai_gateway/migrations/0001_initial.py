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
            name='AIResponseCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(max_length=64)),
                ('provider_used', models.CharField(max_length=64)),
                ('prompt_hash', models.CharField(max_length=64, unique=True)),
                ('response_body', models.JSONField(default=dict)),
                ('expires_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AIRequestLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_used', models.CharField(max_length=64)),
                ('task_type', models.CharField(max_length=64)),
                ('prompt_hash', models.CharField(max_length=64)),
                ('response_hash', models.CharField(max_length=64)),
                ('sensitivity_level', models.CharField(choices=[('public', 'Public'), ('restricted', 'Restricted'), ('classified', 'Classified')], max_length=16)),
                ('action_reason', models.CharField(blank=True, max_length=255)),
                ('approval_status', models.CharField(choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('PENDING', 'Pending')], default='PENDING', max_length=16)),
                ('prompt_tokens', models.PositiveIntegerField(default=0)),
                ('response_tokens', models.PositiveIntegerField(default=0)),
                ('total_tokens', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.case')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('warrant_reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='compliance.warrant')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='airesponsecache',
            index=models.Index(fields=['task_type', 'provider_used'], name='ai_gateway_a_task_ty_19735f_idx'),
        ),
    ]
