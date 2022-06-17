from django.conf import settings
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import os
import numpy as np

from . models import DataAnalysis
from . utils import sort_name

def normaliz_data(job_id,sample_columns,control_columns,norm_method,missing_val_rep):

    data = DataAnalysis.objects.get(id = job_id)
    df = pd.read_excel(data.file.path)
    missing_val = int(missing_val_rep)
    df.fillna(missing_val, inplace = True )

    #for median normalization
    if (norm_method == 'Median'):
        mediun_list = {}

        for controls in control_columns:
            for replicates in controls:
                mediun_list[replicates] = df[replicates].median()

        for samples in sample_columns:
            for samp_replicates in samples:
                mediun_list[samp_replicates] = df[samp_replicates].median()

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
        for samples in sample_normalized_array:
            #caculating average normalized
            df["average_normalized"+sort_name(samples)] = df.groupby(x for x in sample_normalized_array).mean(axis = 1)
            #calculating P value
            df_sample = df[[y for y in samples]]
            _ ,df["P VALUE of"+sort_name(samples)]= stats.ttest_ind(df_control,df_sample,axis=1, equal_var = False)

        print(df)

        df.to_csv("withPval.csv")



    # df_new['average_normalized_A']  = df_new[['normalized_sample_a1','normalized_sample_a2','normalized_sample_a3']].mean( axis = 1)

    # df_new['average_normalized_B']  = df_new[['normalized_sample_b1','normalized_sample_b2','normalized_sample_b3']].mean( axis = 1)

    # df_new['average_normalized_C']  = df_new[['normalized_sample_c1','normalized_sample_c2','normalized_sample_c3']].mean(axis = 1)

    # return df_new
