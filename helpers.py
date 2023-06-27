import pandas as pd
import streamlit as st
from datetime import datetime
import re





month = datetime.today().month
day = datetime.today().day



storymch_logo = "https://storymachine.mocoapp.com/objects/accounts/a201d12e-6005-447a-b7d4-a647e88e2a4a/logo/b562c681943219ea.png"


filters = { 'Total Interaction: High to Low' : ['Total Interactions', False],
            'Total Interaction: Low to High' : ['Total Interactions', True],
            'Posts: Newest First': ['date',False],
            'Posts: Oldest First': ['date',True]}


mapper = { 'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=gr%C3%BCner%20Stahl&origin=FACETED_SEARCH&sid=rN7&sortBy=%22date_posted%22' : 'Grüner Stahl' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=green%20steel&origin=GLOBAL_SEARCH_HEADER&sid=Rk7&sortBy=%22date_posted%22' : 'Green Steel' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=salzgitter%20ag&origin=FACETED_SEARCH&sid=xw)&sortBy=%22date_posted%22' : 'Salzgitter AG' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Direktredduktionsanlage&origin=GLOBAL_SEARCH_HEADER&sid=wRU&sortBy=%22date_posted%22' : 'Direktredduktionsanlage' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Salcos&origin=GLOBAL_SEARCH_HEADER&sid=f((&sortBy=%22date_posted%22' : 'Salcos' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Elektrolichtbogenofen&origin=GLOBAL_SEARCH_HEADER&sid=F4z&sortBy=%22date_posted%22' : 'Elektrolichtbogenofen' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=gr%C3%BCner%20Wasserstoff&origin=GLOBAL_SEARCH_HEADER&sid=rrd&sortBy=%22date_posted%22' : 'Grüner Wasserstoff' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=industrielle%20Transformation&origin=GLOBAL_SEARCH_HEADER&sid=vUP&sortBy=%22date_posted%22' : 'Industrielle Transformation' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Stahlstandort%20Deutschland&origin=GLOBAL_SEARCH_HEADER&sid=%3BiW&sortBy=%22date_posted%22' : 'Stahlstandort Deutschland' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Wasserstoffwirtschaft&origin=GLOBAL_SEARCH_HEADER&sid=A8O&sortBy=%22date_posted%22' : 'Wasserstoffwirtschaft' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=industrielle%20Dekarbonisierung&origin=GLOBAL_SEARCH_HEADER&sid=5Lc&sortBy=%22date_posted%22' : 'Industrielle Dekarbonisierung' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Eisenschwamm%20&origin=GLOBAL_SEARCH_HEADER&sid=c0H&sortBy=%22date_posted%22' : 'Eisenschwamm' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Stahlschrott&origin=GLOBAL_SEARCH_HEADER&sid=QpL&sortBy=%22date_posted%22' : 'Stahlschrott' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Schrottrecycling%20&origin=GLOBAL_SEARCH_HEADER&sid=wG8&sortBy=%22date_posted%22' : 'Schrottrecycling' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Circular%20Economy%20&origin=GLOBAL_SEARCH_HEADER&sid=*D%40&sortBy=%22date_posted%22' : 'Circular Economy' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Circularity&origin=GLOBAL_SEARCH_HEADER&sid=~zu&sortBy=%22date_posted%22' : 'Circularity',
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=co2-armer%20Stahl%20&origin=GLOBAL_SEARCH_HEADER&sid=W2h&sortBy=%22date_posted%22':'CO2-Armer Stahl',
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=klimaneutraler%20stahl%20&origin=GLOBAL_SEARCH_HEADER&sid=z(.&sortBy=%22date_posted%22' : 'Klimaneutraler Stahl' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Scope%203%20&origin=GLOBAL_SEARCH_HEADER&sid=1Af&sortBy=%22date_posted%22' : 'Scope 3',
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Gunnar%20Groebler&origin=GLOBAL_SEARCH_HEADER&sid=eP2&sortBy=%22date_posted%22':'Gunnar Groebler'

            }


discarded_profiles = []

def read_file(filename):
    df =pd.read_csv(filename)
    df = df.dropna(how='any', subset=['textContent'])
    df.drop(['connectionDegree', 'timestamp'], axis=1, inplace=True)

    df = df[~df['profileUrl'].isin(discarded_profiles)]
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

    df['keyword'] =  df['query'].apply(lambda x : mapper[x])

    
    return df




def read_file_sp(filename):
    df =pd.read_csv(filename)
    df = df.dropna(how='any', subset=['postContent'])
    # df.drop(['error', 'timestamp', 'sharedPostUrl','sharedPostProfileUrl',
    #         'sharedJobUrl','videoUrl','sharedPostCompanyUrl'], axis=1, inplace=True)

    df['postDate'] = df.postUrl.apply(getActualDate)
    df = df.dropna(how='any', subset=['postDate'])
    df['date'] =  pd.to_datetime(df['postDate'])

    df['company_name'] =  df.profileUrl.apply(lambda x : mapper[x])
    

    df.drop_duplicates(subset=['postUrl'], inplace=True)
    df = df.reset_index(drop=True)
    df['Total Interactions'] = df['likeCount'] + df['commentCount']
    df['likeCount'] = df['likeCount'].fillna(0)
    df['commentCount'] = df['commentCount'].fillna(0)
    df['Total Interactions'] = df['Total Interactions'].fillna(0)
    df['likeCount'] = df['likeCount'].astype(int)
    df['commentCount'] = df['commentCount'].astype(int)
    df['Total Interactions'] = df['Total Interactions'].astype(int)
    #df['Keyword']  = df['category']
    df['yy-dd-mm'] = pd.to_datetime(df.date).dt.strftime('%Y/%m/%d')
    
    return df


def read_file_account(filename):
    df =pd.read_csv(filename)
    df = df.dropna(how='any', subset=['postContent'])
    # df.drop(['error', 'timestamp', 'sharedPostUrl','sharedPostProfileUrl',
    #         'sharedJobUrl','videoUrl','sharedPostCompanyUrl'], axis=1, inplace=True)

    df['postDate'] = df.postUrl.apply(getActualDate)
    df = df.dropna(how='any', subset=['postDate'])
    df['date'] =  pd.to_datetime(df['postDate'])

    #df['company_name'] =  df.profileUrl.apply(lambda x : mapper[x])
    

    df.drop_duplicates(subset=['postUrl'], inplace=True)
    df = df.reset_index(drop=True)
    df['Total Interactions'] = df['likeCount'] + df['commentCount']
    df['likeCount'] = df['likeCount'].fillna(0)
    df['commentCount'] = df['commentCount'].fillna(0)
    df['Total Interactions'] = df['Total Interactions'].fillna(0)
    df['likeCount'] = df['likeCount'].astype(int)
    df['commentCount'] = df['commentCount'].astype(int)
    df['Total Interactions'] = df['Total Interactions'].astype(int)
    #df['Keyword']  = df['category']
    df['yy-dd-mm'] = pd.to_datetime(df.date).dt.strftime('%Y/%m/%d')
    
    return df



def getActualDate(url):
    a= re.findall(r"\d{19}", url)
    a = int(''.join(a))
    a = format(a, 'b')
    first41chars = a[:41]
    ts = int(first41chars,2)
    actualtime = datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M:%S %Z")
    return actualtime



def printFunction(i, rows, dataframe):
   
    if not pd.isnull(rows['companyUrl']):
        st.subheader(rows.companyName)
        st.write('Company Account')
      
        st.info(rows['textContent'])
        st.write('Total Interactions 📈:  ',rows['Total Interactions'])
        st.write('Likes 👍:  ',rows['likeCount']) 
        st.write('Comments 💬:  ',rows['commentCount'])
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['companyUrl']) #linktoProfile


    if not pd.isnull(rows['profileUrl']):
        #st.image(rows['profileImgUrl'], width=150)
        st.subheader(dataframe.fullName[i])
        st.write('Personal Account')
        st.write(rows['title']) #postType
        st.write('-----------')
       
        st.info(rows['textContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile




def printFunction_search(i, rows, dataframe):
   
    if not pd.isnull(rows['profileUrl']):
        #st.image(rows['profileImgUrl'], width=150)
        st.subheader(dataframe.fullName[i])
        st.write('Personal Account')
        st.write(rows['title']) #postType
        st.write('-----------')
       
        st.info(rows['textContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile
    



def printFunction_posts(i, rows, dataframe):
    if not pd.isnull(rows['profileUrl']):
        
        st.subheader(dataframe.company_name[i])
        st.write('Content Type: ', rows['type']) #postType
        st.write('-----------')
        if 'imgUrl' in dataframe.columns:
            # if rows['imgUrl']:
            #     st.image(rows['imgUrl'], width=230)

            if not pd.isnull(rows['imgUrl']):
                        st.image(rows['imgUrl'])

        st.info(rows['postContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile
    


def printFunction_accounts(i, rows, dataframe):
    if not pd.isnull(rows['profileUrl']):
        
        st.write(dataframe['profileUrl'][i])
        st.write('Content Type: ', rows['type']) #postType
        st.write('-----------')
        if 'imgUrl' in dataframe.columns:
            # if rows['imgUrl']:
            #     st.image(rows['imgUrl'], width=230)

            if not pd.isnull(rows['imgUrl']):
                        st.image(rows['imgUrl'])

        st.info(rows['postContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile


def printError():
    st.image('https://img.freepik.com/premium-vector/hazard-warning-attention-sign-with-exclamation-mark-symbol-white_231786-5218.jpg?w=2000', width =200)
    st.subheader('Oops... No new post found in last Hours.')


def printAccountInfo(dataframe, option):
    dataframe_copy = dataframe[dataframe.Branche == option]
    dataframe_copy = dataframe_copy.reset_index(drop=True)
    num_post = dataframe_copy.shape[0]
    if num_post>0:
        splits = dataframe_copy.groupby(dataframe_copy.index//3)
        for _,frame in splits:
            frame = frame.reset_index(drop=True)
            thumbnail = st.columns(frame.shape[0])
            for i, row in frame.iterrows():
                with thumbnail[i]:
                    st.subheader(row['Account_Name'])
                    if not pd.isnull(row['imgUrl']):
                        st.image(row['imgUrl'])
                    st.info(row['postContent'])
                    st.write('Publish Date & Time 📆:         ',row['postDate'])
                    st.write('Total Interactions 📈:  ',row['Total Interactions'])
                    st.write('Likes 👍:  ',row['likeCount']) #totInteractions
                    st.write('Comments 💬:  ',row['commentCount']) #totInteractions
                    with st.expander('Link to this Post 📮'):
                        st.write(row['postUrl']) #linktoPost
                    with st.expander('Link to  Profile 🔗'):
                        st.write(row['profileUrl']) #linktoProfile
    else:
        st.image('https://img.freepik.com/premium-vector/hazard-warning-attention-sign-with-exclamation-mark-symbol-white_231786-5218.jpg?w=2000', width =200)
        st.subheader('Oops... No new post found for the selection.')

