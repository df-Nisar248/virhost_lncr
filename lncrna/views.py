from django.shortcuts import render ,redirect
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Lncrna , LncrnaTarget


def home(request):
    viruses = Lncrna.objects.values('stimuli').distinct()
    virus_count = len(viruses)


    host_cell_line_count = Lncrna.objects.values('cell_line').distinct().count()
    lncrna_count = Lncrna.objects.values('lncrna_name').distinct().count()
    context = {'viruses':viruses, 'virus_count':virus_count , 'host_cell_line_count':host_cell_line_count,
    'lncrna_count':lncrna_count,}
    return render(request,'lncrna/home.html',context)


def virus_list(request):
    viruses = Lncrna.objects.values('stimuli').distinct()

    context = {'viruses':viruses}

    return render(request,'lncrna/virus_list.html', context)




def target_list(request):
    targets = LncrnaTarget.objects.values('regulator').distinct()
    context = {'targets':targets}

    return render(request,'lncrna/target_list.html', context)


def virus(request, virus):
    viruses = Lncrna.objects.filter(stimuli = virus)
    sel_virus = virus
    context = {'viruses':viruses,'sel_virus':sel_virus }
    return render(request,'lncrna/viruses.html',context)

def lncraname(request, lncraname):

    lncra = Lncrna.objects.filter(Q(ncbi_gene = lncraname)|Q(ensembl_id =  lncraname) )
    has_ncbi = False
    if lncra.filter(ncbi_gene=lncraname).exists():
        has_ncbi = True
    dis_lncraname = lncraname
    context = {'lncra':lncra,'dis_lncraname':dis_lncraname,'has_ncbi':has_ncbi}
    return render(request,'lncrna/lncra_details.html',context)

def targetdetails(request, regulator):
    lncrnatarget = LncrnaTarget.objects.filter(regulator = regulator)
    dis_regulator = regulator
    context = {'lncrnatarget':lncrnatarget,'dis_regulator':dis_regulator}
    return render(request,'lncrna/target_details.html',context)

def faqs(request):
    return render(request,'lncrna/faqs.html')


def lncrna_list(request):
    p = Paginator(Lncrna.objects.all().order_by('stimuli'), 21)
    page =  request.GET.get('page')
    lncrna_p = p.get_page(page)
    context = {'lncrna_p':lncrna_p}

    return render(request,'lncrna/lncrna_list.html', context)

def searchresult(request):
    q = request.GET.get('q')
    q = q.strip()
    if q != '':
        lncrna_p = Lncrna.objects.filter(
            Q(ensembl_id__icontains = q) |
            Q(ncbi_gene__icontains = q )
            ).order_by('stimuli')

        if len(lncrna_p) > 0:
            context = { 'lncrna_p':lncrna_p , 'q':q}
            return render(request,'lncrna/search_result.html',context)
        else:
            messages.error(request, 'Entered Id is invalid or dose not exist!')
            return redirect('home')
    else:
        messages.error(request, 'Enter ensembl id or NCBI id')
        return redirect('home')

def bquery(request):
    q = request.GET.get('q')
    q = q.strip()
    if q == '':
        messages.error(request, 'Please enter NCBI/ensembl ID')
        return redirect('bquery')

    else:
        q = q.replace(';',' ')
        q = q.replace(',',' ')
        id = q.split()
        if len(id) > 150:
            messages.error(request, 'Please enter maximum 100 ids')
            return redirect('bquery')

        lncra = Lncrna.objects.filter(
            Q(ncbi_gene__in = id)|
            Q(ensembl_id__in = id)
            )
        if len(lncra) > 0:
            context = {'lncra':lncra}
            return render(request,'lncrna/bquery_result.html',context)
        else:
            messages.error(request, 'Entered Id is invalid or does not exist!')
            return redirect('bquery')
