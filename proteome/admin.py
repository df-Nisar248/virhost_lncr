from django.contrib import admin
from . models import DataAnalysis , Example

@admin.register(DataAnalysis)
class DataAnalysisAdmin(admin.ModelAdmin):
    list_display = ['user','created']


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    pass
