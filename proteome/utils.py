import pandas as pd
from difflib import SequenceMatcher

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


def removeSpaceAndComma(columns):
    cleaned_col = []
    for column in columns:
            if ',' in column:
                column =column.strip()
                column = column.replace(',',' ')
                cleaned_col.append(column)
            else:
                column =column.strip()
                cleaned_col.append(column)

    return cleaned_col

def forPCA(sample_columns,control_columns,sample_normalized_array):
    before_norm = []
    after_norm = []
    for sample_list in sample_columns:
        for sample in sample_list:
            before_norm.append(sample)

    for control_list in control_columns:
        for control in control_list:
            before_norm.append(control)

    for norm_sample_list in sample_normalized_array:
        for sample in norm_sample_list:
            after_norm.append(sample)

    before_norm = removeSpaceAndComma(before_norm)
    after_norm = removeSpaceAndComma(after_norm)
    return before_norm,after_norm


def expandNCleanColumns(sample_columns,control_columns):
    colum_list = []
    for sample_list in sample_columns:
        for sample in sample_list:
            colum_list.append(sample)

    for control_list in control_columns:
        for control in control_list:
            colum_list.append(control)

    colum_list = removeSpaceAndComma(colum_list)

    return colum_list


