from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd

from .import normaliz
from .utils import get_plot, abundances,clean_coulumn_heading
from .models import DataAnalysis

normalized_df = pd.DataFrame()

@login_required
def home(request):
    return render(request,'proteome/home.html')

@login_required
def inputf(request):
    if (request.method == 'POST'):
        files = request.FILES['file']
        # if files.name.endswith('.xlsx'):
        number_of_samples = int(request.POST.get('no_of_sample'))
        number_of_control = int(request.POST.get('no_of_control'))
        user = request.user
        data_als = DataAnalysis.objects.create(file = files, user = user)
        job_id = data_als.id
        data_als.save()
        df = pd.read_excel(files)
        columns = df.columns
        #send all column name to templates as well
        abd_columns = abundances(columns)
        context = {'abd_columns':abd_columns, 'columns':columns,'number_of_samples':number_of_samples,
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
def downloadfile(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="filename.xlsx"'  #filename???????
    df.to_excel(response)
    return response

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

        normaliz.normaliz_data(job_id,sample_columns,control_columns,norm_method,missing_val_rep)
        # return render(request, 'proteome/normalized.html',{'data':data})
        return render(request, 'proteome/home.html')

    return render(request, 'proteome/home.html')
