# Generated by Django 4.0.5 on 2022-07-11 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proteome', '0009_remove_dataanalysis_cna_remove_dataanalysis_sna'),
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='documents/')),
            ],
        ),
    ]
