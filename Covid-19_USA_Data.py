import pandas as pd
import streamlit as st
from PIL import Image
from pathlib import Path
import plotly.express as px

img_path = 'covid19-information-and-updates-serbia-banner.jpg'
url= 'https://raw.githubusercontent.com/prathami1/covid-analysis/main/data/vaccine_data/all-states-history.csv'

@st.cache
def data():
  data = pd.read_csv(url) # use sep="," for coma separation  <and>   use sep="\t"for tab separation. 
  return data

df = data()

st.sidebar.title('COVID-19')
st.sidebar.subheader('All States History, USA')

st.sidebar.markdown(f'##### Number of Rows in the Dataset : {len(df)}  ##### ')


img = Image.open(img_path)
st.image(img)

st.markdown('**Covid** _DataSet form_ **Github**')
st.caption('Data Source >> https://raw.githubusercontent.com/prathami1/covid-analysis/main/data/vaccine_data/all-states-history.csv')

st.subheader('Dataset of first 10 Rows')
st.dataframe(df.head(6))

col = df.columns.tolist()
state = df['state'].unique().tolist()

col_show = st.selectbox('Select Data type from the droplist :', ('All Columns', 'State'))

if col_show == 'All Columns':
  st.caption(f'Total columns : {len(col)}')
  st.write(col)

elif col_show == 'State':
  st.caption(f'Total State : {len(state)}')
  st.write(state)

st.markdown('### Select a State ###')

sel_list =  state

#sel = st.select_slider( 'Select States :', sel_list)
sel = st.select_slider( 'Select States :', sel_list)

st.markdown(f'__ Selected state: __ ** {sel}**')

df_num = df.select_dtypes(['float', 'int'])
df_num_col = df_num.columns

features = st.multiselect('Select features', df_num_col)

def_sel = df[df['state'] == sel]
df_features = def_sel[df_num_col]
df_date = df.iloc[df_features.index, :]

fig = px.line(df_features, 
  x = df_date.index, 
  y = features, 
  title = (f'Number of death in {sel} state'))
st.plotly_chart(fig)
