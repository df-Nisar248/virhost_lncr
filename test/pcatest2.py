from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from plotly.offline import plot
import plotly.express as px

df = pd.read_excel('afternorm.xlsx')

dfc = df[['normalized Abundances (by Bio. Rep.): Cntrol 1','normalized Abundances (by Bio. Rep.): Cntrol 2','normalized Abundances (by Bio. Rep.): Cntrol 3','Accession']]
dfx = df[['normalized Abundances (by Bio. Rep.): Sample- A1','normalized Abundances (by Bio. Rep.): Sample- A2','normalized Abundances (by Bio. Rep.): Sample- A3','Accession']]

dfy = df[['normalized Abundances (by Bio. Rep.): Sample- B1','normalized Abundances (by Bio. Rep.): Sample- B2','normalized Abundances (by Bio. Rep.): Sample- B3','Accession']]

dfz = df[['normalized Abundances (by Bio. Rep.): Sample- C1','normalized Abundances (by Bio. Rep.): Sample- C2','normalized Abundances (by Bio. Rep.): Sample- C3', 'Accession']]

dfc['sample'] = "control"
dfx['sample'] = "sampleA"
dfy['sample'] = "sampleB"
dfz['sample'] = "sampleC"


dfc.columns = ['R1','R2','R3','Accession','sample']
dfx.columns = ['R1','R2','R3','Accession','sample']
dfy.columns = ['R1','R2','R3','Accession','sample']
dfz.columns = ['R1','R2','R3','Accession','sample']

frames = [dfc, dfx, dfy, dfz]

result = pd.concat(frames)
result.set_index('Accession', inplace = True)
result.to_csv('afternromenorm.csv')

print(result)
