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


mapper = { 'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Immobilienwirtschaft&origin=FACETED_SEARCH&sid=q*e&sortBy=%22relevance%22' : 'Immobilienwirtschaft' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Immobilien&origin=GLOBAL_SEARCH_HEADER&sid=nk6&sortBy=%22relevance%22' : 'Immobilien' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Projektentwicklung&origin=GLOBAL_SEARCH_HEADER&sid=wdo&sortBy=%22relevance%22' : 'Projektentwicklung' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Asset%20Management&origin=GLOBAL_SEARCH_HEADER&sid=Ihf&sortBy=%22relevance%22' : 'Asset Management' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Immobilienbewertung&origin=GLOBAL_SEARCH_HEADER&sid=~n%40&sortBy=%22relevance%22' : 'Immobilienbewertung' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Baurecht&origin=GLOBAL_SEARCH_HEADER&sid=2x7&sortBy=%22relevance%22' : 'Baurecht' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Stadtentwicklung&origin=GLOBAL_SEARCH_HEADER&sid=54A&sortBy=%22relevance%22' : 'Stadtentwicklung' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Facility%20Management&origin=GLOBAL_SEARCH_HEADER&sid=8_9&sortBy=%22relevance%22' : 'Facility Management' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Investmentstrategien&origin=GLOBAL_SEARCH_HEADER&sid=Y5O&sortBy=%22relevance%22' : 'Investmentstrategien' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Nachhaltigkeit&origin=GLOBAL_SEARCH_HEADER&sid=Za!&sortBy=%22relevance%22' : 'Nachhaltigkeit' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Wohnimmobilien&origin=GLOBAL_SEARCH_HEADER&sid=8~B&sortBy=%22relevance%22' : 'Wohnimmobilien' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=gewerbeimmobilien&origin=FACETED_SEARCH&searchId=723f8104-fd1f-4384-9966-1a069a70b6a4&sid=edA' : 'Gewerbeimmobilien' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&heroEntityKey=urn%3Ali%3Aorganization%3A37373115&keywords=immobilienfinanzierung&origin=FACETED_SEARCH&position=0&searchId=49d6345a-12ea-48dc-a547-0a89f6c9438c&sid=_*9' : 'Immobilienfinanzierung' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Risikomanagement&origin=GLOBAL_SEARCH_HEADER&sid=TcY' : 'Risikomanagement' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Internationales%20Immobilienmanagement&origin=GLOBAL_SEARCH_HEADER&sid=mH~' : 'Internationales Immobilienmanagement' ,
            'https://www.linkedin.com/company/fomrealestate/?originalSubdomain=de' : 'FOM REAL ESTATE',
            'https://www.linkedin.com/in/prof-reinhard-walter-81b00922/?originalSubdomain=de':'Prof. Dr. Reinhard Walter'

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

