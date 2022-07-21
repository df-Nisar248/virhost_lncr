# from combat.pycombat import pycombat
# import pandas as pd
# import matplotlib.pyplot as plt

# # prepare data
# # the datasets are dataframes where:
#     # the indexes correspond to the gene names
#     # the column names correspond to the sample names
# # Any number (>=2) of datasets can be treated
# dataset_1 = pd.read_pickle("GSE18520.pickle") # datasets can also be stored in csv, tsv, etc files
# dataset_2 = pd.read_pickle("GSE66957.pickle")
# dataset_3 = pd.read_pickle("GSE69428.pickle")

# # we merge all the datasets into one, by keeping the common genes only
# df_expression = pd.concat([dataset_1,dataset_2,dataset_3],join="inner",axis=1)

# batch = []
# datasets = [dataset_1,dataset_2,dataset_3]
# for j in range(len(datasets)):
#     batch.extend([j for _ in range(len(datasets[j].columns))])

# print(df_expression)
# # print(dataset_1)
# # print(batch)
# # plot raw data
# # plt.boxplot(df_expression.transpose())
# # plt.show()
# import pandas as pd

# df = pd.read_table('hipoo.txt')

# print(df.columns)























