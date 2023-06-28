import streamlit as st
import time
import datetime as dt

from helpers import *



st.set_page_config(layout='wide')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# logo, _ = st.columns(2)
# with logo:
# 	st.image(storymch_logo, width=200)
   
st.markdown("<h1 style='text-align: center; color: cyan;'>LinkedIn posts from the Salzgitter Acccounts </h1>", unsafe_allow_html=True)



col1, col2, col3 = st.columns(3)

with col1:
	filter_day = st.number_input("How many days older posts?", min_value=1, max_value=100, value=7, step=1)
	if filter_day:
		st.success(f'Showing Posts from last {int(filter_day)} Days', icon="✅")

with col2:
	filter_Interactions = st.selectbox( "Filter by total interactions",
						('Total Interaction: High to Low',
						'Total Interaction: Low to High'))

with col3:
	filter_date = st.selectbox( "Filter by total Post date",
						('Posts: Newest First',
						'Posts: Oldest First'))



mutares_emp_path = 'https://cache1.phantombooster.com/UhrenaxfEnY/JLfiphEk8jlUgrwTfub8MQ/salzgitter_accounts_6_28.csv'


#mutares_emp_main = read_file_sp(mutares_emp_path)
mutares_emp_main = read_file_account(mutares_emp_path)


mutares_emp_df = mutares_emp_main[mutares_emp_main['date']>=(dt.datetime.now()-dt.timedelta(days=filter_day))]


mutares_emp_df = mutares_emp_df.sort_values(by = ['yy-dd-mm','Total Interactions'], ascending=[ filters[filter_date][1], filters[filter_Interactions][1]])



	
mutares_emp_df = mutares_emp_df.reset_index(drop=True)



mutares_emp_df_copy = mutares_emp_df.copy()
num_posts = mutares_emp_df_copy.shape[0]
st.write(f'Total number of posts found: ', str(num_posts))

if  num_posts>0:
	splits = mutares_emp_df_copy.groupby(mutares_emp_df_copy.index // 3)
	for _, frames in splits:
		frames = frames.reset_index(drop=True)
		thumbnails = st.columns(frames.shape[0])
		for i, c in frames.iterrows():
			with thumbnails[i]:
				printFunction_accounts(i, c, frames)           
				#printFunction_posts(i, c, frames)        
else:
	printError()


