import streamlit as st
import datetime as dt
from helpers import *



st.set_page_config(layout='wide')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
   
st.markdown("<h1 style='text-align: center; color: cyan;'>LinkedIn posts from the Salzgitter Acccounts </h1>", unsafe_allow_html=True)


filter_day, filter_Interactions, filter_date = display_filters()

dataframe_path = 'https://phantombuster.s3.amazonaws.com/UhrenaxfEnY/EQafnGzssfutlOPDc4DvUA/salzgitter_accounts.csv'
try:
	df_main = load_dataframe(dataframe_path)

	filtered_posts = filter_and_sort_posts(df_main, filter_day, filter_Interactions, filter_date)

	if filtered_posts is not None:
		num_posts = filtered_posts.shape[0]
		st.write(f'Total number of posts found: {num_posts}')

		display_post_chunks(filtered_posts)

	else:
		st.write('An error occurred!')

	
except:
	st.write('Error encountered!!')