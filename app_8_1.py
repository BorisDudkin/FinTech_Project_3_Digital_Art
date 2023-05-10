import time
from pathlib import Path
import math
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

address_register = os.getenv("SMART_CONTRACT_ADDRESS")
address_auction = os.getenv("SMART_CONTRACT_ADDRESS_2")

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

    st.subheader('About this Application')

    app = "This application offrs the digital art creators a one-step full solution from minting and registering their digital art to putting the art pieces on the auction."
    st.write(app)
    st.write("---")

    st.subheader('Minting and Registration')

    mining = "A simple user friendly interface of the applcation allows a user to first mint and register his/her art piece. Once the NFT is minted and registered, we utilize Pinata services to store the newly created contracts in a decentralized manner."
    st.write(mining)
    st.write("---")

    st.subheader("Auction")
    st.write("After minting and registering their art, the creator can right away put it on the decentralized marketplace. The auction runs a certain time period within which the bidders can place their bids and, where the highest bid and the highest bidder are identified after each bid. The bid withdrawl is alsa avalibale to the bidders who are not identified as the highest bidder. The withdrawl is open during as well as some additional time aftr the auction's closing.</br>Once the auction will have ended, the NFT will have changed the ownership and be transferred to the highest bidder, if any, while the highest bid will have been transfterred to the seller.")
    st.write("---")
    # with st.expander("Fees and Charges"):
    #     st.write("Assets in our funds range from High Growth and Crypto to Value Stocks and Fixed Income securities of long-term and short-term maturities. Each fund is constructed with the risk profile of an investor in mind. Our funds are non-diversified and may experience greater volatility than more diversified investments. To compensate for the limited diversification, we only offer Large Cap US equities and Domestic stocks and bonds to reduce volatility brought by small- and medium-cap equities, excluding foreign currency exposure. And yet, there will always be risks involved with ETFs' investments, resulting in the possible loss of money.")

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
        with open(Path('./contracts/compiled/NFT_registry_abi.json')) as f:
            contract_abi = json.load(f)

        # Set the contract address (this is the address of the deployed contract)
        contract_address = address_register

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

    if 'my_list' not in st.session_state:
        st.session_state['my_list'] = []

    st.title("Art Registration, mint your token")
    register, a_list = st.columns(2, gap='large')
    register.write("Choose an account to get started")
    accounts = w3.eth.accounts
    address = register.selectbox("Select Account", options=accounts)
    register.markdown("---")

   #give permission auction to trade the token:
    tx_hash = contract.functions.setApprovalForAll(
        address_auction,
        True
    ).transact({'from': address, 'gas': 1000000})
    
    # Register New Artwork
    register.markdown("## Register New Artwork")
    artwork_name = register.text_input("Enter the name of the artwork")
    artist_name = register.text_input("Enter the artist name")
    initial_appraisal_value = register.number_input("Enter Auction Starting Bid", step=1000)
    file = register.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])

    if register.button("Register Artwork"):
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

        #register.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        #register.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
        register.write("Your tokenized artwork:")
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
        art_dict["image"] = image_ipfs_hash
        art_dict["token_id"] = token_id

        #st.write(art_dict)

        #auc_list=register.checkbox("Add NFT to your auction list?")

#        if auc_list:
#            st.write(auc_list)
        if 'art_d' not in st.session_state:
            st.session_state.art_d = art_dict

        my_list= st.session_state['my_list']
        #st.write(my_list)
        my_list.append(art_dict)
        st.session_state['my_list']=my_list
        for art in my_list:
            #a_list.write(art)
            a_list.write(f"NFTs to be auctioned soon: {art['artwork_name']}")
        #auction=a_list.button("Start new auction?")
        #if auction:
            art_list=st.session_state['auction_list']
            joint_list = art_list + my_list
            #st.write('afterjoin',joint_list)
            # art_list.append(art_dict)
            st.session_state['auction_list'] = joint_list
            #st.write('aftersessionstate',joint_list)
            st.session_state['my_list'] = []
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
    accounts = w3.eth.accounts

    new_auction=st.checkbox("Start New Auction")
    if new_auction:
        ## Load Auction Contract once using cache
        @st.cache_resource()
        def load_contract2():

            # Load the contract ABI
            with open(Path('./contracts/compiled/NFT_Auction_abi.json')) as f:
                contract_abi = json.load(f)

            # Set the contract address (this is the address of the deployed contract)
            contract_address_2 = address_auction

            # Get the contract
            contract_2 = w3.eth.contract(
                address=contract_address_2,
                abi=contract_abi
            )

            return contract_2

        # Load the contract
        contract_2 = load_contract2()

        st.write("---")

        # set variables
        if 'art_d' not in st.session_state:
            st.info("### :magenda[There are no items to auction at the momement!]")
        else:
            art=st.session_state.art_d

        # if 'in_progress' not in st.session_state:
        #     st.session_state.in_progress = True

        if 'started' not in st.session_state:
            st.session_state.started = True

        if 'ended' not in st.session_state:
            st.session_state.ended = True

        if 'set_seller' not in st.session_state:
            st.session_state.set_seller = True

        if 'highestbid' not in st.session_state:
            st.session_state.highestbid = art['last_bid']
        
        if 'highestbidder' not in st.session_state:
            st.session_state.highestbidder = art['seller']

        if 'seller' not in st.session_state:
            st.session_state.seller = art['seller']

        image_link = "https://gateway.pinata.cloud/ipfs/"+art['image']
        time_auction = 125 # I've changed this to 20 seconds for now. 
        # counter_auction = time_auction
        time_withdraw = time_auction + 20
        time_sec = time_withdraw
        if 'time_sec' not in st.session_state:
            st.session_state.time_sec = time_withdraw

        if 'counter_auction' not in st.session_state:
            st.session_state.counter_auction = time_auction
        #testing
        st.write(f"started: {st.session_state.started}")
        st.write(f"ended: {st.session_state.ended}")
        st.write(f"set_seller: {st.session_state.set_seller}")

        # Set seller for contract
        if st.session_state.set_seller:
            tx_hash = contract_2.functions.setSeller(
            art['seller'], # address of seller of art
            ).transact({'from': art['seller'], 'gas': 1000000})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            seller = contract_2.functions.seller().call()
            st.session_state.set_seller = not st.session_state.set_seller
            
            #testing
            st.write(seller)
            st.write(f"started: {st.session_state.started}")
            st.write(f"ended: {st.session_state.ended}")
            st.write(f"set_seller: {st.session_state.set_seller}")
        
        col1, col2, col3 = st.columns([1,2,2], gap='large')
        # my_form = st.form(key="Characteristics)")
        # with st_lottie_spinner(lottie_json_auction, height=100):
            
        with col2:
            placeholder_2= st.container()
            with placeholder_2:
                st.write(f"#### {art['artwork_name']}")
                st.image(image_link, width = 400)
                st.write(f"Creator: {art['author']}")
                st.write(f"Initial Value: **:blue[{art['init']}]** ETH")
                # st.write(f"Highest Bid: **:blue[{st.session_state.highestbid }]** ETH", key ='highestbid')
        with col1:
            placeholder_1= st.empty()
            placeholder_4= st.empty()

        with col3:
            placeholder_3= st.container()
            highestbidder_bid= st.container()
            with placeholder_3:
                # st.write('#### Bid/Withdraw', key = 'bw'+ str(count_art))
                # bidder_address=st.text_input(" #### Bidder's Address")
                # st.text_input("Highest Bidder (address)", key ='highestbidder')
                # st.number_input("Highest Bid (in ETH)", key ='highestbid')  
                
                bid, withdr = st.columns(2, gap = 'large')
                with bid:
                    bidder_form = st.form(key="bidder_form")
                    bidder_address = bidder_form.selectbox(" #### Bidder's Address", options=accounts)
                    bid_amunt = bidder_form.number_input("Bid (in ETH)")
                    place_bid = bidder_form.form_submit_button('Place Bid')

                    if place_bid:
                        if st.session_state.counter_auction>0: 
                            bid_wei = w3.toWei(bid_amunt, 'ether')
                            tx_hash = contract_2.functions.bid().transact({'from': bidder_address,'value': bid_wei, 'gas': 1000000})
                            # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                            highestbid = contract_2.functions.highestBid().call()
                            st.session_state.highestbid  = w3.fromWei(highestbid, "ether")
                            highestbidder = contract_2.functions.highestBidder().call()
                            st.session_state.highestbidder  = highestbidder
                        else:
                            st.warning("Auction ended - cannot place bids!")
                with withdr:
                    withdraw_form = st.form(key="withdraw_form")
                    withdrawer_address = withdraw_form.selectbox(" #### Withdrawer's Address", options=accounts)
                    withdraw_bid=withdraw_form.form_submit_button('Withdraw Bid')

                    if withdraw_bid:
                        if withdrawer_address == st.session_state.highestbidder :
                            st.info("You cannot withdraw as you are the **:orange[highest bidder]**!")
                        else:
                            tx_hash = contract_2.functions.withdraw().transact({'from': withdrawer_address, 'gas': 1000000})
                with highestbidder_bid:        # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                    st.write(f"Highest Bidder: **:pink[{st.session_state.highestbidder}]**", key ='highestbidder')    
                    st.write(f"Highest Bid: **:blue[{st.session_state.highestbid }]** ETH", key ='highestbid')       

        while st.session_state.time_sec:
            if st.session_state.started:
                st.session_state.started = not st.session_state.started
                # start auction function
                tx_hash = contract_2.functions.start(
                address_register, # address of nft registery
                art['token_id'], # token id is from art['token_id']
                art['init'], # intial is from art ['initial price']
                ).transact({'from': st.session_state.seller, 'gas': 1000000})
                receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                #testing
                # st.write(receipt)
                # st.write(f"in_progress: {st.session_state.in_progress}")
                st.write(f"started: {st.session_state.started}")
                st.write(f"ended: {st.session_state.ended}")
                st.write(f"set_seller: {st.session_state.set_seller}")


            st.session_state.time_sec-=1
            st.session_state.counter_auction -=1
            n1 = st.session_state.counter_auction  / 3600
            hours = int(st.session_state.counter_auction  // 3600)
            n2 = (n1-hours)*60
            mins = int(math.floor(n2))
            n3 = n2-mins
            secs = int(round(n3*60,0))
            # hours, remainder = divmod(counter_auction, 3600)
            # mins, secs = divmod(remainder, 60)
            time_now = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)

            #withdrawl remainder
            m1 = st.session_state.time_sec / 3600
            hours_w = int(st.session_state.time_sec // 3600)
            m2 = (m1-hours_w)*60
            mins_w = int(math.floor(m2))
            m3 = m2-mins_w
            secs_w = int(round(m3*60,0))
            # hours_w, remainder_w = divmod(time_sec, 3600)
            # mins_w, secs_w = divmod(remainder_w, 60)
            time_now_w = '{:02d}:{:02d}:{:02d}'.format(hours_w, mins_w, secs_w)

            if st.session_state.counter_auction>0:                   
                with placeholder_1.container():
                    st.markdown('##### Auction Count-down')
                    st.subheader(f'**:green[{time_now}]**')
                with placeholder_4.container():
                    st_lottie(lottie_json_auction, width=180, key = str(st.session_state.time_sec))
            else:
                if st.session_state.ended:
                    # end auction function
                    st.session_state.ended = not st.session_state.ended
                    tx_hash = contract_2.functions.end().transact({'from': st.session_state.seller, 'gas': 1000000})
                    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                    #testing
                    # st.write(f"in_progress: {st.session_state.in_progress}")
                    st.write(receipt)
                    st.write(f"started: {st.session_state.started}")
                    st.write(f"ended: {st.session_state.ended}")
                    st.write(f"set_seller: {st.session_state.set_seller}")

                with placeholder_1.container():
                    st.markdown('##### Auction ended. Withdraw bids within:')
                    st.subheader(f'**:red[{time_now_w}]**')
                placeholder_4.empty()
           

            time.sleep(1)
                # time_sec-=1
        # placeholder_1.empty()
        # placeholder_2.empty()
        # placeholder_3.empty()
        st.balloons()
        st.markdown("#### **:red[Auction ended!]**")

        # st.session_state.in_progress = not st.session_state.in_progress
        st.session_state.started = not st.session_state.started
        st.session_state.ended = not st.session_state.ended
        st.session_state.set_seller = not st.session_state.set_seller
        #testing
        # st.write(f"in_progress: {st.session_state.in_progress}")
        # st.write(f"started: {st.session_state.started}")
        # st.write(f"ended: {st.session_state.ended}")
        # st.write(f"set_seller: {st.session_state.set_seller}")

