# Generated by Django 4.0.5 on 2022-07-02 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proteome', '0004_auto_20220620_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataanalysis',
            name='fileType',
            field=models.CharField(max_length=20, null=True),
        ),
    ]