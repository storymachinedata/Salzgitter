import re
import json
import datetime as dt
from datetime import datetime
import pandas as pd
import streamlit as st




filters = { 'Total Interaction: High to Low' : ['Total Interactions', False],
            'Total Interaction: Low to High' : ['Total Interactions', True],
            'Posts: Newest First': ['date',False],
            'Posts: Oldest First': ['date',True]}


@st.cache
def load_config(file_path='query_mapper.json'):
    try:
        with open(file_path, 'r') as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        return {}
    

def getActualDate(url):
    a= re.findall(r"\d{19}", url)
    a = int(''.join(a))
    a = format(a, 'b')
    first41chars = a[:41]
    ts = int(first41chars,2)
    actualtime = datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M:%S %Z")
    return actualtime


def display_filters():
    col1, col2, col3 = st.columns(3)

    with col1:
        filter_day = st.number_input("How many days older posts?", min_value=1, max_value=100, value=7, step=1)
        if filter_day:
            st.success(f'Showing Posts from the last {int(filter_day)} Days', icon="✅")

    with col2:
        filter_Interactions = st.selectbox(
            "Filter by total interactions",
            ('Total Interaction: High to Low', 'Total Interaction: Low to High'))

    with col3:
        filter_date = st.selectbox(
            "Filter by total Post date",
            ('Posts: Newest First', 'Posts: Oldest First'))

    return filter_day, filter_Interactions, filter_date


def choice_selector(dataframe,choice='All'):
    if choice == 'All':
        selected_df = dataframe.loc[dataframe['category'] == 'Content']
    else:
        selected_df= dataframe.loc[dataframe['keyword'] == choice]
    
    return selected_df


def filter_and_sort_posts(df, filter_day, filter_Interactions, filter_date):
    filtered_df = df[df['date'] >= (datetime.now() - dt.timedelta(days=filter_day))]

    sorting_columns = ['yy-dd-mm', 'Total Interactions']
    ascending=[ filters[filter_date][1], filters[filter_Interactions][1]]

    sorted_df = filtered_df.sort_values(by=sorting_columns, ascending=ascending)
    sorted_df = sorted_df.reset_index(drop=True)
    
    return sorted_df


@st.cache(ttl=7200)
def load_dataframe(filename):
    df =pd.read_csv(filename)
    df = df.dropna(how='any', subset=['textContent'])

    df.drop(['connectionDegree', 'timestamp'], axis=1, inplace=True)

    if 'companyUrl' in df.columns:
        df['profileUrl'].fillna(df['companyUrl'], inplace=True)
        df['fullName'].fillna(df['companyName'], inplace=True)

    df['title'].fillna(' ', inplace=True)

    df['postDate'] = df.postUrl.apply(getActualDate)
    df = df.dropna(how='any', subset=['postDate'])
    df['date'] =  pd.to_datetime(df['postDate'])

    df.drop_duplicates(subset=['postUrl'], inplace=True)
    df = df.reset_index(drop=True)

    df['Total Interactions'] = df['likeCount'] + df['commentCount']
    df['likeCount'] = df['likeCount'].fillna(0)
    df['commentCount'] = df['commentCount'].fillna(0)
    df['Total Interactions'] = df['Total Interactions'].fillna(0)
    df['likeCount'] = df['likeCount'].astype(int)
    df['commentCount'] = df['commentCount'].astype(int)
    df['Total Interactions'] = df['Total Interactions'].astype(int)

    df['Keyword']  = df['category']
    df['yy-dd-mm'] = pd.to_datetime(df.date).dt.strftime('%Y/%m/%d')

    query_mapper = load_config()
    df['keyword'] =  df['query'].apply(lambda x : query_mapper[x] if x in query_mapper else x)

    return df


def display_info(rows): 
        st.subheader(rows['fullName'])
        st.write(rows['title'])
        st.write('-----------')
        st.info(rows['textContent']) 
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) 
        st.write('Likes 👍:  ',rows['likeCount']) 
        st.write('Comments 💬:  ',rows['commentCount']) 
        st.write('Publish Date & Time 📆:         ',rows['postDate']) 

        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) 
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) 


def display_post_chunks(df_filtered):
    df_filtered.reset_index(drop=True, inplace=True)
    data_chunk = [df_filtered.iloc[i:i+3] for i in range(0, len(df_filtered), 3)]
    
    for data in data_chunk:
        data = data.reset_index(drop=True)
        thumbnails = st.columns(data.shape[0])
        
        for i, row in data.iterrows():
            with thumbnails[i]:
                display_info(row)


