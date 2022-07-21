from django.db import models

class Remembprot(models.Model):
    pmid = models.CharField(max_length = 255,null = True, blank = True )
    author = models.CharField(max_length = 255,null = True, blank = True )
    paper = models.CharField(max_length = 255,null = True, blank = True )
    organism = models.CharField(max_length = 255,null = True, blank = True )
    CellOrtissue = models.CharField(max_length = 255,null = True, blank = True )
    disease = models.CharField(max_length = 255,null = True, blank = True )
    author = models.CharField(max_length = 255,null = True, blank = True )
    paper = models.CharField(max_length = 255,null = True, blank = True )
    organism = models.CharField(max_length = 255,null = True, blank = True )
    profileOrDifex = models.CharField(max_length = 20,null = True, blank = True )
    contxtOfIdent = models.CharField(max_length = 20,null = True, blank = True )
    contxtOfDiferentialREG = models.CharField(max_length = 20,null = True, blank = True )
    test = models.CharField(max_length = 255,null = True, blank = True )
    control = models.CharField(max_length = 255,null = True, blank = True )
    foldchange = models.CharField(max_length = 255,null = True, blank = True )
    expression = models.CharField(max_length = 255,null = True, blank = True )
    protienExtractMethod = models.CharField(max_length = 255,null = True, blank = True )
    geneSymbol = models.CharField(max_length = 255,null = True, blank = True )
    geneID = models.CharField(max_length = 255,null = True, blank = True )
    ontology = models.CharField(max_length = 255,null = True, blank = True )
    membraneType = models.CharField(max_length = 255,null = True, blank = True )
    peripheral = models.CharField(max_length = 255,null = True, blank = True )
    refSeq  = models.CharField(max_length = 255,null = True, blank = True )
    predictedTmh = models.CharField(max_length = 255,null = True, blank = True )
    isTrans = models.CharField(max_length = 255,null = True, blank = True )


    def __str__(self):
        return self.geneID

# Index(['PMID', 'Author', 'Title of the paper', 'Organism', 'Cell/tissue',
#        'Disease', 'Profile and/or differential expression',
#        'Context of identification', 'Context of differential regulation',
#        'Test', 'Control', 'Fold change', 'Expression',
#        'Method of protein extraction', 'Membrane protein Gene symbol',
#        'Entrez Gene ID', 'Ontology', 'Transmembrane ', 'Membrane type',
#        'Peripheral', 'Gene ID', 'RefSeq Protein Accession',
#        'Number of predicted TMHs', 'is it Transmembrane'],
#       dtype='object')
