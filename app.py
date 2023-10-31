import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('vehicles2_us.csv')
df['date_posted'] = pd.to_datetime(df['date_posted'], format= '%m/%d/%Y')
df['year'] = df['date_posted'].dt.year

st.header('Data Viewer')
st.dataframe(df)

manufacturers = df['manufacturer'].unique()

make_choice_manu = st.selectbox('Select manufacturer:',manufacturers)


min_year,max_year = int(df['model_year'].min()), int(df['model_year'].max())

year_range = st.slider('Choose Year', value=(min_year, max_year), min_value = min_year, max_value = max_year)

actual_range = list(range(year_range[0], year_range[1] +1))


df.filtered = df[df['manufacturer']==make_choice_manu] & (df.model_year.isin(list(actual_range)))
st.table(df.filtered)

#--------------------------

st.header('Price Analysis')
st.write("""###### Let's analyze what influences price the most. Comparing price vs. transmission vs. body type""")


list_for_hist = ['transmission', 'cylinder', 'type','condition']
choice_for_hist = st.selectbox('Split for Price distribution',list_for_hist)
fig1 = px.histogram(df, x='price', color=choice_for_hist)
fig1.update_layout(title="<b> Split of price by {}</b>".format(choice_for_hist))
st.plotly_chart(fig1)
