import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA

df = pd.read_excel('testPCA.xlsx', index_col = "index")
# x = df[['R1','R2','R3']]
pca = PCA(n_components=2)
components = pca.fit_transform(df)


plt.scatter(components[0],components[1])
plt.tight_layout()
plt.show()
