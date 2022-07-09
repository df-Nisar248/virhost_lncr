from django.conf import settings
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import os
import numpy as np
from combat.pycombat import pycombat

from . models import DataAnalysis
from . utils import sort_name,removeSpaceAndComma,forPCA,expandNCleanColumns,removeavgsmp

def normaliz_data(job_id,sample_columns,control_columns,norm_method,missing_val_rep):

    data = DataAnalysis.objects.get(id = job_id)
    datafile = data.file.path
    df = pd.DataFrame()

    if (datafile.endswith('.xlsx')):
        df = pd.read_excel(datafile, engine='openpyxl')

    elif(datafile.endswith('.csv')):
        df = pd.read_csv(datafile,)
    else:
        df = pd.read_csv(datafile, delimiter = '\t')

    columns = df.columns

    df.columns = removeSpaceAndComma(columns)

    missing_val = float(missing_val_rep)

    df.fillna(missing_val, inplace = True )

    # df = deletemultizero(df,sample_columns,control_columns)
    #for median normalization
    mediun_list = {}

    if (norm_method == 'Median'):

        for controls in control_columns:
            for replicates in controls:
                mediun_list[replicates] = df[replicates].median()

        for samples in sample_columns:
            for samp_replicates in samples:
                mediun_list[samp_replicates] = df[samp_replicates].median()

    elif (norm_method == 'Sum'):
        for controls in control_columns:
            for replicates in controls:
                mediun_list[replicates] = df[replicates].mean()

        for samples in sample_columns:
            for samp_replicates in samples:
                mediun_list[samp_replicates] = df[samp_replicates].mean()

    elif (norm_method == "Quntail"):
        col_list_samp, col_list_cont = expandNCleanColumns(sample_columns,control_columns)

        col_list = col_list_samp + col_list_cont

        df_for_qunt = df[col_list]
        df_for_qunt['Accession'] = df['Accession']
        df_for_qunt.set_index('Accession', inplace = True)
        df_PCA_before = df_for_qunt
        quant_df = quantile_normalize(df_for_qunt)
        print(quant_df)
        col_names = {}
        for columns in quant_df.columns:
            col_names[columns] = "normalized "+columns

        quant_df.rename(columns = col_names, inplace = True)
        df_PCA_after = quant_df
        df = pd.merge(df,quant_df, on = "Accession")
        cna = []
        sna = []
        for samp in col_list_samp:
            sna.append("normalized "+samp)
        for cntrl in col_list_cont:
            cna.append("normalized "+cntrl)




        return df,df_PCA_before, df_PCA_after , cna, sna

    minn = min(mediun_list.values())

    #deviding each value with multiplication factor
    multiplication_fact_list = {}
    for key,value in mediun_list.items():
        multiplication_fact_list[key] = (minn/value)

    cna = []
    for controls in control_columns:
        each_control = []
        for replicates in controls:
            df['normalized '+replicates] = df[replicates] * multiplication_fact_list[replicates]
            each_control.append('normalized '+replicates)
        cna.append(each_control)


    sna = []
    for samples in sample_columns:
        each_sample = []
        for samp_replicates in samples:
            df['normalized '+samp_replicates] = df[samp_replicates] * multiplication_fact_list[samp_replicates]
            each_sample.append('normalized '+samp_replicates)
        sna.append(each_sample)


    before_norm,after_norm = forPCA(sample_columns,control_columns,sna,cna)


    df_PCA_before = df[before_norm]
    df_PCA_after = df[after_norm]

    df_PCA_before['Accession']  = df ['Accession']
    df_PCA_before.set_index('Accession', inplace = True)

    df_PCA_after['Accession']  = df ['Accession']
    df_PCA_after.set_index('Accession', inplace = True)
    return df,df_PCA_before, df_PCA_after , cna, sna


# normalizing biological rreplicates data
def normaliz_data_bio(job_id,sample_columns,control_columns,norm_method,missing_val_rep):
    data = DataAnalysis.objects.get(id = job_id)
    datafile = data.file.path

    df = pd.DataFrame()
    if (datafile.endswith('.xlsx')):
        df = pd.read_excel(datafile, engine='openpyxl')

    elif(datafile.endswith('.csv')):
        df = pd.read_csv(datafile)
    else:
        df = pd.read_csv(datafile, delimiter = '\t')

    columns = df.columns
    df.columns = removeSpaceAndComma(columns)
    missing_val = float(missing_val_rep)
    df.fillna(missing_val, inplace = True)

    mediun_list = {}

    if (norm_method == 'Median'):

        for controls in control_columns:
            for replicates in controls:
                mediun_list[replicates] = df[replicates].median()

        for samples in sample_columns:
            for samp_replicates in samples:
                mediun_list[samp_replicates] = df[samp_replicates].median()

    elif (norm_method == 'Sum'):
        for controls in control_columns:
            for replicates in controls:
                mediun_list[replicates] = df[replicates].mean()

        for samples in sample_columns:
            for samp_replicates in samples:
                mediun_list[samp_replicates] = df[samp_replicates].mean()


    minn = min(mediun_list.values())

    #deviding each value with multiplication factor
    multiplication_fact_list = {}
    for key,value in mediun_list.items():
        multiplication_fact_list[key] = (minn/value)

    cna = []
    for controls in control_columns:
        each_control = []
        for replicates in controls:
            df['normalized '+replicates] = df[replicates] * multiplication_fact_list[replicates]
            each_control.append('normalized '+replicates)

        cna.append(each_control)



    sna = []
    for samples in sample_columns:
        each_sample = []
        for samp_replicates in samples:
            df['normalized '+samp_replicates] = df[samp_replicates] * multiplication_fact_list[samp_replicates]
            each_sample.append('normalized '+samp_replicates)

        sna.append(each_sample)

    # df_control = df[[y for y in cna]]

    batch_list = []
    df_list_sample = []
    i = 1
    for batch in sna:
        for sample in batch:
            batch_list.append(i)
            df_list_sample.append(sample)
        i +=1

    i = 1
    df_list_control = []
    for batch in cna:
        for control in batch:
            batch_list.append(i)
            df_list_control.append(control)
        i +=1

    df_columns_for_bc = df_list_sample + df_list_control

    before_norm,after_norm = forPCA(sample_columns,control_columns,sna)
    df_PCA_before = df[before_norm]
    df_PCA_before['Accession']  = df ['Accession']
    df_PCA_before.set_index('Accession', inplace = True)


    df_bc = df[df_columns_for_bc]
    df_bc['Accession'] = df['Accession']

    df_bc.set_index('Accession', inplace = True)

    # print(batch_list)
    df_after_bc = pycombat(df_bc,batch_list)

    # average_normalized_sample_array = []

    # for samples in sna:

    #     df_sample = df[[y for y in samples]]
    #     #caculating average normalized
    #     average_normalized_sample_array.append("average_normalized"+sort_name(samples[0]))

    #     df["average_normalized"+sort_name(samples)] = df_sample.mean(axis = 1)
    #     #calculating P value

    #     _ ,df["P VALUE of"+sort_name(samples)]= stats.ttest_ind(df_control,df_sample,axis=1, equal_var = False)

    # df["average_normalized_of_CONTROL"] = df_control.mean(axis =1 )

    # before_norm,after_norm = forPCA(sample_columns,control_columns,sna)
    # df_PCA_before = df[before_norm]
    # df_PCA_after = df[after_norm].join(df_control)


    return df, df_PCA_before, df_after_bc


def quantile_normalize(df):
    df_sorted = pd.DataFrame(np.sort(df.values,
                                     axis=0),
                             index=df.index,
                             columns=df.columns)
    df_mean = df_sorted.mean(axis=1)
    df_mean.index = np.arange(1, len(df_mean) + 1)
    df_qn =df.rank(method="min").stack().astype(int).map(df_mean).unstack()
    df_qn.to_csv('quantiled.csv')
    return(df_qn)

def pvalAndRatio(cna,sna,job_id):
    data = DataAnalysis.objects.get(id = job_id)
    datafile = data.resultData.path
    islabelled  = data.labledData
    df = pd.DataFrame()

    if (datafile.endswith('.xlsx')):
        df = pd.read_excel(datafile, engine='openpyxl')

    elif(datafile.endswith('.csv')):
        df = pd.read_csv(datafile,)
    else:
        df = pd.read_csv(datafile, delimiter = '\t')
    columns = df.columns
    df.columns = removeSpaceAndComma(columns)


    average_normalized_sample_array = []
    average_normalized_control_array = []

    controlcols = []

    for controls in cna:
        for control in controls:
            controlcols.append(control)

    avrg_norm_array = []

    for samples in sna:
        df_sample = df[[y for y in samples]]
        #caculating average normalized
        average_normalized_sample_array.append("average_normalized"+sort_name(samples))
        df["average_normalized"+sort_name(samples)] = df_sample.mean(axis = 1)
        avrg_norm_array.append("average_normalized"+sort_name(samples))
        #calculating P value
        _ ,df["P VALUE of"+sort_name(samples)]= stats.ttest_ind(df[controlcols],df_sample,axis=1, equal_var = False)

    df["average_normalized_of_CONTROL"] = df[controlcols].mean(axis =1 )

    #calculating foldchange
    foldchange_array = []
    print(avrg_norm_array)
    for avg_sample in avrg_norm_array:
        sample_name  = avg_sample.replace("average_normalized" , '')
        foldchange_array.append('FOLDCHANGE of '+ sample_name)
        df['FOLDCHANGE of '+ sample_name ] = df[avg_sample].div(df["average_normalized_of_CONTROL"])

    #caluclating log2 of foldchange
    for foldchange in foldchange_array:
        name = foldchange.replace("FOLDCHANGE of ",'')
        df['LOG2 foldchange of'+ name ] = np.log2(df[foldchange])

    df.to_csv('log2.csv')
    return df

# def deletemultizero(df,sample_columns,control_columns):




























