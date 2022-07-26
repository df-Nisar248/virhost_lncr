from django.conf import settings
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import os
import numpy as np
from . import combat

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
    df = deletemultizero(df,sample_columns,control_columns)
    missing_val = float(missing_val_rep)


    df.fillna(missing_val, inplace = True )

    #for median normalization
    print(df.shape)
    mediun_list = {}

    if (norm_method == 'Median'):

        for controls in control_columns:
            for replicates in controls:
                mediun_list[replicates] = df[replicates].median()

        for samples in sample_columns:
            for samp_replicates in samples:
                mediun_list[samp_replicates] = df[samp_replicates].median()


    elif (norm_method == 'TMM'):

        for controls in control_columns:
            for replicates in controls:
                mediun_list[replicates] = stats.trim_mean(df[replicates], 0.1)

        for samples in sample_columns:
            for samp_replicates in samples:
                mediun_list[samp_replicates] = stats.trim_mean(df[samp_replicates], 0.1)


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


    # df_PCA_before = df_PCA_before.transpose().reset_index()
    # df_PCA_before.set_index('index', inplace=True)
    df_PCA_before['Accession']  = df['Accession']

    df_PCA_before.set_index('Accession', inplace = True)

    df_PCA_after['Accession']  = df['Accession']
    df_PCA_after.set_index('Accession', inplace = True)

    return df,df_PCA_before, df_PCA_after ,cna, sna


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

    df = deletemultizero(df,sample_columns,control_columns)

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

    elif (norm_method == "Quntail"):
        col_list_samp, col_list_cont = expandNCleanColumns(sample_columns,control_columns)

        col_list = col_list_samp + col_list_cont

        df_for_qunt = df[col_list]
        df_for_qunt['Accession'] = df['Accession']
        df_for_qunt.set_index('Accession', inplace = True)
        df_PCA_before = df_for_qunt
        quant_df = quantile_normalize(df_for_qunt)
        col_names = {}
        for columns in quant_df.columns:
            col_names[columns] = "normalized "+columns

        quant_df.rename(columns = col_names, inplace = True)
        df_PCA_after = quant_df
        df = pd.merge(df,quant_df, on = "Accession")

        cna = []
        for controls in control_columns:
            each_control = []
            controls = removeSpaceAndComma(controls)
            for replicates in controls:
                each_control.append('normalized '+replicates)
            cna.append(each_control)


        sna = []
        for samples in sample_columns:
            samples = removeSpaceAndComma(samples)
            each_sample = []
            for samp_replicates in samples:
                each_sample.append('normalized '+samp_replicates)
            sna.append(each_sample)


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

        df_before_bc = df[df_columns_for_bc]
        df_before_bc['Accession'] = df['Accession']

        df_before_bc.set_index('Accession', inplace = True)

        df_after_bc = combat.pycombat(df_before_bc,batch_list)

        return df, df_PCA_before, df_PCA_after, df_before_bc,  df_after_bc , cna, sna




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

    before_norm,after_norm = forPCA(sample_columns,control_columns,sna,cna)

    df_PCA_before = df[before_norm]
    df_PCA_after = df[after_norm]

    df_PCA_before['Accession']  = df ['Accession']
    df_PCA_before.set_index('Accession', inplace = True)

    df_PCA_after['Accession']  = df ['Accession']
    df_PCA_after.set_index('Accession', inplace = True)

    df_before_bc = df[df_columns_for_bc]
    df_before_bc['Accession'] = df['Accession']

    df_before_bc.set_index('Accession', inplace = True)

    # print(batch_list)
    df_after_bc = combat.pycombat(df_before_bc,batch_list)

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


    return df, df_PCA_before, df_PCA_after, df_PCA_before, df_after_bc , cna, sna

def quantile_normalize(df):
    df_sorted = pd.DataFrame(np.sort(df.values,
                                     axis=0),
                             index=df.index,
                             columns=df.columns)
    df_mean = df_sorted.mean(axis=1)
    df_mean.index = np.arange(1, len(df_mean) + 1)
    df_qn =df.rank(method="min").stack().astype(int).map(df_mean).unstack()
    return(df_qn)


def pvalAndRatio(cna,sna,job_id, pvalue):
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

    if islabelled:

        average_normalized_sample_array = []
        average_normalized_control_array = []

        controlcols = []

        for controls in cna:
            for control in controls:
                controlcols.append(control)
        samplecols = []
        for samples in sna:
            for sample in samples:
                controlcols.append(sample)

        foranova = cna + sna
        avrg_norm_array = []

        minuslog10array = list()
        log2fcarray = list()
        for samples in sna:
            df_sample = df[[y for y in samples]]
            #caculating average normalized
            average_normalized_sample_array.append("average_normalized"+sort_name(samples))
            df["average_normalized"+sort_name(samples)] = df_sample.mean(axis = 1)
            avrg_norm_array.append("average_normalized"+sort_name(samples))
            #calculating P value

            if pvalue == 'ttest':
                #T-test
                _,df["P VALUE of"+sort_name(samples)]= stats.ttest_ind(df[controlcols],df_sample,axis=1, equal_var = False)
                df["Minus Log10(PVAL) "+sort_name(samples)] = abs(np.log10(df["P VALUE of"+sort_name(samples)]))
                minuslog10array.append("Minus Log10(PVAL) "+sort_name(samples))
            else:
                #ANOVA
                _,df["P VALUE using One-Way-ANOVA"]= stats.f_oneway(*exapndd(foranova,df), axis = 1)

                df["Minus Log10(PVAL)"] = abs(np.log10(df["P VALUE of"+sort_name(samples)]))

                minuslog10array.append("Minus Log10(PVAL)")


            df["average_normalized_of_CONTROL"] = df[controlcols].mean(axis =1 )


        #calculating foldchange
        foldchange_array = []
        for avg_sample in avrg_norm_array:
            sample_name  = avg_sample.replace("average_normalized" , '')
            foldchange_array.append('FOLDCHANGE of '+ sample_name)
            df['FOLDCHANGE of '+ sample_name ] = df[avg_sample].div(df["average_normalized_of_CONTROL"])

        print(foldchange_array)
        #caluclating log2 of foldchange
        for foldchange in foldchange_array:
            name = foldchange.replace("FOLDCHANGE of ",'')
            df['LOG2 foldchange of'+ name ] = np.log2(df[foldchange])
            log2fcarray.append('LOG2 foldchange of'+ name )

        # forvolcano = df[['Accession','LOG2 foldchange of  (by Bio. Rep.): Sample- A','Minus Log10(PVAL)   (by Bio. Rep.): Sample- A']]
        forvolcano = list()
        i = 0
        for fc in log2fcarray:
            volcano = []
            volcano.append(fc)
            volcano.append(minuslog10array[i])
            i+=1
            volcano.append("Accession")

            forvolcano.append(volcano)

        print(forvolcano)

        forheatmap = df[log2fcarray]
        forheatmap['Accession'] = df['Accession']
        forheatmap.set_index('Accession',inplace = True)
        return df,forvolcano , forheatmap

        # for lablefree data

    else:
        return None

def deletemultizero(df,sample_columns,control_columns):
    sc,cc = expandNCleanColumns(sample_columns,control_columns)
    all_cols = sc+cc
    no_of_repli = 0

    print(df.shape)
    df = df.dropna(how='all', subset=all_cols)
    print(df.shape)

    for sample in sample_columns:
        no_of_repli = len(sample)

    if no_of_repli == 3:
        indices_to_drop = list()
        for index, row in df[sample].iterrows():
            if ( pd.isnull(row[sample[0]])  and (  pd.isnull(row[sample[1]])  or  pd.isnull(row[sample[2]])  )  or ( pd.isnull(row[sample[1]])  and  pd.isnull(row[sample[2]]) )  ):
                indices_to_drop.append(index)
        df.drop(labels=indices_to_drop, inplace=True)

    # if no_of_repli == 2:
    #     indices_to_drop = list()

    return df


def exapndd(foranova,df):
    dflist = []
    for sam in foranova:
        dflist.append(df[sam])
    return dflist
    print(dflist)















