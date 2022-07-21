import pandas as pd
from plotly.offline import plot
import plotly.express as px
from sklearn.decomposition import PCA

df = pd.read_excel('testPCA.xlsx', index_col = "samples")
# x = df[['R1','R2','R3']]
pca = PCA(n_components=2)
components = pca.fit_transform(df)
fig = px.scatter(components, x=0, y=1,)
fig.show()
