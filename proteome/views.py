from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.http import Http404
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.conf import settings

import csv
import base64
from io import BytesIO

import pandas as pd
import numpy as np
from plotly.offline import plot
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from .import normaliz
from .utils import abundances,clean_coulumn_heading,intensities,lablesforbox, sort_name , columnsforbox
from .models import DataAnalysis , Example

normalized_df = pd.DataFrame()

@login_required
def home(request):
    return render(request,'proteome/index.html')

@login_required
def input(request):
    return render(request,'proteome/home.html')

@login_required

def inputf(request):
    #for example dataset
    if (request.method == 'GET'):
        q = Example.objects.get(usethis = True)
        file = q.file.path
        lablled = q.labledData
        lablefree = q.lableFreeData
        number_of_samples = q.number_of_sample
        number_of_control = 1
        df = pd.read_excel(file, engine='openpyxl')

        columns = df.columns
        abd_columns = []
        all_column = []

        for column in columns:
            if ',' in column:
                column = column.replace(',',' ')
                all_column.append(column)
            else:
                all_column.append(column)
        #send all column name to templates as well
        if lablled:
            abd_columns = abundances(all_column)
        else:
            abd_columns = intensities(all_column)

        user = request.user
        data_als = DataAnalysis.objects.create(file = file, user = user, labledData = lablled,lableFreeData = lablefree )
        job_id = data_als.id
        data_als.save()

        context = {'abd_columns':abd_columns, 'number_of_samples':number_of_samples,
                'number_of_control':number_of_control,'job_id':job_id}
        return render(request,'proteome/pre_analyze.html',context)

    if (request.method == 'POST'):

        files = request.FILES['file']
        lableornot = request.POST.get('lableornot')
        lablled = False
        lablefree = False
        if (lableornot == "lablled"):
            lablled = True
        if (lableornot == "lablefree"):
            lablefree = True

        if files.name.endswith('.xlsx') or files.name.endswith('.csv') or files.name.endswith('.txt'):
            user = request.user

            if (request.POST.get('rep_method')) == "techrep":
                # files = request.FILES['file']
                number_of_samples = int(request.POST.get('no_of_sample'))
                number_of_control = 1
                data_als = DataAnalysis.objects.create(file = files, user = user, labledData = lablled,lableFreeData = lablefree )
                job_id = data_als.id
                data_als.save()
                df = pd.DataFrame()
                if files.name.endswith('.xlsx'):
                    df = pd.read_excel(files,engine='openpyxl')
                elif files.name.endswith('.csv'):
                    df = pd.read_csv(files , encoding_errors = 'ignore')
                else:
                    data = DataAnalysis.objects.get(id = job_id)
                    df = pd.read_csv(data.file.path, delimiter = '\t', encoding_errors = 'ignore')

                columns = df.columns
                all_column = []
                abd_columns = []
                for column in columns:
                    if ',' in column:
                        column = column.replace(',',' ')
                        all_column.append(column)
                    else:
                        all_column.append(column)
                #send all column name to templates as well
                if lableornot == "lablled":
                    abd_columns = abundances(all_column)
                else:
                    abd_columns = intensities(all_column)

                context = {'abd_columns':abd_columns, 'columns':all_column,'number_of_samples':number_of_samples,
                'number_of_control':number_of_control,'job_id':job_id}
                return render(request,'proteome/pre_analyze.html',context)

            else:
                number_of_batches = int(request.POST.get('no_of_batches'))
                data_als = DataAnalysis.objects.create(file = files, user = user)
                job_id = data_als.id
                data_als.save()

                if files.name.endswith('.xlsx'):
                    df = pd.read_excel(files,engine='openpyxl')
                elif files.name.endswith('.csv'):
                    df = pd.read_csv(files, encoding_errors = 'ignore')
                else:
                    data = DataAnalysis.objects.get(id = job_id)
                    df = pd.read_csv(data.file.path, delimiter = '\t', encoding_errors = 'ignore')

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

                context = {'abd_columns':abd_columns, 'columns':all_column,'number_of_batches':number_of_batches,
                    'job_id':job_id}

                return render(request,'proteome/pre_anlz_bio.html',context)

        else:
            #send message saying file format incorrect
            return render(request, 'proteome/home.html')


    # form = FileUpload()
    # data = {'form': form}
    return render(request, 'proteome/home.html')


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

        final_data,df_before_norm, df_after_norm, cna, sna = normaliz.normaliz_data(job_id,sample_columns,
            control_columns,norm_method,missing_val_rep)

        request.session['cna'] = cna
        request.session['sna'] = sna

        new_df = final_data.to_csv(index = False)
        updated_file = ContentFile(new_df)
        updated_file.name = "result.csv"

        result_q = DataAnalysis.objects.get(id =job_id)
        result_q.resultData = updated_file
        result_q.save()

        # pca = PCA(n_components=2)
        # components = pca.fit_transform(df_PCA_before)
        # pcafig_before = px.scatter(df_PCA_before, x=0, y=1 )

        # components = pca.fit_transform(df_PCA_after)
        # pcafig_after = px.scatter(components, x=0, y=1)
        pca_before =plot_pca(df_before_norm,sample_columns,control_columns, title = "PCA plot Before Normalization", )
        pca_after =plot_pca(df_after_norm,sample_columns,control_columns,title = "PCA plot After Normalization")

        df_before_norm.columns = columnsforbox(df_before_norm.columns)
        before_norm_box = get_box_plot(df_before_norm, title = "Box plot Before Normalization")

        df_after_norm.columns = columnsforbox(df_after_norm.columns)
        after_norm_box = get_box_plot(df_after_norm, title = "Box plot After Normalization")

        context = {'job_id':job_id,
            'pca_before':pca_before,'pca_after':pca_after,'before_norm_box':
            before_norm_box, 'after_norm_box': after_norm_box}

        return render(request, 'proteome/normalized.html', context)

    return render(request, 'proteome/home.html')


@login_required
def analaze_cols_bio(request):
    if (request.method == 'POST'):
        sample_data_columns = request.POST.get('final_sample_data')
        final_control_data = request.POST.get('final_control_data')
        job_id = request.POST.get('job_id')
        missing_val_rep = request.POST.get('missing_val')
        norm_method = request.POST.get('norm_method')

        sample_columns = clean_coulumn_heading(sample_data_columns)
        control_columns = clean_coulumn_heading(final_control_data)


        final_data, df_PCA_before, df_PCA_after, df_before_bc,  df_after_bc , cna, sna = normaliz.normaliz_data_bio(job_id,
            sample_columns,control_columns,norm_method,missing_val_rep)

        request.session['cna'] = cna
        request.session['sna'] = sna

        new_df = final_data.to_csv(index = False)
        updated_file = ContentFile(new_df)
        updated_file.name = "result.csv"

        result_q = DataAnalysis.objects.get(id =job_id)
        result_q.resultData = updated_file
        result_q.save()

        # box_plot = plot(fig, output_type = "div")
        # 'box_plot':box_plot

        # pcafig_before = px.scatter(
        #     df_PCA_before,
        #     )

        # pcafig_after = px.scatter(
        #     df_PCA_after,
        #     )

        before_norm_box = get_box_plot(df_before_bc, title = "Box plot Before Normalization")

        after_norm_box = get_box_plot(df_after_bc, title = "Box plot After Normalization")

        box_before_plot = plot(before_bc_box, output_type = "div")
        box_after_plot = plot(after_bc_box, output_type = "div")

        context = {'box_before_plot':box_before_plot,
            'box_after_plot':box_after_plot, 'job_id':job_id}

        return render(request, 'proteome/normalized.html', context)

    return render(request, 'proteome/home.html')

@login_required
def pvalues(request):
    if (request.method == 'POST'):
        job_id = int(request.POST.get('job_id'))
        pvalue = request.POST.get('pvalue')
        cna = request.session.get('cna')
        sna = request.session.get('sna')
        df, forvolcano , forheatmap= normaliz.pvalAndRatio(cna,sna,job_id, pvalue)
        # result_q = DataAnalysis.objects.get(id =job_id)
        # result_q.resultData = final_data
        # result_q.save()
        volcanoplotlist = list()
        for volcanocols in forvolcano:
            volcanodf = df[volcanocols]
            volcanodf.set_index('Accession', inplace = True)
            fig = px.scatter(volcanodf, x=volcanocols[0], y = volcanocols[1])
            volcanoplot = plot(fig, output_type = "div")
            volcanoplotlist.append(volcanoplot)
        # figure = io.BytesIO()
        # content_file = ImageFile(volcanoplot)
        plt.switch_backend('AGG')
        sns.clustermap(forheatmap,cbar_pos=(0.03,.01, .03, .2),yticklabels=False  ,cmap="RdYlGn_r",figsize=(5,8))
        heatmap = get_graph()
        # heatmap_to_plot = plot(heatmap_fig, output_type = "div")

        new_df = df.to_csv(index = False)
        updated_file = ContentFile(new_df)
        updated_file.name = "finalresult.csv"

        result_q = DataAnalysis.objects.get(id =job_id)
        result_q.resultData = updated_file
        result_q.save()

        context = {'job_id':job_id, 'volcanoplotlist': volcanoplotlist, 'heatmap': heatmap}
        return render(request, 'proteome/pvalandratio.html', context)


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format = 'svg')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def plot_pca(df_for_pca,sample_columns,control_columns,title):

    df = df_for_pca.loc[:, df_for_pca.columns != 'Accession']
    df = df.transpose()

    scaler = StandardScaler()
    scaler.fit(df)
    df_np_array = scaler.transform(df)

    sample_list = list()
    for samples in sample_columns:
        for each_sample in samples:
            sample_list.append(sort_name(samples).strip())

    for control in control_columns:
        for each_control in control:
            sample_list.append(sort_name(control).strip())

    pca = PCA(n_components=2)

    components = pca.fit_transform(df_np_array)
    pca_df = pd.DataFrame(components, columns = ['x','y'])
    pca_df['samples'] = pd.Series(sample_list)
    # pca_df.set_index('samples', inplace = True)

    plt.switch_backend('AGG')
    plt.scatter(pca_df['x'],pca_df['y'], s=50, alpha=0.7)

    plt.title(title)

    plt.tight_layout()
    pcaplot = get_graph()
    return pcaplot


def get_box_plot(df,title):
    plt.switch_backend('AGG')
    #do exception handling here

    df = np.log2(df)
    df.plot(kind='box', title= title)
    plt.xticks(fontsize=6, rotation=90)
    plt.ylabel('Log2 of Abundances')
    plt.tight_layout()
    box_plot = get_graph()
    return box_plot
