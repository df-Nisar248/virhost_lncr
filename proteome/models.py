from django.db import models
from accounts.models import UserBase
class DataAnalysis(models.Model):
    file = models.FileField(null = True, upload_to='documents/')
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserBase, null = True, on_delete=models.CASCADE)
    resultData = models.FileField(null = True, upload_to='documents/')
    labledData = models.BooleanField(default=False)
    lableFreeData = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Plots(models.Model):
    jobid = models.IntegerField(null = True)
    volcano1 = models.FileField(null = True, upload_to='plots/')
    volcano2 = models.FileField(null = True, upload_to='plots/')
    volcano3 = models.FileField(null = True, upload_to='plots/')
    volcano4 = models.FileField(null = True, upload_to='plots/')
    volcano5 = models.FileField(null = True, upload_to='plots/')
    volcano6 = models.FileField(null = True, upload_to='plots/')
    volcano7 = models.FileField(null = True, upload_to='plots/')
    volcano8 = models.FileField(null = True, upload_to='plots/')
    volcano9 = models.FileField(null = True, upload_to='plots/')
    volcano10 = models.FileField(null = True, upload_to='plots/')
    volcano11 = models.FileField(null = True, upload_to='plots/')
    volcano12 = models.FileField(null = True, upload_to='plots/')
    heatmap = models.FileField(null = True, upload_to='plots/')


class Example(models.Model):
    name = models.CharField(null = True, max_length = 255)
    file = models.FileField(null = True, upload_to='documents/')
    usethis = models.BooleanField(default=True)
    labledData = models.BooleanField(default=False)
    lableFreeData = models.BooleanField(default=False)
    number_of_sample = models.IntegerField(default = 0)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return None

