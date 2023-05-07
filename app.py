import time
from pathlib import Path

import requests
import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
from streamlit_option_menu import option_menu
from attributedict.collections import AttributeDict

st.set_page_config(page_title="Digital Solutions", layout='wide')

#########
# NIELS
########
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
####

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

lottie_url_auction = 'https://assets3.lottiefiles.com/private_files/lf30_9cbxvjqt.json'

lottie_json_auction = load_lottieurl(lottie_url_auction)

with st.sidebar:
    st_lottie(lottie_json, height=270, key="lottie_sidebar")
    selected = option_menu(
        menu_title = 'Main Menu',
        options = ['🏠 Home','🔨 Minting and Registration','💰 Auction'],
        default_index = 0,
    )

if selected == '🏠 Home':

    st.title('🏠 Digital Art Solutions')
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

#######
# NIELS
#######

if selected == '🔨 Minting and Registration':
    st.title('🔨 Mint and Register Your Artwork')
    st.write("---")
    
  
    ## Loads the contract once using cache
    @st.cache_resource()
    def load_contract():

        # Load the contract ABI
        with open(Path('./contracts/compiled/NFT_registry.json')) as f:
            contract_abi = json.load(f)

        # Set the contract address (this is the address of the deployed contract)
        contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

        # Get the contract
        contract = w3.eth.contract(
            address=contract_address,
            abi=contract_abi
        )

        return contract

    # Load the contract
    contract = load_contract()

# Helper functions to pin files and json to Pinata

    def pin_artwork(artwork_name, artwork_file):
        # Pin the file to IPFS with Pinata
        ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

        # Build a token metadata file for the artwork
        token_json = {
            "name": artwork_name,
            "image": ipfs_file_hash
        }
        json_data = convert_data_to_json(token_json)

        # Pin the json to IPFS with Pinata
        json_ipfs_hash = pin_json_to_ipfs(json_data)

        return json_ipfs_hash

    def pin_image(artwork_file):
        # Pin the file to IPFS with Pinata
        ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())
        
        # Build a token metadata file for the artwork
        token_json_2 = ipfs_file_hash

        json_data_image = convert_data_to_json(token_json_2)

        # Pin the json to IPFS with Pinata
        json_ipfs_hash_image = pin_json_to_ipfs(json_data_image)

        # return hash of picture on pinata
        return token_json_2 

### To be removed in next version
    def pin_appraisal_report(report_content):
        json_report = convert_data_to_json(report_content)
        report_ipfs_hash = pin_json_to_ipfs(json_report)
        return report_ipfs_hash
###
    if 'auction_list' not in st.session_state:
        st.session_state['auction_list'] = []

    st.title("Art Registration, mint your token")
    register, a_list = st.columns(2, gap='large')
    register.write("Choose an account to get started")
    accounts = w3.eth.accounts
    address = register.selectbox("Select Account", options=accounts)
    register.markdown("---")

    # Register New Artwork
    register.markdown("## Register New Artwork")
    artwork_name = register.text_input("Enter the name of the artwork")
    artist_name = register.text_input("Enter the artist name")
    initial_appraisal_value = register.number_input("Enter Auction Starting Bid", step=1000)
    file = register.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
    # art_list = []

    # else:
    #     st.session_state['auction_list'] = []

    if register.button("Register Artwork"):
        my_list=[]
        artwork_ipfs_hash = pin_artwork(artwork_name, file)
        artwork_uri = f"ipfs://{artwork_ipfs_hash}"
        image_ipfs_hash = pin_image(file)

        # create token ID for this contract
        #token_id = contract.functions.registerArtwork(tokenId).call()

        tx_hash = contract.functions.registerArtwork(
            address,
            artwork_name,
            artist_name,
            int(initial_appraisal_value),
            artwork_uri
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        # st.write("Transaction receipt mined:")
        # st.write(dict(receipt))
        register.markdown("---")

        register.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        register.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
        register.write("Your uploaded artwork:")
        register.markdown(f"![Artwork Link](https://gateway.pinata.cloud/ipfs/{image_ipfs_hash})")

        #  temporary tokenId:
        event_filter = contract.events.TokenId.createFilter(fromBlock='latest')
        reports = event_filter.get_all_entries()
        if reports:
            for report in reports:
                report_dictionary = dict(report)
        # st.write(int(report_dictionary['args'].tokenId))

        token_id = int(report_dictionary['args'].tokenId)

        # token_id=0

        # crete a dictionary with the new art work
        art_dict ={}
        art_dict["seller"] = address
        art_dict["artwork_name"] = artwork_name
        art_dict["author"] = artist_name
        art_dict["init"] = initial_appraisal_value
        art_dict["last_bid"] = 0
        art_dict["image"] = "https://gateway.pinata.cloud/ipfs/{image_ipfs_hash})"
        art_dict["token_id"] = token_id

        auc_list=register.button("Add NFT to your auction list?")
        if auc_list:
            my_list.append(art_dict)

        for art in my_list:
            a_list.write(f"NFT {art['artwork_name']}")
        auction=a_list.button("Start new auction?")
        if auction:
            art_list=st.session_state['auction_list']
            joint_list = art_list + my_list
            # art_list.append(art_dict)
            st.session_state['auction_list'] = joint_list

        st.markdown("---")
    # st.write(st.session_state)
    # auction=st.button("Start new auction?")
    # st.write(auction)
    # if "load_state" not in st.session_state:
    #     st.session_state.load_state = False
    # if auction:
    #     st.session_state.load_state = True
        # st.write(st.session_state)
    # st.write(st.session_state)

if selected == '💰 Auction':
    st.title('💰 Auction')
    st.write("---")
    count_art = 0

    if 'auction_list' not in st.session_state:
        st.info("### :magenda[There are no items to auction at the momement!]")
    else:
        art_list=st.session_state['auction_list']


    while len(art_list)>0:
    # for art in art_list:
        art = art_list.pop(0)
        st.session_state['auction_list'] = art_list
        count_art +=1

        #set auction time to 3 min
        time_auction = 130
        counter_auction = time_auction
        time_withdraw = time_auction + 20
        time_sec = time_withdraw

        
        col1, col2, col3 = st.columns([1,2,2], gap='large')
        # my_form = st.form(key="Characteristics)")
        # with st_lottie_spinner(lottie_json_auction, height=100):
            
        with col2:
            placeholder_2= st.empty()
            with placeholder_2.container():
                st.write(f"#### {art['artwork_name']}", key = 'name'+ str(count_art))
                st.image(art['image'], width = 400)
                st.write(f"Creator: {art['author']}", key = 'author'+ str(count_art))
                st.write(f"Initial Value: **:blue[{art['init']}]** ETH", key = 'Initial_value'+ str(count_art))
                st.write(f"Highest Bid: **:blue[{art['last_bid']}]** ETH", key = 'last_bid'+ str(count_art))
                # st.write(f"My name {art['init']}", key = "Initial_value"+ str(count_art))

        with col1:
            placeholder_1= st.empty()
            placeholder_4= st.empty()

        with col3:
            placeholder_3= st.empty()
            placeholder_5= st.empty()
            with placeholder_3.container():
                # st.write('#### Bid/Withdraw', key = 'bw'+ str(count_art))
                st.text_input(" #### Bidder's Address", key = 'bid_address'+ str(count_art))
                
                bid, withdr = st.columns(2, gap = 'large')
                with bid:
                    st.number_input("Bid (in ETH)", key = 'bid'+ str(count_art))
                    st.button('Place Bid', key = 'order'+ str(count_art))
                with withdr:
                    st.button('Withdraw Bid', key = 'withdraw'+ str(count_art))

        while time_sec:
            time_sec-=1
            counter_auction-=1
            n1 = counter_auction / 3600
            hours = int(counter_auction // 3600)
            n2 = (n1-hours)*60
            mins = int(math.floor(n2))
            n3 = n2-mins
            secs = int(round(n3*60,0))
            # hours, remainder = divmod(counter_auction, 3600)
            # mins, secs = divmod(remainder, 60)
            time_now = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)

            #withdrawl remainder
            m1 = time_sec / 3600
            hours_w = int(time_sec // 3600)
            m2 = (m1-hours_w)*60
            mins_w = int(math.floor(m2))
            m3 = m2-mins_w
            secs_w = int(round(m3*60,0))
            # hours_w, remainder_w = divmod(time_sec, 3600)
            # mins_w, secs_w = divmod(remainder_w, 60)
            time_now_w = '{:02d}:{:02d}:{:02d}'.format(hours_w, mins_w, secs_w)

            if counter_auction>0:
                with placeholder_1.container():
                    st.markdown('##### Auction Count-down')
                    st.subheader(f'**:green[{time_now}]**')
                with placeholder_4.container():
                    st_lottie(lottie_json_auction, width=180, key = str(time_sec)+str(count_art))
            else:
                with placeholder_1.container():
                    st.markdown('##### Auction ended. Withdraw bids within:')
                    st.subheader(f'**:red[{time_now_w}]**')
                placeholder_4.empty()               

            time.sleep(1)
                # time_sec-=1
        placeholder_1.empty()
        placeholder_2.empty()
        placeholder_3.empty()
        st.balloons()
    st.markdown("#### **:red[All auction ended!]**")


