from django.contrib import admin
from . models import DataAnalysis , Example, Plots

@admin.register(DataAnalysis)
class DataAnalysisAdmin(admin.ModelAdmin):
    list_display = ['user','created']


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    pass


@admin.register(Plots)
class PlotsAdmin(admin.ModelAdmin):
    pass
