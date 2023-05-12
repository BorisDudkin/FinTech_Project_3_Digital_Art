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

# get smart contract addresses from env file
address_nft_register = os.getenv("SMART_CONTRACT_NFT_REGISTER")
address_auction = os.getenv("SMART_CONTRACT_AUCTION")

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

# set locations for lottie files
lottie_url = 'https://assets7.lottiefiles.com/packages/lf20_1iCXQLskUr.json'
lottie_json = load_lottieurl(lottie_url)
lottie_url_auction = 'https://assets3.lottiefiles.com/private_files/lf30_9cbxvjqt.json'
lottie_json_auction = load_lottieurl(lottie_url_auction)

# include lottie file into side bar
with st.sidebar:
    st_lottie(lottie_json, height=270, key="lottie_sidebar")
    selected = option_menu(
        menu_title = 'Main Menu',
        options = ['🏠 Home','🔨 Minting and Registration','💰 Auction'],
        default_index = 0,
    )

# Home section starts here
if selected == '🏠 Home':

    # write title
    st.title('🏠 Digital Art Solutions')
    st.write("---")
    st.image('Images/sc.png',use_column_width=True)

    st.write("---")

    # write introduction for the application and pages
    st.subheader('About this Application')

    app = "This application offers the digital art creators a one-step full solution from minting and registering their digital art to selling the art pieces on the auction."
    st.write(app)
    st.write("---")

    st.subheader('Minting and Registration')

    mining = "A simple user friendly interface of the applcation allows a user to first mint and register his/her art piece. Once the NFT is minted and registered, we utilize Pinata services to store the newly created contracts in a decentralized manner."
    st.write(mining)
    st.write("---")

    st.subheader("Auction")
    st.markdown("After minting and registering their art, the creators can right away put it on the decentralized marketplace. The auction runs a certain time period, within which the bidders can place their bids and, where the highest bid and the highest bidder are identified after each bid. The withdrawl is avalibale to the bidders, who are not identified as the highest bidder. The withdrawl remains open during, as well as some additional time after the auction's closing. Once the auction will have ended, the NFT will change the ownership by being transferred to the highest bidder, while the highest bid will be transfterred to the seller.")
    st.write("---")
    # with st.expander("Fees and Charges"):
    #     st.write("Assets in our funds range from High Growth and Crypto to Value Stocks and Fixed Income securities of long-term and short-term maturities. Each fund is constructed with the risk profile of an investor in mind. Our funds are non-diversified and may experience greater volatility than more diversified investments. To compensate for the limited diversification, we only offer Large Cap US equities and Domestic stocks and bonds to reduce volatility brought by small- and medium-cap equities, excluding foreign currency exposure. And yet, there will always be risks involved with ETFs' investments, resulting in the possible loss of money.")

#######
# NIELS
#######

# minting and registration page beginst here
if selected == '🔨 Minting and Registration':
    st.title('🔨 Mint and Register Your Artwork')
    st.write("---")
    
  
    ## Loads the NFT register contract once using cache
    @st.cache_resource()
    # define loading contract of nft register
    def load_contract_nft_register():

        # Load the contract ABI of nft register
        with open(Path('./contracts/compiled/NFT_registry_abi.json')) as f:
            contract_abi = json.load(f)

        # Set the contract address (this is the address of the nft register contract)
        contract_address_nft_register = address_nft_register

        # Get the nft register contract
        contract_nft_register = w3.eth.contract(
            address=contract_address_nft_register,
            abi=contract_abi
        )

        # return the nft register contract
        return contract_nft_register

    # Load the nft register contract
    contract_nft_register = load_contract_nft_register()
    
    # functions to pin files and json to Pinata

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

    # start of uploading artwork and minting token
    st.title("Art Registration, mint your token")
    register, a_list = st.columns(2, gap='large')
    register.write("Choose an account to get started")
    accounts = w3.eth.accounts
    address = register.selectbox("Select Account", options=accounts)
    register.markdown("---")

   # give auction to permission trade the token during auction:
    tx_hash = contract_nft_register.functions.setApprovalForAll(
        address_auction,
        True
    ).transact({'from': address, 'gas': 1000000})
    
    # Register New Artwork
    register.markdown("## Register New Artwork")
    artwork_name = register.text_input("Enter the name of the artwork")
    artist_name = register.text_input("Enter the artist name")
    initial_appraisal_value = register.number_input("Enter Auction Starting Bid in ETH", step=1)
    file = register.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])

    # create art_d session state
    if 'art_d' not in st.session_state:
            st.session_state.art_d = {}
    
    # create register artwork button if pressed continue
    if register.button("Register Artwork"):
        artwork_ipfs_hash = pin_artwork(artwork_name, file)
        artwork_uri = f"ipfs://{artwork_ipfs_hash}"
        image_ipfs_hash = pin_image(file)

        # run smart contract function to Register Artwork
        tx_hash = contract_nft_register.functions.registerArtwork(
            address,
            artwork_name,
            artist_name,
            int(initial_appraisal_value),
            artwork_uri
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        register.markdown("---")

        #  Call tokenid event to incorporate tokenId:
        event_filter = contract_nft_register.events.TokenId.createFilter(fromBlock='latest')
        reports = event_filter.get_all_entries()
        if reports:
            for report in reports:
                report_dictionary = dict(report)

        # set token id variable
        token_id = int(report_dictionary['args'].tokenId)

        # create a dictionary with the new art work
        art_dict ={}
        art_dict["seller"] = address
        art_dict["artwork_name"] = artwork_name
        art_dict["author"] = artist_name
        art_dict["init"] = initial_appraisal_value
        art_dict["last_bid"] = 0
        art_dict["image"] = image_ipfs_hash
        art_dict["token_id"] = token_id

        # if 'art_d' not in st.session_state:
        st.session_state.art_d = art_dict

        # create an overview of the recently registered and minted artwork    
        a_list.write(f"NFTs Ready for Auction")
        # define preview of artwork
        image_uploaded = "https://gateway.pinata.cloud/ipfs/"+art_dict['image']
        # show preview of artwork
        a_list.image(image_uploaded, width = 300)
        # write features of the artwork just minted
        a_list.write(f"Artwork: {art_dict['artwork_name']}")
        a_list.write(f"Artist: {art_dict['author']}")
        a_list.write(f"Owner: {art_dict['seller']}")
        a_list.write(f"token ID: {art_dict['token_id']}")    

    # create load_state session state
    if "load_state" not in st.session_state:
        st.session_state.load_state = False
    else:
        st.session_state.load_state = False

    # create button for auctioning the registered NFT
    auction=a_list.button("Auction your NFT?")
    if auction:
        st.session_state.load_state = not st.session_state.load_state

        st.markdown("---")
        
# Auction page begins here
if selected == '💰 Auction':
    st.title('💰 Auction')

    # check load_state
    if "load_state" not in st.session_state:
        st.session_state.load_state = False

    # if load state ready then proceed to auction
    auction = st.session_state.load_state
    if auction:
        accounts = w3.eth.accounts
        
        ## Load Auction Contract once using cache
        @st.cache_resource()
        def load_contract_auction():

            # Load the auction contract ABI
            with open(Path('./contracts/compiled/NFT_Auction_abi.json')) as f:
                contract_abi_auction = json.load(f)

            # Set the auction contract address (this is the address of the deployed contract)
            contract_address_auction = address_auction

            # Get the auction contract
            contract_auction = w3.eth.contract(
                address=contract_address_auction,
                abi=contract_abi_auction
            )

            # return auction contract
            return contract_auction

        # Load the auction contract
        contract_auction = load_contract_auction()

        st.write("---")

        # set session state variables
        if 'art_d' not in st.session_state:
            st.info("### :magenda[There are no items to auction at the momement!]")
        else:
            art=st.session_state.art_d

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

        # present artwork on auction
        image_link = "https://gateway.pinata.cloud/ipfs/"+art['image']
        # create timer of auction
        time_auction = 125 
        # create a timeframe to withdraw 
        time_withdraw = time_auction + 30
        time_sec = time_withdraw
        if 'time_sec' not in st.session_state:
            st.session_state.time_sec = time_withdraw

        if 'counter_auction' not in st.session_state:
            st.session_state.counter_auction = time_auction
        # #testing
        # st.write(f"started: {st.session_state.started}")
        # st.write(f"ended: {st.session_state.ended}")
        # st.write(f"set_seller: {st.session_state.set_seller}")

        # Set seller for contract
        if st.session_state.set_seller:
            tx_hash = contract_auction.functions.setSeller(
            art['seller'], # address of seller of art
            ).transact({'from': art['seller'], 'gas': 1000000})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            seller = contract_auction.functions.seller().call()
            st.session_state.set_seller = not st.session_state.set_seller
        
        # create 3 columns for auction page to display artwork and bid/withdraw option and accounts
        col1, col2, col3 = st.columns([1,2,2], gap='large')
       
        # create column 2 to display artwork and creator and inital value    
        with col2:
            placeholder_2= st.container()
            with placeholder_2:
                st.write(f"#### {art['artwork_name']}")
                st.image(image_link, width = 400)
                st.write(f"Creator: {art['author']}")
                st.write(f"Initial Value: **:blue[{art['init']}]** ETH")
                # st.write(f"Highest Bid: **:blue[{st.session_state.highestbid }]** ETH", key ='highestbid')
        # leave column1 empty 
        with col1:
            placeholder_1= st.empty()
            placeholder_4= st.empty()

        # create column 3 with form to bid / withdraw and selection of addresses
        with col3:
            placeholder_3= st.container()
            highestbidder_bid= st.container()
            with placeholder_3:
                bidder_form = st.form(key="bidder_form")
                bidder_address = bidder_form.selectbox(" #### Bidder's Address", options=accounts)
                bid_amunt = bidder_form.number_input("Bid (in ETH)")
                bidder_choice = bidder_form.radio(label ="Bid or Withdraw?", options = ['Bid', 'Withdraw All'], horizontal=True)
                submit = bidder_form.form_submit_button('Submit')

                # define what happens when bid is placed
                if submit:
                    if bidder_choice == "Bid":
                        if bidder_address == st.session_state.seller:
                            st.error("**:orange[the Seller]** is not allowed to place bids!", icon ="⛔")
                        if st.session_state.counter_auction>0:
                            bid_wei = w3.toWei(bid_amunt, 'ether')
                            tx_hash = contract_2.functions.bid().transact({'from': bidder_address,'value': bid_wei, 'gas': 1000000})
                            # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                            highestbid = contract_2.functions.highestBid().call()
                            st.session_state.highestbid  = w3.fromWei(highestbid, "ether")
                            highestbidder = contract_2.functions.highestBidder().call()
                            st.session_state.highestbidder  = highestbidder
                        else:
                            st.warning("Auction ended - cannot place bids!", icon="⚠️")
                    else:
                        if bidder_address == st.session_state.highestbidder:
                            st.info("You cannot withdraw as you are the **:orange[highest bidder]**!", icon = "❌")
                        else:
                            tx_hash = contract_2.functions.withdraw().transact({'from': bidder_address, 'gas': 1000000})
                # if submit:
                #     if bidder_choice == "Bid":
                #         if st.session_state.counter_auction>0: 
                #             bid_wei = w3.toWei(bid_amunt, 'ether')
                #             # call bid function from auction contract
                #             tx_hash = contract_auction.functions.bid().transact({'from': bidder_address,'value': bid_wei, 'gas': 1000000})
                #             # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                #             # call highest bid function from auction contract
                #             highestbid = contract_auction.functions.highestBid().call()
                #             st.session_state.highestbid  = w3.fromWei(highestbid, "ether")
                #             highestbidder = contract_auction.functions.highestBidder().call()
                #             st.session_state.highestbidder  = highestbidder
                #         else:
                #             # create warning that auction ended so no bids can be placed anymore
                #             st.warning("Auction ended - cannot place bids!")
                #     else:
                #         # make sure highest bidder cannot withdraw
                #         if bidder_address == st.session_state.highestbidder :
                #             st.info("You cannot withdraw as you are the **:orange[highest bidder]**!")
                #         # else bidder can withdrawfrom auction
                #         else:
                #             tx_hash = contract_auction.functions.withdraw().transact({'from': bidder_address, 'gas': 1000000})
            # show highest bidder                 
            with highestbidder_bid:        # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                st.write(f"Highest Bidder: **:green[{st.session_state.highestbidder}]**", key ='highestbidder')    
                st.write(f"Highest Bid: **:green[{st.session_state.highestbid }]** ETH", key ='highestbid')       

        # when time starts running call start function once 
        while st.session_state.time_sec:
            if st.session_state.started:
                st.session_state.started = not st.session_state.started
                
                # start auction function
                tx_hash = contract_auction.functions.start(
                address_nft_register, # address of nft registery
                art['token_id'], # token id is from art['token_id']
                art['init'], # intial is from art ['initial price']
                ).transact({'from': st.session_state.seller, 'gas': 1000000})
                receipt = w3.eth.waitForTransactionReceipt(tx_hash)

            # create countdown and timer
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

            # if counter still above 1 run the counter down
            if st.session_state.counter_auction>0:                   
                with placeholder_1.container():
                    st.markdown('##### Auction Count-down')
                    st.subheader(f'**:green[{time_now}]**')
                with placeholder_4.container():
                    st_lottie(lottie_json_auction, width=180, key = str(st.session_state.time_sec))
            else:
                # when auction is over call end function of auction contract
                if st.session_state.ended:
                    # end auction function
                    st.session_state.ended = not st.session_state.ended
                    tx_hash = contract_auction.functions.end().transact({'from': st.session_state.seller, 'gas': 1000000})
                    receipt = w3.eth.waitForTransactionReceipt(tx_hash)

                # show that auction ened
                with placeholder_1.container():
                    st.markdown('##### Auction ended. Withdraw bids within:')
                    st.subheader(f'**:red[{time_now_w}]**')
                placeholder_4.empty()
           

            time.sleep(1)

        st.balloons()
        st.markdown("#### **:orange[Auction closed!]**")

        # st.session_state.in_progress = not st.session_state.in_progress
        st.session_state.started = not st.session_state.started
        st.session_state.ended = not st.session_state.ended
        st.session_state.set_seller = not st.session_state.set_seller

    # remove current session states
    del st.session_state.started
    del st.session_state.ended
    del st.session_state.set_seller
    del st.session_state.highestbid
    del st.session_state.highestbidder
    del st.session_state.seller
    del st.session_state.time_sec
    del st.session_state.counter_auction


