# Generated by Django 4.1.3 on 2023-03-29 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_workersreg_wages'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='wages',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
