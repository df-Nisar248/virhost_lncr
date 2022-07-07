from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'proteome'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('input/', views.input, name = 'input'),
    path('inputfile/', views.inputf, name='inputfile'),
    path('download<int:job_id>',views.downloadfile, name='download_file'),
    path('unlabelled/',TemplateView.as_view(template_name='proteome/unlabelled.html'), name='unlabelled'),
    path('labelled/',TemplateView.as_view(template_name='proteome/labelled.html'), name='labelled'),
    path('pre_process/',views.pre_process, name='pre_process'),
    path('analaze_cols/',views.analaze_cols, name = 'analaze_cols'),
    path('analaze_cols_bio/',views.analaze_cols_bio, name = 'analaze_cols_bio'),
    path('pvalue/',views.pvalues, name = 'pvalues')

]

