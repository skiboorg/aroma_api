# Generated by Django 4.0.1 on 2022-01-16 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemvolume',
            name='label',
            field=models.CharField(max_length=20, null=True, verbose_name='Название, например 10 мл'),
        ),
    ]
