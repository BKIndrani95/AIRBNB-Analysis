# AIRBNB ANALYSIS
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import pymongo
from streamlit_option_menu import option_menu
import plotly.express as px


st.set_page_config(page_title="AIRBNB ANALYSIS",
                   layout="wide",
                   initial_sidebar_state="expanded")
st.title("AIRBNB ANALYSIS")
st.divider()

with st.sidebar:
    selected=option_menu("Menu",["About","Overview", "Explore"],
                         menu_icon="menu_button_wide",
                         default_index=0,
                         styles={"nav-link":{"font-size":"20px", "text-align":"center", "margin":"1px"},
                                 "nav-link-selected": {"background-color":"#517fc9"}})
df = pd.read_csv(r"C:\Users\HP\Desktop\Master data science\Jupyter\Airbnb.csv", encoding='latin1')
if selected=="About":
   # col1 = st.column #(1,gap='medium')
    #with col1:

    st.markdown(":green[Technologies used]")
    st.write("Python, Pandas, Plotly, Seaborn, Matplotlib, WordCloud, MongoDB, Streamlit, PowerBI")
    st.markdown(":red[About]")
    st.write("This project is Airbnb Analysis. Collecting Data from MongoDB Atlas, Analysed in Jupyter Notebook using python, pandas, seaborn, wordcloud, matplotlib and visualization part was done in PowerBI finally Streamlit used for user interface")
#with col2:
        #col2.image(Image.open(r"C:\Users\HP\Downloads\airbnb.jpeg"), width=200)

if selected == "Overview":
    tab1,tab2 = st.tabs(["Airbnb Data", "Top-Insight"])
    with tab1:
        st.write("##:blue[Airbnb DataFrame]")
        st.write(df)
    with tab2:
        country=st.sidebar.multiselect('Choose a Country',sorted(df.country.unique()), sorted(df.country.unique()))
        proper=st.sidebar.multiselect('Choose a Property Type', sorted(df.property_type.unique()), sorted(df.property_type.unique()))
        room=st.sidebar.multiselect('Choose a Room Type', sorted(df.room_type.unique()), sorted(df.room_type.unique()))
        #avail365=st.sidebar.slider('choose a availablility', sorted(df.availability_365.unique()), sorted(df.availability_365.unique()))
        price=st.sidebar.slider('Choose a Price', df.price.min(), df.price.max(), (df.price.min(),df.price.max()))
        query = f'country in {country} and room_type in {room} and property_type in {proper} and price >={price[0]} and price <={price[1]}'

        col1, col2 = st.columns(2, gap='medium')
        with col1:
            df1 = df.query(query).groupby(['property_type']).size().reset_index(name='price').sort_values(by='price',ascending=False)[:10]
            fig = px.bar(df1,
                         title="price with Property type",
                         x='price',
                         y='property_type',
                         orientation='h',
                         #names="property_type",
                         color_continuous_scale=px.colors.sequential.Rainbow)
            st.plotly_chart(fig,use_container_width=True)

            df2 =df.query(query).groupby('host_name').size().reset_index(name='host_listings_count')
            df2=df2.sort_values(by='host_listings_count',ascending=False)[:10]
            fig = px.bar(df2,
                         title='host with listings',
                         x='host_listings_count',
                         y='host_name',
                         orientation='h',
                         color='host_name',
                         color_continuous_scale='Reds')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            df3 = df.query(query).groupby(['room_type']).size().reset_index(name='counts')
            fig=px.pie(df3,
                       title='listings with room_type',
                       names='room_type',
                       values='counts',
                       color_discrete_sequence=px.colors.sequential.solar)
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig,use_container_width=True)

            country_df=df.query(query).groupby(['country'],as_index=False)['name'].count().rename(columns={'name':'host_listings_count'})
            fig=px.choropleth(country_df,
                              title='listings and country',
                              locations=country,
                              locationmode='country names',
                              color='host_listings_count',
                              color_continuous_scale='Reds')
            st.plotly_chart(fig,use_container_width=True)

if selected =='Explore':
    st.markdown("#Lets Explore the data")
    st.subheader('Histogram of Prices')
    fig, ax = plt.subplots()
    ax.hist(df['price'], bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel('Price ($)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    st.subheader('Room Type Counts')
    room_type_counts = df['room_type'].value_counts()
    fig2, ax2 =plt.subplots()
    ax2.bar(room_type_counts.index, room_type_counts.values, color='orange')
    ax2.set_xlabel('Room Type')
    ax2.set_ylabel('Count')
    ax2.tick_params(axis='x',rotation=45)
    st.pyplot(fig2)
