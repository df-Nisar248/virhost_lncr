from combat.pycombat import pycombat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_excel('test.xlsx',index_col = 'Accession')

print()
batch = [1,1,1,2,2,2]

df_corrected = pycombat(df,batch)

print(df_corrected)
df_corrected.to_excel('result.xlsx')
