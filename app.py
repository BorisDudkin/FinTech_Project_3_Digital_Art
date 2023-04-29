import time
from pathlib import Path

import requests
import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Digital Solutions", layout='wide')

# st.title('Digital Art Solutions')
# st.write("---")
# st.image('Images/sc.png',use_column_width=True)
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = 'https://assets7.lottiefiles.com/packages/lf20_1iCXQLskUr.json'
lottie_json = load_lottieurl(lottie_url)

with st.sidebar:
    st_lottie(lottie_json, height=180)
    selected = option_menu(
        menu_title = 'Main Menu',
        options = ['🏠 Home','🔨 Minting and Registration','💰 Auction'],
        default_index = 0,
    )

if selected == '🏠 Home':

    st.title('Digital Art Solutions')
    st.write("---")
    st.image('Images/sc.png',use_column_width=True)


    st.write("---")

    st.subheader('Minting and Registration')

    my_text = "The Investment Advisor application will assess an investor's risk tolerance and their capacity to absorbe risk. Based on those evaluations, two corresponding risk scores will be calculated, and associated investment portfolios will be chosen from our ETFs offering. Their performance will be assessed and compared to the Benchmark portfolio with a 40/60 bond to stock ratio. To increase clients' awareness of our new Cryptomix ETF, we will include the comparison performance of this fund as well."

    st.write(my_text)
    st.write("---")
    st.subheader("Auction")
    st.write("We offer our clients a tailored approach to constructing an investment portfolio based on their risk tolerance and personal cicumstances to absorbe the risk arising from the investment activities.")
    st.write("---")
    with st.expander("Fees and Charges"):
        st.write("Assets in our funds range from High Growth and Crypto to Value Stocks and Fixed Income securities of long-term and short-term maturities. Each fund is constructed with the risk profile of an investor in mind. Our funds are non-diversified and may experience greater volatility than more diversified investments. To compensate for the limited diversification, we only offer Large Cap US equities and Domestic stocks and bonds to reduce volatility brought by small- and medium-cap equities, excluding foreign currency exposure. And yet, there will always be risks involved with ETFs' investments, resulting in the possible loss of money.")

if selected == '🔨 Minting and Registration':
    st.title('🔨 Mint and Register Your Artwork')
    st.write("---")
if selected == '💰 Auction':
    st.title('💰 Auction Your Artwork')
    st.write("---")
