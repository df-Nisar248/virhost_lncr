from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd
import csv

from .models import Remembprot

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class RemembprotaAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
        if (request.method == 'POST' ):
            csv_file = request.FILES['csv_upload']
            if not csv_file.name.endswith('.csv'):
                messages.warning(request,'the wrong type of file was uploaded ')
                return HttpResponseRedirect(request.path_info)

            df = pd.read_csv(csv_file, encoding_errors='ignore')
            df.fillna('', inplace=True)

            df_records = df.to_dict('records')

            for data in df_records:
                print(data)
                created = Remembprot.objects.update_or_create (
                    idd = data['idd'],
                    name = data['name'],
                    address = data['address'],
                      )




        form = CsvImportForm()
        data = {'form': form }
        return render(request,'admin/csv_upload.html',data)

admin.site.register(Remembprot,RemembprotaAdmin)
