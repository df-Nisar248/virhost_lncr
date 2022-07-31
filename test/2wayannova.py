import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols


#create data
df = pd.DataFrame({'water': np.repeat(['daily', 'weekly'], 15),
                   'sun': np.tile(np.repeat(['low', 'med', 'high'], 5), 2),
                   'height': [6, 6, 6, 5, 6, 5, 5, 6, 4, 5,
                              6, 6, 7, 8, 7, 3, 4, 4, 4, 5,
                              4, 4, 4, 4, 4, 5, 6, 6, 7, 8]})

df.to_csv('watersun.csv')
# print(df)
model = ols('height ~ sun+ water' data=df).fit()
result = sm.stats.anova_lm(model, type=2)
print(result)
