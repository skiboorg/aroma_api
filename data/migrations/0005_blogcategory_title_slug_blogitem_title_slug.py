# Generated by Django 4.0.5 on 2022-07-04 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_blogitem_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='title_slug',
            field=models.CharField(editable=False, max_length=100, null=True, verbose_name='Название категории'),
        ),
        migrations.AddField(
            model_name='blogitem',
            name='title_slug',
            field=models.CharField(editable=False, max_length=100, null=True, verbose_name='Название статьи'),
        ),
    ]
