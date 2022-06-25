from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.http import Http404

import os
from django.conf import settings
import csv
from io import StringIO
from django.core.files.base import ContentFile

from .import normaliz
from .utils import get_plot, abundances,clean_coulumn_heading
from .models import DataAnalysis


normalized_df = pd.DataFrame()

@login_required
def home(request):
    return render(request,'proteome/index.html')

@login_required
def input(request):
    return render(request,'proteome/home.html')


@login_required
def inputf(request):
    if (request.method == 'POST'):
        files = request.FILES['file']
        # if files.name.endswith('.xlsx'):
        number_of_samples = int(request.POST.get('no_of_sample'))
        number_of_control = 1
        user = request.user
        data_als = DataAnalysis.objects.create(file = files, user = user)
        job_id = data_als.id
        data_als.save()
        df = pd.read_excel(files)
        columns = df.columns
        all_column = []
        for column in columns:
            if ',' in column:
                column = column.replace(',',' ')
                all_column.append(column)
            else:
                all_column.append(column)
        #send all column name to templates as well
        abd_columns = abundances(all_column)
        context = {'abd_columns':abd_columns, 'columns':all_column,'number_of_samples':number_of_samples,
        'number_of_control':number_of_control,'job_id':job_id}

        return render(request,'proteome/pre_analyze.html',context)
    # form = FileUpload()
    # data = {'form': form}
    return render(request, 'proteome/home.html')

@login_required
def plotss(request):
    df = normalized_df

    x1 = data.x1

    x2 = data.x2

    x3 = data.x3

    sample_a_plot = get_plot([x1,x2,x3])
    context = {'sample_a_plot': sample_a_plot}
    return render(request, 'proteome/plots.html',context)
    # sample_b_plot = get_plot([b1,b2,b3])
    # sample_c_plot = get_plot([c1,c2,c3])

@login_required
def pre_process(request):
    if (request.method == 'POST'):
        files = request.FILES['file']
        df = pd.read_excel(files)
        columns = df.columns
        abundance_list = abundances(columns)
        context = {'abundance_list': abundance_list}
        return render(request, 'proteome/list_of_abc.html', context)



@login_required
def downloadfile(request,job_id = None):

    print(job_id)
    q = DataAnalysis.objects.get(id = job_id)
    file = q.resultData.path

    download_path = os.path.join(settings.MEDIA_ROOT, file)

    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(download_path)
            return response

    raise Http404


@login_required
def analaze_cols(request):
    if (request.method == 'POST'):
        sample_data_columns = request.POST.get('final_sample_data')
        final_control_data = request.POST.get('final_control_data')
        job_id = request.POST.get('job_id')
        missing_val_rep = request.POST.get('missing_val')
        norm_method = request.POST.get('norm_method')

        sample_columns = clean_coulumn_heading(sample_data_columns)
        control_columns = clean_coulumn_heading(final_control_data)

        final_data = normaliz.normaliz_data(job_id,sample_columns,control_columns,norm_method,missing_val_rep)
        final_data.to_csv('resultttt.csv', mode='a')
        new_df = final_data.to_csv()
        updated_file = ContentFile(new_df)
        updated_file.name = "result.csv"

        result_q = DataAnalysis.objects.get(id =job_id)
        result_q.resultData = updated_file
        result_q.save()
        data = final_data.head(30)
        return render(request, 'proteome/normalized.html',{'data':data,'job_id':job_id} )

    return render(request, 'proteome/home.html')
