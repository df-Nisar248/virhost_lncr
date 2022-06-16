from django.conf import settings
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import os

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

        control_array = []
        for controls in control_columns:
            for replicates in controls:
                control_array.append('normalized '+replicates)
                df['normalized '+replicates] = df[replicates] * multiplication_fact_list[replicates]


        sample_array = []
        for samples in sample_columns:
            for samp_replicates in samples:
                sample_array.append('normalized '+samp_replicates)
                df['normalized '+samp_replicates] = df[samp_replicates] * multiplication_fact_list[samp_replicates]

# ------------------------------------------ask them what column to select and what to ignore------------------------------------------------------------
    # df_new = df[['Unique Sequence ID','Protein Group IDs', 'Accession','Description',
    #         'normalized_control_1', 'normalized_contorl_2','normalized_control_3','normalized_sample_a1','normalized_sample_a2',
    #         'normalized_sample_a3','normalized_sample_b1','normalized_sample_b2','normalized_sample_b3',
    #         'normalized_sample_c1','normalized_sample_c2','normalized_sample_c3']]
# -------------------------------------------------------------------------------------------------------------------


        for samples in sample_columns:

            _ ,df["P VALUE of "sort_name(samples)]= stats.ttest_ind([df[x for x in control_array]],
                [df[x for x in control_array]], equal_var = False )

    # _ ,df_new['p_value_b']= stats.ttest_ind([df_new['normalized_control_1'],df_new['normalized_contorl_2'],df_new['normalized_control_3']],
    #      [df_new['normalized_sample_b1'],df_new['normalized_sample_b2'],df_new['normalized_sample_b3']] , equal_var = False)

    # _ ,df_new['p_value_c']= stats.ttest_ind([df_new['normalized_control_1'],df_new['normalized_contorl_2'],df_new['normalized_control_3']],
    #      [df_new['normalized_sample_c1'],df_new['normalized_sample_c2'],df_new['normalized_sample_c3']], equal_var = False )


    # df_new['average_normalized_A']  = df_new[['normalized_sample_a1','normalized_sample_a2','normalized_sample_a3']].mean( axis = 1)

    # df_new['average_normalized_B']  = df_new[['normalized_sample_b1','normalized_sample_b2','normalized_sample_b3']].mean( axis = 1)

    # df_new['average_normalized_C']  = df_new[['normalized_sample_c1','normalized_sample_c2','normalized_sample_c3']].mean(axis = 1)

    # return df_new
