# Generated by Django 5.1.2 on 2024-10-23 02:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_threshold'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'notifications',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='threshold',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='threshold',
            name='threshold_type',
            field=models.CharField(choices=[('min', 'Minimum Value'), ('max', 'Maximum Value'), ('exact', 'Exact Value')], max_length=10),
        ),
        migrations.AddConstraint(
            model_name='threshold',
            constraint=models.UniqueConstraint(fields=('employee', 'questionnaire'), name='unique_employee_questionnaire'),
        ),
        migrations.AddField(
            model_name='notification',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.employee'),
        ),
    ]
