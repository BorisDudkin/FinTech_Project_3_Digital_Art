# FinTech Project 3 
# Digital Art

This application offers digital art creators a one-step full solution from minting and registering their digital art to putting the art pieces on the auction.</br>
The simple user friendly interface of the applcation allows a user to first mint and register his/her art piece. Once the NFT is minted and registered, we utilize Pinata services to store the newly created contracts in a decentralized manner. </br>
After minting and registering their art, the creator can right away put it on the decentralized marketplace. The auction runs for a certain time period within which the bidders can place their bids and, where the highest bid and the highest bidder are identified after each bid. The bid withdrawl is also available to the bidders who are not identified as the highest bidder. The withdrawl is open during as well as some additional time after the auction's closing.</br>
Once the auction has ended, the NFT will have changed the ownership and be transferred to the highest bidder, if any, while the highest bid will have been transferred to the seller.

---
![Digital Art](Images/1_robo.jpg)
---

## Table of contents

1. [Technologies](#technologies)
2. [Installation Guide](#installation-guide)
3. [Environment Setup](#Environment-Setup)
4. [Usage](#usage)
5. [Contributors](#contributors)
6. [License](#license)

---

## Technologies
```
Python 3.9
Solidity
Remix IDE
Ganache
Pinata IPFS Storage
```

Python libraries:

1. `Pandas` is a Python package that provides fast, flexible, and expressive data structures designed to make working with large sets of data easy and intuitive.

   - [pandas](https://github.com/pandas-dev/pandas) - for the documentation, installation guide and dependencies.

2. `Streamlit` is a library that allows developers to build web applications with live user input.

   - [Streamlit](https://streamlit.io/) - to read more about deploying, installing and customizing.<br/>

3. `Streamlit-lottie` A Streamlit custom component to load Lottie animations

   - [Streamlit-lottie](https://pypi.org/project/streamlit-lottie/) - to read more about deploying, installing and customizing.<br/>

4. `dotenv` Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. 

   - [dotenv](https://pypi.org/project/python-dotenv/) - to read about available functions and installation.<br/>

5. `web3` is a Python library for interacting with Ethereum

   - [web3](https://pypi.org/project/web3/) - to read about available functions and installation.<br/>
    
6. `attributedict` is library that allows you to access dictionary keys as if they were object attributes. 

   - [attributedict](https://pypi.org/project/attributedict/) - to read about available functions and installation.<br/>

7. `requests` with the requests library, you can easily send HTTP requests to web servers and APIs. 

   - [requests](https://pypi.org/project/requests/) - to read about available functions and installation.<br/>

8. `JSON` the json library is used to encode and decode data in JSON (JavaScript Object Notation) format. 

   - [JSON](https://docs.python.org/3/library/json.html) - to read about available functions and installation.<br/>

9. `math` library provides access to the mathematical functions defined by the C standard.

   - [math](https://docs.python.org/3/library/math.html) - to read about available functions and installation.<br/>

10. `pathlib` This module offers classes representing filesystem paths with semantics appropriate for different operating systems.

      - [pathlib](https://docs.python.org/3/library/pathlib.html) - to read about available functions and installation.<br/>

---

The requests, JSON, math and pathlib libraries come installed with Anaconda. To verify, in Terminal type:

```python
conda list | grep -E 'requests|json|math|pathlib'
```
---

## Installation Guide

Please clone the full repository from github to a project folder.<br/> 
The application can be started from the terminal using Streamlit in the directory of the application after all the required libraries, additional software and the environment setup is completed. (see instructions below):<br/>

```python
streamlit run app.py
```
### Library Installations

Install each of the following libraries (if not installed already):<br/>

To install pandas run:

```python
pip install pandas
```
Confirm the installation of pandas package by running the following commands in Terminal:
```python
conda list pandas
```

To install Streamlit, in Terminal run:

```python
pip install streamlit
```
Confirm the installation of the Streamlit package by running the following commands in Terminal:

```python
 conda list streamlit
```

To install Streamlit Lottie in Terminal run:

```python
pip install streamlit-lottie
```
Confirm the installation of the Streamlit-lottie package by running the following commands in Terminal:

```python
 conda list streamlit-lottie
```

To install dotenv in Terminal run:

```python
pip install python-dotenv
```
Confirm the installation of the dotenv package by running the following commands in Terminal:

```python
 conda list python-dotenv
```

To install web3 in Terminal run:

```python
pip install web3
```
Confirm the installation of the web3 package by running the following commands in Terminal:

```python
 conda list web3
```

To install attributedict in Terminal run:

```python
pip install attributedict
```
Confirm the installation of the math package by running the following commands in Terminal:

```python
 conda list attributedict
```

If Requests, JSON, math or Pathlib libraries are missing, in Terminal run:

```python
conda install -c anaconda requests
conda install -c jmcmurray json
conda install math
conda install pathlib
```

### Software Installation
Once all the libraries are installed please Install following software:

#### **Ganache**
Ganache is a program that allows you to set up a local blockchain, which you can be used to test and develop smart contracts.
1. Download the latest version of Ganache and then create a Ganache workspace throught this link [Ganache download page](https://trufflesuite.com/ganache/)
2. Once installed please open Ganache and create a workspace by clicking Quickstart Ethereum. 

   <img src="./Images/2_Ganache_quickstart.jpg" width=1100 height=600>

3. Open **Sample.env** file in the cloned folder and use the **RPC SERVER** address from Ganache as input for the **WEB3_PROVIDER_URI** address in the Sample.env file and save Sample.env file. 



   <img src="./Images/3_Ganache_Sample_File_update.jpg" width=500 height=200>

* PLEASE NOTE THAT THE RPC SERVER ADDRESS CAN DIFFER FROM THIS EXAMPLE


### **Web Services**

#### **Remix IDE**
Remix IDE is used to build and test smart contracts created in Solidity. For this project the web version of Remix IDE can be used. 
1. Open Remix IDE by clicking the following link [REMIX IDE](https://remix.ethereum.org/)
2. Select solidity in the featured plugins area

   <img src="./Images/4_Remix_solidity.jpg" width=1100 height=600>

#### **Pinata**
Storing data on a chain is expensive. IPFS is a technology that can be used to store and retrieve files from a decentralized system. IPFS distributes each file across multiple nodes in its own network. It breaks down the file into pieces of data and then distributes the pieces across multiple nodes. Smart contracts and dApps can store and retrieve their files directly from the nodes that have the data pieces. This means that they store and access their data by using a decentralized technology—without the expense of storing that data on the chain.
For this dApp Pinata is utilized for IPFS services. 

1. Go to Pinata website [Pinata Website](https://www.pinata.cloud/)
2. Sign up for a free account.
3. Log into the pinata and proceed to the dashboard. 
4. In the developers section please select API keys or access through the following link [Pinata API Keys](https://app.pinata.cloud/developers/api-keys)
5. Please click on + New Key
6. Make sure to click the option to grant Admin privileges for your keys.
7. Please insert a Key Name
8. Click Create Key button
9. Open **Sample.env** file in the cloned folder and copy the Pinata **API KEY** and **SECRET KEY** into the Sample.env file and save Sample.env file. 

   <img src="./Images/5_Pinata_API.jpg" width=750 height=650>

   <img src="./Images/6_Pinata_API_key.jpg" width=500 height=250>
   <img src="./Images/7_Pinata_Secret_key.jpg" width=500 height=250>

---

## Environment Setup

After the installation of all required libraries, software, established access to both web services and updated the **PINATA_API_KEY**, **PINATA_SECRET_API_KEY** with the API information from Pinata and the **WEB3_PROVIDER_URI** with the RPC Server information from GANACHE in the Sample.env file you are ready link all the components together by setting up the environment to run the streamlit app.py application.

Please follow the following steps in the exact sequence described below:

#### Step 1: Ganache
Create a new Ganache workspace
* click Quickstart Ethereum, or if already in a started session click switch button this will bring you back to the starting screen. (Please also see video below)
* Please make sure that the RPC Server Address is the same as the WEB3_PROVIDER_URI in the Sample.env file

   <img src="./Images/8_Step1_Ganache_new_Workspace.gif" width=750 height=550>

#### Step 2: Remix IDE Setup
* Start Remix IDE [REMIX IDE](https://remix.ethereum.org/)
* Select File Explorer
* Create new WorkSpaces and Provide Workspace Name
* Select Upload Folder
* Select contracts folder within the project folder
* Auction_deployer.sol and NFTRegister_2.sol are now availabele within Remix IDE

   <img src="./Images/9_Step2_Remix_IDE_setup.gif" width=750 height=550>

#### Step 3: Compile and Deploy AuctionDeployer Smart Contract in Remix IDE
* Select Auction_deployer.sol contract (by clicking on the contract a new tab will open in remix displaying to solidity code)
* Select Solidity Compiler Icon (Left sidebar)
* Select Pragma Solidity Compiler in COMPILER selextbox (In this project you can use the 0.8.6 and up)
* Select Compile Auction_Deployer.sol (Please wait until check mark appears)
* Select Deploy and Run Transactions icon (left sidebar)
* Select Dev - Ganache Provider in ENVIRONMENT selectbox
* In the Pop-up please provide the correct RPC Server Address
* Select AuctionDeployer in CONTRACT (compile by Remix) selectbox
* Select Deploy -- Auction Deployer Contract should appear in Deployed Contracts Section

   <img src="./Images/10_Step3_Compile_and_Deploy_AuctionDeployer_Smart_Contract.gif" width=750 height=550>

#### Step 4: Deploy Auction Contract and NFT Register Contract (from auction deployer contract)
* In Auction Deployer contract click button Auction_address
* Copy auction address by couble clicking on the address, use right mouse click and copy address.
* Select Auction contract in CONTRACT (compile by Remix) selectbox
* Paste auction address in "At Address" text box and 
* Click "At Address" Button
* Copy NFTRegistry address by couble clicking on the address, use right mouse click and copy address.
* Select NFTRegistry contract in CONTRACT (compile by Remix) selectbox
* Paste NFTRegistry address in "At Address" text box and 
* Click "At Address" Button
* Both Contracts should now be availabe in the Deployed Contracts Section. 

   <img src="./Images/11_Step4_Deploy_Auction_NFTRegistry_Contracts.gif" width=750 height=550>

#### Step 5: Update Sample.env File
* In the Sample.env file please update the **SMART_CONTRACT_AUCTION** with the Auction contract address
* In the Sample.env file please update the **SMART_CONTRACT_NFT_REGISTER** with the NFTRegistery contract address

   <img src="./Images/12_Step5_Update_Sample_with_auction_contract_address.jpg" width=750 height=550>
   <img src="./Images/13_Step5_Update_Sample_with_NFTRegistery_contract_address.jpg" width=750 height=550>

* PLEASE NOTE THAT THE CONTRACT ADDRESSES IN THIS EXAMPLE WILL DIFFER FROM NEWLY DEPLOYED CONTRACTS

* ONCE ALL API KEYS AND ADDRESSES ARE CORRECTLY UPDATED IN THE SAMPLE.ENV FILE, PLEASE SAVE THE SAMPLE.ENV FILE AS **.env**


## Usage

#### Start Streamlit app from Terminal
* From your terminal go to the project folder and type:

```python
streamlit run app.py
```
> Application summary<br/>

This project provides digital artists a decentralized application for minting and registering their digital art and allows artists to put their art pieces on the auction.</br>
The application uses solidity smart contracts and python on the back-end while utilizing streamlit as the Front-end.</br>
Additionally to avoid expensive storage cost on the Etherium blockchain we utilize decentralized storage services offered by Pinata to store the metadata and artwork in a decentralized manner. 

- Home: </br> 
   - Home Section provides information about the project and the project's objective.
   
   <img src="./Images/14_Home_Page.jpg" width=850 height=550>


- Minting and Registration:</br> 
   - The Minting and Registration section provides the Artist with a user friendly way to select their etherium address and upload their artwork in the application.</br> 
   - After uploading the artwork and providing basic information about the artwork, the artist can then register the artwork by pressing the Register Artwork button. 
   - Once the button is pressed the registerArtwork function in the NFT Register smart contract is run and a token that represents the artwork is minted, tokenURI is set and tokenId is emitted</br>
   
   - After minting and registration the Artist gets a preview of the uploaded artwork utilizing Pinata IPFS cloud services and can press the Auction your NFT button.

   **Please see video below for the full demonstation of the Minting and Registration process.**

   <img src="./Images/15_Art_Registration_Mint_token.gif" width=750 height=550>

- Auction:</br> 
   - The auction will run for two minutes in this period interested parties can place their bids throught the bidding portal. 
   - At the start of the auction the setSeller function in the auction smart contract is run and the seller is registered, additionally in the auction contract there is require statement that does not allow the seller to put in bids on their own artwork in a bid to increase the price. 
   - After the seller is set the auction start function is run transferring onwership from the seller to the auction contract so that the auction can handle the settlement of the auction. 
   - During auction period interested parties can place their bids through the bid function in the auction contract. When a bid is placed the auction contract requires that the balance of the bidder is higher than the bid to ensure that the bidder has the funds to purchase the artwork. 
   - During the auction bidders can also withdraw their bids and receive back their funds. For this the auction contract requires that the withdrawing bidder is not the heighest bidder. 
   - Once the auction timer runs out the end function of the auction contract is run to settle the auction. 
   At the end of the auction there are 2 possiblities: 
      1) No bids are received for the artwork, in this case the auction contract transfers the artwork back the seller. 
      2) Bids are are received for the artwork, in this case the auction contract transfers the artwork to the highest bidder and transfers the funds from the bidder to the seller. 
   
   **Please see video below for the full demonstation of the Auction process.**

   <img src="./Images/16_Auction.gif" width=750 height=550>

- Withdrawal Period:</br> 
   - After the auction finishes the application offers an additional time period in which bidders that did not have the highest bid can withdraw their bids and funds are transferred back to the bidder. 
   - During withdrawal period the application does not allow for any new bids. 

   **Please see video below for the full demonstation of the Auction process.**

   <img src="./Images/18_Withdrawal_period.gif" width=750 height=550>

- Final settlements in Remix and Ganache:</br> 
   - Remix IDE Auction Contract:</br>   
      - Below overview displays that the interaction between the Front-End application and the Auction smart contract deployed in Remix IDE was succesfull.
      - Highest Bid, Highest Bidder, Seller, token and TokenID are all correctly updated.</br> 
      <img src="./Images/19_Remix_Auction_Contract_After_Auction.jpg" width=850 height=550>

   - Remix IDE NFTRegister Contract:</br> 
      - Below overview displays that the interaction between the Front-End application and the NFT Register smart contract deployed in Remix IDE was succesfull.
      - ownerOf and tokenURI of BNAT token 0 are correctly updated.</br> 
      <img src="./Images/20_Remix_NFTRegister_after_auction.jpg" width=850 height=550>

   - Ganache:</br>
      - Below overview displays that the interaction between Front-End application and Ganache was succesfull. 
      - Funds are succesfully transferred from highest bidder to seller.</br>  
      <img src="./Images/21_Ganache_after_withdrawal_period.jpg" width=850 height=550> 
    


## Contributors

Contact Details:

Boris Dudkin:
- [Email](boris.dudkin@gmail.com)
- [LinkedIn](www.linkedin.com/in/Boris-Dudkin)

Niels de Haan:
- [Email](nlsdhn@gmail.com)
- [LinkedIn](www.linkedin.com/in/nielsdehaan)
---

## License

MIT

---