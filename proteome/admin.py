from django.contrib import admin
from . models import DataAnalysis

@admin.register(DataAnalysis)
class DataAnalysisAdmin(admin.ModelAdmin):
    list_display = ['user','created']
