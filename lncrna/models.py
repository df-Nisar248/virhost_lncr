from django.db import models

class Lncrna(models.Model):
    stimuli = models.CharField(max_length = 255)
    dosage = models.CharField(max_length = 255)
    time_point = models.CharField(max_length = 50 )
    experiment_type = models.CharField( max_length = 200)
    cell_line = models.CharField(max_length = 255)
    lncrna_name = models.CharField(max_length = 255)
    ncbi_gene = models.CharField(max_length = 255 , null = True, blank = True )
    ensembl_id = models.CharField(max_length = 255, null = True, blank = True )
    foldchange = models.CharField( max_length = 255, null = True, blank = True )
    expression = models.CharField(max_length = 50)
    pubmed_id = models.CharField(max_length = 50, null = True , blank = True)
    reference = models.CharField(max_length = 255, null = True, blank = True)

    # class meta:
    #     ordering = ('-lncrna_name',)

    def __str__(self):
        return self.stimuli



class LncrnaTarget(models.Model):
    regulator = models.CharField(max_length=255)
    target = models.CharField(max_length = 255)
    regulatory_mech = models.CharField(max_length = 255 , null = True, blank = True)
    regulatory_type = models.CharField(max_length = 255 , null = True, blank = True)
    Target_type = models.CharField(max_length = 255 , null = True, blank = True)
    regulator_ensemble_id = models.CharField(max_length = 255 , null = True, blank = True)


    def __str__(self):
        return self.regulator


class Files(models.Model):
    mailfile = models.FileField(null = True, upload_to='documents/')
    target = models.FileField(null = True, upload_to='documents/')
