import plotly.express as px
df = px.data.iris()

df.to_csv('irisdatasett.csv')
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                 size='petal_length', hover_data=['petal_width'])
fig.show()
