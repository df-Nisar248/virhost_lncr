from django.db import models

class Remembprot(models.Model):
    idd = models.CharField(max_length = 255,null = True, blank = True )
    name = models.CharField(max_length = 255,null = True, blank = True )
    address = models.CharField(max_length = 255,null = True, blank = True )


    def __str__(self):
        return self.name
