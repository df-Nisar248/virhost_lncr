import statsmodels.api as sm
from statsmodels.formula.api import ols
import pandas as pd

df = pd.read_csv('sampleres.csv')
df_new  = df[['Accession','normalized Abundances (by Bio. Rep.): Cntrol 1', 'normalized Abundances (by Bio. Rep.): Cntrol 2', 'normalized Abundances (by Bio. Rep.): Cntrol 3',
'normalized Abundances (by Bio. Rep.): Sample- A1', 'normalized Abundances (by Bio. Rep.): Sample- A2', 'normalized Abundances (by Bio. Rep.): Sample- A3']]


df_new.columns = ['Accession','c1','c2','c3','a1','a2','a3']

# data = data.rename(columns={"partner.status" :
#                              "partner_status"}) # make name pythonic
# moore_lm = ols('conformity ~ C(fcategory, Sum)*C(partner_status, Sum)',
#                  data=data).fit()

# print(data)
# table = sm.stats.anova_lm(moore_lm, typ=2) # Type 2 Anova DataFrame


model = ols('c1 ~ C(c1,c2,c3):C(a1,a2,a3)', data=df_new).fit()
output  = sm.stats.anova_lm(model, typ=2)
print(output)
