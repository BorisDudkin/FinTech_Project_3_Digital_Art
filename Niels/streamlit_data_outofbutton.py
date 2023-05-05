import streamlit as st
import csv
import os
# Initialize an empty list to store data
#data_list = []

    # Get some data from the user
artwork_name = st.text_input("Enter some data:")
author = st.text_input("author")
init = st.number_input('initial bid',min_value=1,max_value=10)
image = st.text_input("whatever")

# Create a Streamlit button
if st.button("Add Data"):
    
    file_path = 'Auction.csv'
    header = ['artwork_name', 'author','init','image']
    data = [artwork_name,author,init,image]
    
    if not os.path.isfile(file_path):
        with open(file_path, 'w',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(data)

    else: 
        with open(file_path,'a',newline ='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
