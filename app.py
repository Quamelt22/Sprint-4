import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('vehicles2_us.csv')
df['date_posted'] = pd.to_datetime(df['date_posted'], format= '%m/%d/%Y')
df['year'] = df['date_posted'].dt.year

st.header('Data Viewer')
st.dataframe(df)

#------------------------------
st.header('Manufactures by years')
st.write("""###### Let's analyze manufactures by year.""")

manufacturers = df['manufacturer'].unique()

make_choice_manu = st.selectbox('Select manufacturer:',manufacturers)


min_year,max_year = int(df['model_year'].min()), int(df['model_year'].max())

year_range = st.slider('Choose Year', value=(min_year, max_year), min_value = min_year, max_value = max_year)

actual_range = list(range(year_range[0], year_range[1] +1))

df.filtered = df[(df['manufacturer']==make_choice_manu) & (df.model_year.isin(list(actual_range)))]
st.table(df.filtered)

#--------------------------

st.header('Price Analysis')
st.write("""###### Let's analyze what influences price the most. Comparing price vs. transmission vs. body type""")


list_for_hist = ['transmission', 'cylinders', 'type','condition']
choice_for_hist = st.selectbox('Split for Price distribution',list_for_hist)
fig1 = px.histogram(df, x='price', color=choice_for_hist)
fig1.update_layout(title="<b> Split of price by {}</b>".format(choice_for_hist))
st.plotly_chart(fig1)


#------------------------------------
#defining age category of the car

df['age']= 2023 - df['model_year']

def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'

df['age_category'] = df['age'].apply(age_category)

st.write("""###### Checking how Price is affected by odometer, condition, fuel type.""")

list_for_scatter = ('odometer', 'condition', 'fuel')

choice_for_scatter= st.selectbox('Price Dependency on', list_for_scatter)
fig2 = px.scatter(df, x='price', y= choice_for_scatter, color ='age_category', hover_data= ['model_year'])

fig2.update_layout("<b> Price vs. {} <b>".format(choice_for_scatter))
st.plotly_chart(fig2)