from django.conf import settings
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import os
import numpy as np
from combat.pycombat import pycombat

from . models import DataAnalysis
from . utils import sort_name,removeSpaceAndComma,forPCA,expandNCleanColumns

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
        col_list = expandNCleanColumns(sample_columns,control_columns)
        df_for_qunt = df[col_list]
        df_for_qunt['Accession'] = df['Accession']
        df_for_qunt.set_index('Accession', inplace = True)
        quant_df = quantile_normalize(df_for_qunt)

        print(quant_df)


    minn = min(mediun_list.values())

    #deviding each value with multiplication factor
    multiplication_fact_list = {}
    for key,value in mediun_list.items():
        multiplication_fact_list[key] = (minn/value)

    control_norm_array = []
    for controls in control_columns:
        for replicates in controls:
            df['normalized '+replicates] = df[replicates] * multiplication_fact_list[replicates]
            control_norm_array.append('normalized '+replicates)

    sample_normalized_array = []
    for samples in sample_columns:
        each_sample = []
        for samp_replicates in samples:
            df['normalized '+samp_replicates] = df[samp_replicates] * multiplication_fact_list[samp_replicates]
            each_sample.append('normalized '+samp_replicates)
        sample_normalized_array.append(each_sample)

    df_control = df[[y for y in control_norm_array]]
    average_normalized_sample_array = []

    for samples in sample_normalized_array:
        df_sample = df[[y for y in samples]]
        #caculating average normalized
        average_normalized_sample_array.append("average_normalized"+sort_name(samples))

        df["average_normalized"+sort_name(samples)] = df_sample.mean(axis = 1)
        #calculating P value

        _ ,df["P VALUE of"+sort_name(samples)]= stats.ttest_ind(df_control,df_sample,axis=1, equal_var = False)

    df["average_normalized_of_CONTROL"] = df_control.mean(axis =1 )

    #calculating foldchange
    # for avg_sample in average_normalized_sample_array:
    #     df['FOLDCHANGE of '+sort_name(avg_sample)] = df["average_normalized_of_CONTROL"] / df
    # # print(df["average_normalized_of_CONTROL"])

    # df.to_csv("withPval.csv")

    before_norm,after_norm = forPCA(sample_columns,control_columns,sample_normalized_array)
    df_PCA_before = df[before_norm]
    df_PCA_before['Accession']  = df ['Accession']
    df_PCA_before.set_index('Accession', inplace = True)
    df_PCA_after = df[after_norm].join(df_control)

    df_PCA_after['Accession']  = df ['Accession']
    df_PCA_after.set_index('Accession', inplace = True)
    return df, df_PCA_before, df_PCA_after


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

    control_norm_array = []
    for controls in control_columns:
        each_control = []
        for replicates in controls:
            df['normalized '+replicates] = df[replicates] * multiplication_fact_list[replicates]
            each_control.append('normalized '+replicates)

        control_norm_array.append(each_control)



    sample_normalized_array = []
    for samples in sample_columns:
        each_sample = []
        for samp_replicates in samples:
            df['normalized '+samp_replicates] = df[samp_replicates] * multiplication_fact_list[samp_replicates]
            each_sample.append('normalized '+samp_replicates)

        sample_normalized_array.append(each_sample)

    # df_control = df[[y for y in control_norm_array]]

    batch_list = []
    df_list_sample = []
    i = 1
    for batch in sample_normalized_array:
        for sample in batch:
            batch_list.append(i)
            df_list_sample.append(sample)
        i +=1

    i = 1
    df_list_control = []
    for batch in control_norm_array:
        for control in batch:
            batch_list.append(i)
            df_list_control.append(control)
        i +=1

    df_columns_for_bc = df_list_sample + df_list_control
    print(batch_list)
    print(df_columns_for_bc)


    before_norm,after_norm = forPCA(sample_columns,control_columns,sample_normalized_array)
    df_PCA_before = df[before_norm]
    df_PCA_before['Accession']  = df ['Accession']
    df_PCA_before.set_index('Accession', inplace = True)

    print(df_PCA_before)

    df_bc = df[df_columns_for_bc]
    df_bc['Accession'] = df['Accession']

    df_bc.set_index('Accession', inplace = True)

    # print(batch_list)
    df_after_bc = pycombat(df_bc,batch_list)

    # average_normalized_sample_array = []

    # for samples in sample_normalized_array:

    #     df_sample = df[[y for y in samples]]
    #     #caculating average normalized
    #     average_normalized_sample_array.append("average_normalized"+sort_name(samples[0]))

    #     df["average_normalized"+sort_name(samples)] = df_sample.mean(axis = 1)
    #     #calculating P value

    #     _ ,df["P VALUE of"+sort_name(samples)]= stats.ttest_ind(df_control,df_sample,axis=1, equal_var = False)

    # df["average_normalized_of_CONTROL"] = df_control.mean(axis =1 )

    # before_norm,after_norm = forPCA(sample_columns,control_columns,sample_normalized_array)
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
    return(df_qn)
