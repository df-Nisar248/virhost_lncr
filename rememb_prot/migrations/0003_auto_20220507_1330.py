# Generated by Django 3.2.3 on 2022-05-07 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rememb_prot', '0002_rename_remb_remembprot'),
    ]

    operations = [
        migrations.AddField(
            model_name='remembprot',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='remembprot',
            name='idd',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='remembprot',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
