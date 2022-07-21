# Generated by Django 3.2.14 on 2022-07-18 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Remembprot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pmid', models.CharField(blank=True, max_length=255, null=True)),
                ('CellOrtissue', models.CharField(blank=True, max_length=255, null=True)),
                ('disease', models.CharField(blank=True, max_length=255, null=True)),
                ('author', models.CharField(blank=True, max_length=255, null=True)),
                ('paper', models.CharField(blank=True, max_length=255, null=True)),
                ('organism', models.CharField(blank=True, max_length=255, null=True)),
                ('profileOrDifex', models.CharField(blank=True, max_length=20, null=True)),
                ('contxtOfIdent', models.CharField(blank=True, max_length=20, null=True)),
                ('contxtOfDiferentialREG', models.CharField(blank=True, max_length=20, null=True)),
                ('test', models.CharField(blank=True, max_length=255, null=True)),
                ('control', models.CharField(blank=True, max_length=255, null=True)),
                ('foldchange', models.CharField(blank=True, max_length=255, null=True)),
                ('expression', models.CharField(blank=True, max_length=255, null=True)),
                ('protienExtractMethod', models.CharField(blank=True, max_length=255, null=True)),
                ('geneSymbol', models.CharField(blank=True, max_length=255, null=True)),
                ('geneID', models.CharField(blank=True, max_length=255, null=True)),
                ('ontology', models.CharField(blank=True, max_length=255, null=True)),
                ('membraneType', models.CharField(blank=True, max_length=255, null=True)),
                ('peripheral', models.CharField(blank=True, max_length=255, null=True)),
                ('refSeq', models.CharField(blank=True, max_length=255, null=True)),
                ('predictedTmh', models.CharField(blank=True, max_length=255, null=True)),
                ('isTrans', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
