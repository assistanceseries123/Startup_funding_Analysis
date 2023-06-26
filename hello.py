import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

df = pd.read_csv('startup_cleaned.csv')
# df['Investors Name']=df['investors'].fillna('Undisclosed')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
st.set_page_config(layout='wide', page_title='Startup Analysis')


# st.dataframe(df)

def load_satrtup_analysis(startup):
    st.title(startup)
    st.subheader('Industry Type')
    temp = df[df['startup'].str.contains(startup)].groupby('startup')['vertical'].count()
    st.dataframe(temp)
    # fig7,ax7=plt.subplots()
    # ax7.bar(temp.index,temp.values)
    # st.pyplot(fig7)

    st.subheader('Total available startup')
    num = df['startup'].count()

    st.metric('Total Startup', num)


def show_overall_analysis():
    st.title('Overall Analysis')
    # total invested amount
    total = round(df['amount'].sum())
    # maximum amount infused in the startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg_funding for the indian startup
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total Amount', str(total) + ' Cr')
    with col2:
        st.metric('Max Amount', str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg amount', str(round(avg_funding)) + ' Cr')
    with col4:
        st.metric('Funded Startups', num_startups)

    st.header('MOM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':

        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype(str) + '_' + temp_df['year'].astype(str)
    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig6)


def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investment of the investors
    last_5 = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last_5)
    # loading the biggest investment of the investor
    col1, col2 = st.columns(2)
    with col1:
        big_df = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False)
        st.subheader('Biggest Investement')
        # st.dataframe(big_df)
        fig, ax = plt.subplots()
        ax.bar(big_df.index, big_df.values)
        st.pyplot(fig)
    with col2:
        sector_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(
            ascending=False)
        st.subheader('Sector Investment')
        fig1, ax1 = plt.subplots()
        ax1.pie(sector_series, labels=sector_series.index, autopct='%0.01f%%')
        st.pyplot(fig1)
    col3, col4 = st.columns(2)
    with col3:
        stage_invest = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(
            ascending=False)
        st.subheader('Stage of the investment')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_invest, labels=stage_invest.index)
        st.pyplot(fig2)
    with col4:
        city_invest = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(
            ascending=False)
        st.subheader("The city where the investor has been invested")
        fig3, ax3 = plt.subplots()
        ax3.pie(city_invest, labels=city_invest.index)
        st.pyplot(fig3)

    yoy_invest = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader("YOY Investment")
    fig4, ax4 = plt.subplots()
    ax4.plot(yoy_invest.index, yoy_invest.values)
    st.pyplot(fig4)


st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])
if option == 'Overall Analysis':
    # st.title('Overall Analysis')
    # btn0=st.sidebar.button('Show Overall Analysis')
    # if btn0:
    show_overall_analysis()
elif option == 'Startup':
    st.title('Startup Analysis')
    startup_option = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find startup details')
    if btn1:
        load_satrtup_analysis(startup_option)
else:
    st.title('Investor Analysis')
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find investor details')
    if btn2:
        load_investor_details(selected_investor)
