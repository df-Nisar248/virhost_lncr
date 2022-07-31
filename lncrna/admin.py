from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd
import csv

from .models import Lncrna , LncrnaTarget , Files


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class LncrnaAdmin(admin.ModelAdmin):

    list_display = ('stimuli','dosage','time_point','experiment_type','cell_line','lncrna_name','ncbi_gene','ensembl_id','foldchange','expression',
        'pubmed_id','reference')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
        if (request.method == 'POST' ):
            csv_file = request.FILES['csv_upload']
            # if not csv_file.name.endswith('.csv') or csv_file.name.endswith('.xlsx'):
            #     messages.warning(request,'the wrong type of file was uploaded ')
            #     return HttpResponseRedirect(request.path_info)

            df = pd.read_excel(csv_file)
            df.fillna('', inplace=True)
            df['Stimuli'] = df['Stimuli'].str.replace('/','_')

            df_records = df.to_dict('records')

            for data in df_records:
                print(data)
                created = Lncrna.objects.update_or_create (
                    stimuli = data['Stimuli'],
                    dosage = data['Dosage'],
                    time_point = data['Time point'],
                    experiment_type = data['Experiment Type'],
                    cell_line = data['Cell line'],
                    lncrna_name = data['lncRNA name as in article'],
                    ncbi_gene = data['NCBI_Gene_symbol'],
                    ensembl_id = data['Ensembl_id'],
                    foldchange = data['Foldchange'],
                    expression = data['Expression'],
                    pubmed_id = data['PubMed_ID'],
                    reference =data['Reference']
                    )




        form = CsvImportForm()
        data = {'form': form }
        return render(request,'admin/csv_upload.html',data)


class LncrnaTargetAdmin(admin.ModelAdmin):

    list_display = ('regulator','target','regulatory_mech','regulatory_type','Target_type','regulator_ensemble_id')


    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv-trgt/', self.upload_csv_trgt),]
        return new_urls + urls

    def upload_csv_trgt(self, request):
        if (request.method == 'POST' ):
            csv_file = request.FILES['csv_upload']

            df = pd.read_excel(csv_file)
            df.fillna('', inplace=True)
            df_records = df.to_dict('records')

            for data in df_records:
                print(data)
                created = LncrnaTarget.objects.update_or_create (
                    regulator = data['Regulator'],
                    target = data['Target'],
                    regulatory_mech = data['Regulatory Mechanism'],
                    regulatory_type = data['Regulatory Type'],
                    Target_type = data['Target Type'],
                    regulator_ensemble_id = data['Regulator EnsembleID'],
                    )

                # url = reverse('admin:index')
                # return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {'form': form }
        return render(request,'admin/csv_upload.html',data)


admin.site.register(Lncrna, LncrnaAdmin)
admin.site.register(LncrnaTarget, LncrnaTargetAdmin)

admin.site.register(Files)
