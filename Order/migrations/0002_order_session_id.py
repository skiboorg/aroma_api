# Generated by Django 4.0.5 on 2022-07-04 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='session_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
