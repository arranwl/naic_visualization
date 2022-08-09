import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('NAIC_Wage_Data_Median2.csv')
gdp = pd.read_csv('GDP_DATA_v3.csv')
gr = pd.read_csv('GROWTH_RATE_v2.csv')
bc = pd.read_csv('BUSINESS_COUNT_v7.csv')
em = pd.read_csv('EMPLOYMENT_V3.csv')

em['NAICS'] = em['NAICS'].str.strip()
bc['Geography'] = bc['Geography'].str.strip()

st.title('NAIC Data Visualization')
st.sidebar.subheader('Select a data element you would like to visualization')

element = st.sidebar.selectbox(label='Select an element', options=['GDP','Growth Rate','Wage', 'Business Count', 'Employment'])

for i in range(3):
    st.text("")

if element == 'Wage':
    #Search and Select input
    ptlist = df['GEO'].drop_duplicates().to_list()
    ptlist.remove('Canada')
    ptlist.insert(0,'Canada')
    province = st.sidebar.selectbox(label='Select a province', options=ptlist)
    sectors = st.sidebar.multiselect(label='Select sectors', options=df['NAICS'].drop_duplicates())

    data = df[df['GEO'] == province]
    data = data[data['NAICS'].isin(sectors)]

    fig, scatter = plt.subplots(figsize = (10,6), dpi = 200)
    scatter = sns.lineplot(x = 'YEAR', y = 'VALUE', data=data, hue='NAICS', ci = None, markers='o')
    scatter.set_title('Wages by Sector by Year', fontsize = 50, y =1.05)
    scatter.set(xlabel='Year', ylabel='Wage ($)')
    scatter.legend(loc=(1,0))
    st.pyplot(fig)
elif element == 'GDP':
    # Search and Select input
    years = st.sidebar.multiselect(label='Select years', options=gdp['YEAR'].drop_duplicates(), default=[2021])

    data = gdp[gdp['YEAR'].isin(years)]
    data = data.sort_values('VALUE')
    data = data[data['NAICS'] != 'All industries  ']

    fig, scatter = plt.subplots(figsize=(12, 10), dpi=200)
    scatter = sns.barplot(x='VALUE', y='NAICS', data=data, hue='YEAR', ci=None)
    scatter.set_title('GDP by Sector by Year', fontsize=50, y=1.05)
    scatter.set(xlabel='GDP (in millions)', ylabel='Sector')
    scatter.legend(loc=(1, 0))
    st.pyplot(fig)
elif element == 'Growth Rate':
    # Search and Select input
    sectors = st.sidebar.multiselect(label='Select sectors', options=gr['NAICS'].drop_duplicates())

    data = gr[gr['NAICS'].isin(sectors)]

    fig, scatter = plt.subplots(figsize=(10, 6), dpi=200)
    scatter = sns.lineplot(x='YEAR', y='VALUE', data=data, hue='NAICS', ci=None, markers='o')
    scatter.set_title('GDP change by Sector by Year', fontsize=50, y=1.05)
    scatter.set_xticklabels([' ','2017',' ','2018',' ','2019',' ','2020',' ','2021'])
    scatter.set(xlabel='Year', ylabel='GDP % Change')
    scatter.legend(loc=(1, 0))
    st.pyplot(fig)
elif element == 'Business Count':
    # Search and Select input
    year = st.sidebar.multiselect(label='Select Year', options=bc['Year'].drop_duplicates().sort_values(ascending=False),
                                  default=[2021])
    pt = st.sidebar.selectbox(label='Select Region', options=bc['variable'].drop_duplicates())
    sizes = st.sidebar.selectbox(label='Select Business Size', options=bc['Size'].drop_duplicates())

    data0 = bc[bc['variable'] == pt]
    data = data0[data0['Size'] == sizes]
    data = data[data['Year'].isin(year)]
    data = data[data['Geography'] != 'Total, all industries']
    data = data.sort_values('value')

    fig, scatter = plt.subplots(figsize=(10, 12), dpi=200)
    scatter = sns.barplot(x='value', y='Geography', hue='Year', data=data, ci=None)
    scatter.set_title('Business Count', fontsize=50, y=1.05)
    #scatter.set_xticklabels([' ','2017',' ','2018',' ','2019',' ','2020',' ','2021'])
    scatter.set(xlabel='Number of Businesses in Sector', ylabel='Sector')
    scatter.legend(loc=(1, 0))
    st.pyplot(fig)
elif element == 'Employment':
    # Search and Select input
    year = st.sidebar.multiselect(label='Select Year',
                                  options=em['YEAR'].drop_duplicates().sort_values(ascending=False),
                                  default=[2021])
    pt = st.sidebar.selectbox(label='Select Region', options=em['GEO'].drop_duplicates())

    data = em[em['GEO'] == pt]
    data = data[data['YEAR'].isin(year)]
    data = data[data['NAICS'] != 'Total, all industries']
    data = data.sort_values('VALUE')
    data = data[~data['VALUE'].isna()]

    fig, scatter = plt.subplots(figsize=(10, 12), dpi=200)
    scatter = sns.barplot(x='VALUE', y='NAICS', hue='YEAR', data=data, ci=None)
    scatter.set_title('Employment Count', fontsize=50, y=1.05)
    scatter.set(xlabel='Number of Employment in Sector (In Thousands)', ylabel='Sector')
    scatter.legend(loc=(1, 0))
    st.pyplot(fig)