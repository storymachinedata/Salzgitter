import pandas as pd
import streamlit as st
from datetime import datetime
import re




filters = { 'Total Interaction: High to Low' : ['Total Interactions', False],
            'Total Interaction: Low to High' : ['Total Interactions', True],
            'Posts: Newest First': ['date',False],
            'Posts: Oldest First': ['date',True]}

def getActualDate(url):
    a= re.findall(r"\d{19}", url)
    a = int(''.join(a))
    a = format(a, 'b')
    first41chars = a[:41]
    ts = int(first41chars,2)
    actualtime = datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M:%S %Z")
    return actualtime


def change_linkedin_url(url):
    part_to_replace = "https://www.linkedin.com/feed/update/"

    replacement = "https://www.linkedin.com/embed/feed/update/"

    return url.replace(part_to_replace, replacement)


def read_file(filename):
    df =pd.read_csv(filename)
    df = df.dropna(how='any', subset=['textContent'])
    df.drop(['connectionDegree', 'timestamp'], axis=1, inplace=True)
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
    df['yy-dd-mm'] = pd.to_datetime(df.date).dt.strftime('%Y/%m/%d')

    df  = df[['postUrl','Total Interactions', 'yy-dd-mm' , 'date']]
    df['embed_url'] = df.postUrl.apply(change_linkedin_url)




    
    return df


def embed_post(rows):
    #url = rows['postUrl']
    #st.write(rows['postUrl'])

    #url = change_linkedin_url(url)

    #URL = "https://www.linkedin.com/embed/feed/update/urn:li:activity:7122828272853291009"

    embed_code =f'''<div style="position:relative;overflow:hidden;padding-top:56.25%;">
    <iframe 
    frameborder="0"
    style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
    src={rows.embed_url}
    ></iframe>
    </div>'''

    st.markdown(embed_code, unsafe_allow_html=True)