from django.conf import settings
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import os

from . models import DataAnalysis


def normaliz_data(job_id,sample_columns,control_columns):

    data = DataAnalysis.objects.get(id = job_id)
    print(data.file.path)
    df = pd.read_excel(data.file.path)
    print(df.shape)

# https://stackoverflow.com/questions/60448693/input-csv-models-filefield-into-pandas-object

        # filename = os.path.join(settings.MEDIA_ROOT ,dataset.file)
    # df.fillna(0, inplace = True )

# documents/New_Microsoft_Excel_Worksheet_GnpPF3K_iAbIjo3.xlsx
    # mediun_list = []
    # median_df = pd.DataFrame()

    # median_control_1 = df['Abundances (by Bio. Rep.): Cntrol 1'].median()
    # median_control_2 = df['Abundances (by Bio. Rep.): Cntrol 2'].median()
    # median_control_3 = df['Abundances (by Bio. Rep.): Cntrol 3'].median()



    # median_a1 = df['Abundances (by Bio. Rep.): Sample- A1'].median()
    # median_a2 = df['Abundances (by Bio. Rep.): Sample- A2'].median()
    # median_a3 = df['Abundances (by Bio. Rep.): Sample- A3'].median()

    # median_b1 = df['Abundances (by Bio. Rep.): Sample- B1'].median()
    # median_b2 = df['Abundances (by Bio. Rep.): Sample- B2'].median()
    # median_b3 = df['Abundances (by Bio. Rep.): Sample- B3'].median()


    # median_c1 = df['Abundances (by Bio. Rep.): Sample- C1'].median()
    # median_c2 = df['Abundances (by Bio. Rep.): Sample- C2'].median()
    # median_c3 = df['Abundances (by Bio. Rep.): Sample- C3'].median()


    # mediun_list.append([median_control_1, median_control_2, median_control_3, median_a1, median_a2, median_a3,
    #     median_b1,median_b2,median_b3,median_c1,median_c2,median_c3])


    # mediun_list = mediun_list[0]

    # minn = min(mediun_list)
    # mediun_list_new = []

    # for n in mediun_list:
    #     mediun_list_new.append(minn/n)



    # df['normalized_control_1'] = df['Abundances (by Bio. Rep.): Cntrol 1'] * mediun_list_new[0]
    # df['normalized_contorl_2'] = df['Abundances (by Bio. Rep.): Cntrol 2'] * mediun_list_new[1]
    # df['normalized_control_3'] = df['Abundances (by Bio. Rep.): Cntrol 3'] * mediun_list_new[2]

    # df['normalized_sample_a1'] = df['Abundances (by Bio. Rep.): Sample- A1'] * mediun_list_new[3]
    # df['normalized_sample_a2'] = df['Abundances (by Bio. Rep.): Sample- A2'] * mediun_list_new[4]
    # df['normalized_sample_a3'] = df['Abundances (by Bio. Rep.): Sample- A3'] * mediun_list_new[5]

    # df['normalized_sample_b1'] = df['Abundances (by Bio. Rep.): Sample- B1'] * mediun_list_new[6]
    # df['normalized_sample_b2'] = df['Abundances (by Bio. Rep.): Sample- B2'] * mediun_list_new[7]
    # df['normalized_sample_b3'] = df['Abundances (by Bio. Rep.): Sample- B3'] * mediun_list_new[8]


    # df['normalized_sample_c1'] = df['Abundances (by Bio. Rep.): Sample- C1'] * mediun_list_new[9]
    # df['normalized_sample_c2'] = df['Abundances (by Bio. Rep.): Sample- C2'] * mediun_list_new[10]
    # df['normalized_sample_c3'] = df['Abundances (by Bio. Rep.): Sample- C3'] * mediun_list_new[11]

    # df_new = df[['Unique Sequence ID','Protein Group IDs', 'Accession','Description',
    #         'normalized_control_1', 'normalized_contorl_2','normalized_control_3','normalized_sample_a1','normalized_sample_a2',
    #         'normalized_sample_a3','normalized_sample_b1','normalized_sample_b2','normalized_sample_b3',
    #         'normalized_sample_c1','normalized_sample_c2','normalized_sample_c3']]


    # _ ,df_new['p_value_a']= stats.ttest_ind([df_new['normalized_control_1'],df_new['normalized_contorl_2'],df_new['normalized_control_3']],
    #      [df_new['normalized_sample_a1'],df_new['normalized_sample_a2'],df_new['normalized_sample_a3']], equal_var = False )

    # _ ,df_new['p_value_b']= stats.ttest_ind([df_new['normalized_control_1'],df_new['normalized_contorl_2'],df_new['normalized_control_3']],
    #      [df_new['normalized_sample_b1'],df_new['normalized_sample_b2'],df_new['normalized_sample_b3']] , equal_var = False)

    # _ ,df_new['p_value_c']= stats.ttest_ind([df_new['normalized_control_1'],df_new['normalized_contorl_2'],df_new['normalized_control_3']],
    #      [df_new['normalized_sample_c1'],df_new['normalized_sample_c2'],df_new['normalized_sample_c3']], equal_var = False )


    # df_new['average_normalized_A']  = df_new[['normalized_sample_a1','normalized_sample_a2','normalized_sample_a3']].mean( axis = 1)

    # df_new['average_normalized_B']  = df_new[['normalized_sample_b1','normalized_sample_b2','normalized_sample_b3']].mean( axis = 1)

    # df_new['average_normalized_C']  = df_new[['normalized_sample_c1','normalized_sample_c2','normalized_sample_c3']].mean(axis = 1)

    # return df_new
