from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from plotly.offline import plot
import plotly.express as px
plt.style.use('seaborn')

df = pd.read_csv('afternromenorm.csv')
df_for_pca = df[['R1','R2','R3']]

# df_for_pca['R1'] = np.log2(df_for_pca['R1'])
# df_for_pca['R2'] = np.log2(df_for_pca['R2'])
# df_for_pca['R3'] = np.log2(df_for_pca['R3'])


pca = PCA(n_components=2)
components = pca.fit_transform(df_for_pca)
print(components)
df_PCA = pd.DataFrame(components,columns = ['x','y'])

df_PCA['sample'] = df['sample']

# df_PCA.to_csv('transformed.csv')
pcafig_after = px.scatter(df_PCA, x = df_PCA['x'], y= df_PCA['y'], color = df_PCA['sample'] )
pcafig_after.show()

