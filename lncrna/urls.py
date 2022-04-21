from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
path('',views.home, name = 'home'),
path('virus_list/', views.virus_list, name = 'virus_list'),
path('lncrna_list/', views.lncrna_list, name = 'lncrna_list'),
path('target_list/', views.target_list, name = 'target_list'),

path('virus_details/<str:virus>/',views.virus, name = 'virus'),
path('rnadetials/<str:lncraname>/', views.lncraname, name = 'lncraname'),
path('targetdetails/<str:regulator>/', views.targetdetails, name = 'targetdetails'),
path('FAQs/',views.faqs, name = 'faqs'),
path('search/',views.searchresult, name = 'search'),
path('bquery/',TemplateView.as_view(template_name="lncrna/bquery.html"), name='bquery'),
path('bquerysearch/',views.bquery, name = 'bquerysearch'),
]
