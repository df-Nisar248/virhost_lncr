# Generated by Django 3.2.14 on 2022-07-18 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proteome', '0013_example_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volcano1', models.FileField(null=True, upload_to='plots/')),
                ('volcano2', models.FileField(null=True, upload_to='plots/')),
                ('volcano3', models.FileField(null=True, upload_to='plots/')),
                ('volcano4', models.FileField(null=True, upload_to='plots/')),
                ('volcano5', models.FileField(null=True, upload_to='plots/')),
                ('volcano6', models.FileField(null=True, upload_to='plots/')),
                ('volcano7', models.FileField(null=True, upload_to='plots/')),
                ('volcano8', models.FileField(null=True, upload_to='plots/')),
                ('volcano9', models.FileField(null=True, upload_to='plots/')),
                ('volcano10', models.FileField(null=True, upload_to='plots/')),
                ('volcano11', models.FileField(null=True, upload_to='plots/')),
                ('volcano12', models.FileField(null=True, upload_to='plots/')),
                ('heatmap', models.FileField(null=True, upload_to='plots/')),
            ],
        ),
    ]
