# Generated by Django 4.0.5 on 2022-07-02 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proteome', '0005_dataanalysis_filetype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataanalysis',
            name='fileType',
        ),
    ]