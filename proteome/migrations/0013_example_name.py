# Generated by Django 4.0.5 on 2022-07-11 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proteome', '0012_example_number_of_sample'),
    ]

    operations = [
        migrations.AddField(
            model_name='example',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]