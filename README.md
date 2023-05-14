# FinTech Project 3 
# Digital Art

This application offers digital art creators a one-step full solution from minting and registering their digital art to putting the art pieces on the auction.</br>
The simple user friendly interface of the applcation allows a user to first mint and register his/her art piece. Once the NFT is minted and registered, we utilize Pinata services to store the newly created contracts in a decentralized manner. </br>
After minting and registering their art, the creator can right away put it on the decentralized marketplace. The auction runs for a certain time period within which the bidders can place their bids and, where the highest bid and the highest bidder are identified after each bid. The bid withdrawl is also available to the bidders who are not identified as the highest bidder. The withdrawl is open during as well as some additional time after the auction's closing.</br>
Once the auction has ended, the NFT will have changed the ownership and be transferred to the highest bidder, if any, while the highest bid will have been transferred to the seller.

---
![Digital Art](Images/robo.jpg)
---

## Table of contents

1. [Technologies](#technologies)
2. [Installation Guide](#installation-guide)
3. [Usage](#usage)
4. [Contributors](#contributors)
5. [License](#license)

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

   -[attributedict](https://pypi.org/project/attributedict/) - to read about available functions and installation.<br/>

7. `requests` with the requests library, you can easily send HTTP requests to web servers and APIs. 

   - [requests](https://pypi.org/project/requests/) - to read about available functions and installation.<br/>

8. `JSON` the json library is used to encode and decode data in JSON (JavaScript Object Notation) format. 

   - [JSON](https://docs.python.org/3/library/json.html) - to read about available functions and installation.<br/>

9. `math` library provides access to the mathematical functions defined by the C standard.

   - [math](https://docs.python.org/3/library/math.html) - to read about available functions and installation.<br/>

10. `pathlib` This module offers classes representing filesystem paths with semantics appropriate for different operating systems.

   - [pathlib](https://docs.python.org/3/library/pathlib.html) - to read about available functions and installation.<br/>

* The requests, JSON, math and pathlib libraries come installed with Anaconda. To verify, in Terminal type:

```python
conda list | grep -E 'requests|json|math|pathlib'

```
---

## Installation Guide

The application can be started from the terminal using Streamlit, once in the directory of the application and all the required libraries and the application are installed.  (see instructions below):<br/>

```python
streamlit run app.py
```
### Library Installations

Install each of the below libraries:<br/>

1. To install pandas run:

```python
pip install pandas
```
```python
# or conda
conda install pandas
```

2. To install Streamlit, in Terminal run:

```python
pip install streamlit
```
Confirm the installation of the Streamlit package by running the following commands in Terminal:

```python
 conda list streamlit
```

3. To install Streamlit Lottie in Terminal run:

```python
pip install streamlit-lottie
```
Confirm the installation of the Streamlit-lottie package by running the following commands in Terminal:

```python
 conda list streamlit-lottie
```

4. To install dotenv in Terminal run:

```python
pip install python-dotenv
```
Confirm the installation of the dotenv package by running the following commands in Terminal:

```python
 conda list python-dotenv
```

5. To install web3 in Terminal run:

```python
pip install web3
```
Confirm the installation of the web3 package by running the following commands in Terminal:

```python
 conda list web3
```

6. To install attributedict in Terminal run:

```python
pip install attributedict
```
Confirm the installation of the math package by running the following commands in Terminal:

```python
 conda list attributedict
```

If Requests, JSON math or Pathlib libraries are missing, in Terminal run:

```python
conda install -c anaconda requests
conda install -c jmcmurray json
conda install math
conda install pathlib

```

### Software Installation
Once all the libraries are installed please Install following software:

#### Ganache
Ganache is a program that allows you to set up a local blockchain, which you can be used to test and develop smart contracts.
1. Eownload the latest version of Ganache and then create a Ganache workspace throught this link [Ganache download page](https://trufflesuite.com/ganache/)
2. Once installed please open Ganache and create a workspace by clicking Quickstart Ethereum. 
![Ganache_Quickstart](Images/Ganache_quickstart.jpg)
3. Open Sample.env file in the cloned folder and use the RPC SERVER address from Ganache as input for the WEB3_PROVIDER_URI address in the Sample.env file and save Sample.env file. 

### Web Services

#### Remix IDE
Remix IDE is used to build and test smart contracts created in Solidity. For this project the web version of Remix IDE can be used
1. Open Remix IDE by clicking the following link [REMIX IDE](https://remix.ethereum.org/)
2. Select solidity in the featured plugins area
![Remix_Solidity](Images/Remix_solidity.jpg)

#### Pinata
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
![Pinata_API_Keys](Images/Pinata_API.jpg)
9. Open Sample.env file in the cloned folder and copy the Pinata API KEY and SECRET KEY in the Sample.env file and save Sample.env file. 





Copy the provided SAMPLE.env file to a new file named .env, and then add the missing data to the environment variables.

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