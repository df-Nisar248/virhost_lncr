import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from difflib import SequenceMatcher

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, fromat = 'png')
    buffer.seek(0)
    img_png = buffer.getvalue()
    graph = base64.b64encode(img_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x):
    plt.switch_backend('AGG')
    plt.figure(figsize = (10,5))
    plt.title('Abundance of peptides')
    plt.boxplot(x)
    plt.xlabel('Abundance')
    plt.tight_layout()
    graph = get_graph()
    return graph

def abundances(columns):
    abundance_list =  []
    for l in columns:
        l = l.strip()
        if ('Abundances' in l) or ('Abundance' in l):
            abundance_list.append(l)
    abundance_list.sort()
    return abundance_list
    #give option to see all column names also if the name column name may vary

def clean_coulumn_heading(sample_data_columns):

    samples = sample_data_columns.split("SaMpSepeR")

    sample_list = []
    for sample in samples:
        abd_list = []
        abundance = sample.split('RepsepRatTor')
        for abd in abundance:
            abd = abd.strip()
            if abd != '':
                abd_list.append(abd)
        sample_list.append(abd_list)
    final_list = [x for x in sample_list if x != []]
    print(final_list)
    return final_list

def sort_name(samples):
    name = ''
    if len(samples) > 1:
        string1 = samples[0]
        string2 = samples[1]
        match = SequenceMatcher(None, string1,
                        string2).find_longest_match(0, len(string1), 0,
                                                    len(string2))
        name =  string1[match.a:match.a + match.size]

    else:
        name = samples
    if 'Abundances' in name:
        name = name.replace('Abundances','')
    if  'Abundance' in name:
        name = name.replace('Abundance','')
    if  'normalized' in name:
        name = name.replace('normalized','')
    if 'average_normalized' in name:
        name = name.replace('average_normalized','')

    return name

