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
    columns = df.columns

    cleaned_col = []

    for column in columns:
            if ',' in column:
                column =column.strip()
                column = column.replace(',',' ')
                cleaned_col.append(column)
            else:
                column =column.strip()
                cleaned_col.append(column)
    df.columns = cleaned_col

    missing_val = float(missing_val_rep)

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

        average_normalized_sample_array = []
        for samples in sample_normalized_array:

            print(samples)

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





    return df
