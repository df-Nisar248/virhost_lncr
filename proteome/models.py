from django.db import models
from accounts.models import UserBase
class DataAnalysis(models.Model):
    file = models.FileField(null = True, upload_to='documents/')
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserBase, null = True, on_delete=models.CASCADE)
    resultData = models.FileField(null = True, upload_to='documents/')


    def __str__(self):
        return str(self.user)
