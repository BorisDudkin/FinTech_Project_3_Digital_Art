import time
from pathlib import Path

import requests
import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
from streamlit_option_menu import option_menu

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
        with open(Path('./contracts/compiled/NFT_registry_abi_token.json')) as f:
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

    st.title("Art Registration, mint your token")
    st.write("Choose an account to get started")
    accounts = w3.eth.accounts
    address = st.selectbox("Select Account", options=accounts)
    st.markdown("---")

    # Register New Artwork
    st.markdown("## Register New Artwork")
    artwork_name = st.text_input("Enter the name of the artwork")
    artist_name = st.text_input("Enter the artist name")
    initial_appraisal_value = st.number_input("Enter Auction Starting Bid")
    file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
    art_list = []
    if 'auction_list' not in st.session_state:
        st.session_state['auction_list'] = art_list
    # else:
    #     art_list=st.session_state['auction_list']

    if st.button("Register Artwork"):
        artwork_ipfs_hash = pin_artwork(artwork_name, file)
        artwork_uri = f"ipfs://{artwork_ipfs_hash}"
        image_ipfs_hash = pin_image(file)

        # create token ID for this contract
        token_id = contract.tokenSupply().call()
        st.write(token_id)

        tx_hash = contract.functions.registerArtwork(
            address,
            artwork_name,
            artist_name,
            int(initial_appraisal_value),
            artwork_uri
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.markdown("---")

        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
        st.write("Your uploaded artwork:")
        #st.markdown(f"![Artwork Link](https://gateway.pinata.cloud/ipfs/{image_ipfs_hash})")

        #st.write("1",st.session_state['auction_list'])

        #  temporary tokenId:
        token_id= 0

        # crete a dictionary with the new art work
        art_dict ={}
        art_dict["artwork_name"] = artwork_name
        art_dict["author"] = artist_name
        art_dict["init"] = initial_appraisal_value
        art_dict["last_bid"] = 0
        art_dict["image"] = image_ipfs_hash
        art_dict["token_id"] = token_id
        art_list=st.session_state['auction_list']
        art_list.append(art_dict)
        
        st.session_state['auction_list'] = art_list
        st.write(art_list)


        #st.write("2",st.session_state['auction_list'])
        
        #df = pd.DataFrame(art_list, columns=['artwork_name', 'artist_name', 'init', 'image'])
        #art_dict.append(art_dict)

        #if art_dict not in st.session_state:
        #    st.session_state.art_dict = art_dict
        #st.write(df)

        st.markdown("---")

        #art_list.append(nft_info_dict)
    #st.write("current data:", art_dict)
    


    # art_list=[{'artwork_name': 'The Lake', 'author': "Boris",'init': 1.5, 'last_bid': 0, 'image': "https://www.andrisapse.com/prints/2281.jpg"},
    #    {'artwork_name': 'Sunshine', 'author': "Boris",'init': 1.1, 'last_bid': 0, 'image': "https://docs.gimp.org/en/images/tutorials/quickie-jpeg-100.jpg"}]
    
#    if 'auction_list' not in st.session_state:
#        st.session_state['auction_list']=art_list

######
# Niels
######


    auction=st.button("Start new auction?")
    if auction:
        if "load_state" not in st.session_state:
            st.session_state.load_state = True

if selected == '💰 Auction':
    st.title('💰 Auction Your Artwork')
    st.write("---")
    count_art = 0
    # artwork_name= 'The Lake'
    # author = "Boris"
    # init_value = 1.5
    # last_bid = 1.6

    #st.write("3",st.session_state['auction_list'])

    if 'auction_list' not in st.session_state:
        st.info("### :magenda[There are no items to auction at the momement!]")
    else:
        art_list=st.session_state['auction_list']

    #st.write("4",st.session_state['auction_list'])

    if "load_state" not in st.session_state:
            st.session_state.load_state = False
    # auction=st.button("Start new auction?")
    # if "load_state" not in st.session_state:
    #         st.session_state.load_state = False
    auction = st.session_state.load_state
    if auction:
        while len(art_list)>0:
        # for art in art_list:
            art = art_list.pop(0)
            count_art +=1

            time_sec = 60
            
            col1, col2, col3 = st.columns([1,3,2], gap='large')
            # my_form = st.form(key="Characteristics)")
            # with st_lottie_spinner(lottie_json_auction, height=100):
                
            with col2:
                placeholder_2= st.empty()
                with placeholder_2.container():
                    st.write(f"#### {art['artwork_name']}", key = 'name'+ str(count_art))
                    
                    st.markdown(f"![Art](https://gateway.pinata.cloud/ipfs/{art['image']})")
                    
                    #st.image(art['image'])
                    st.write(f"by: {art['author']}", key = 'author'+ str(count_art))
                    st.write(f"Initial Value: **:blue[{art['init']}]** ETH", key = 'Initial_value'+ str(count_art))
                    st.write(f"Last Bid: **:blue[{art['last_bid']}]** ETH", key = 'last_bid'+ str(count_art))
                    # st.write(f"My name {art['init']}", key = "Initial_value"+ str(count_art))

            with col1:
                placeholder_1= st.empty()
                    # count_header=st.empty()
                    # time_header=st.empty()

            with col3:
                placeholder_3= st.empty()
                with placeholder_3.container():
                    st.write('#')
                    st.write('#')
                    my_form = st.form(key="bidder"+ str(count_art))
                    my_form.subheader('Bid')
                    my_form.text_input("Bidder's address")
                    my_form.number_input("Bid (in ETH)")
                    my_form.form_submit_button('Place order')

            while time_sec:
                    
                time_sec-=1
                mins, secs = divmod(time_sec, 60)
                time_now = '{:02d}:{:02d}'.format(mins, secs)
                with placeholder_1.container():
                    st.markdown('#### Count-down')
                    st.subheader(f'**:green[{time_now}]**')
                    st_lottie(lottie_json_auction, height=180, key = str(time_sec)+str(count_art))
                    # my_form.subheader('The Lake')
                    # my_form.image("https://www.andrisapse.com/prints/2281.jpg")
                    # my_form.text_input("The address", key = time_sec)
                    # my_form.form_submit_button('Submit your selections for price prediction')
                time.sleep(1)
                    # time_sec-=1
            placeholder_1.empty()
            placeholder_2.empty()
            placeholder_3.empty()
            st.balloons()
        st.markdown("#### **:red[All auction ended!]**")
            # time.sleep(5)
            