# Generated by Django 4.0.5 on 2022-07-04 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_blogcategory_title_slug_blogitem_title_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogitem',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]