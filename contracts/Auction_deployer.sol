// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.4;

import "./NftRegister_2.sol";
// import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

//ensure we have thoe two functions available in our contract
// the functions are inherent to ERC721 tokens
// interface IERC721 {
//     function transfer(address, uint) external;
//     function transferFrom(
//         address,
//         address,
//         uint
//     ) external;
// }

contract Auction {

    // define the events for the auction:
    event Start();
    event End(address highestBidder, uint highestBid);
    event Bid(address indexed sender, uint amount);
    event Withdraw(address indexed bidder, uint amount);

    // define the address of the NFT seller:
    address payable public seller;

    // is auction started or ended?
    bool public started;
    bool public ended;
    uint public endAt;

    //declaring nft:
    //token is the address of our nft contract
    IERC721 public token;
    uint public tokenId;

    // highest bid and highest bidder:
    uint public highestBid;
    address public highestBidder;

    //mapping between the bidder's address and the bids they make:
    mapping(address => uint) public bids;

    // constructor (){
    //     //the deployer of the contract is the seller of the NFT's
    //     // seller = payable(msg.sender);
    // }

    // modifier:
    modifier onlySeller() {
        require(msg.sender == payable(seller), "Only seller can start the auction");
        _;
    }

    modifier inProgress() {
        //make sure the auction is in progress already:
        require(started && !ended, "Auction has to be  in progress!");
        _;
    }

    //set seller
    function setSeller(address payable _seller) public {
        seller = _seller;
    }
    //starting the auction by the seller:
    function start(IERC721 _token, uint _tokenId, uint startingBid) external onlySeller{
        //make sure the auction is not in progress already:
        require(!started, "Auction in progress!");
       
        // initializing the highest bid:
        highestBid = startingBid;

        //assigning values to nft:
        token = _token;
        tokenId = _tokenId;

        //  transfer nft to the contract:
        token.transferFrom(msg.sender, address(this), tokenId);

         //start the auction
        started = true;
        ended= false;
        // define the end time of the auction:
        endAt = block.timestamp + 2 minutes;

        //emitting the event:
        emit Start();
    }
    
    //bidding during the auction:
    function bid() external payable {
        // make sure the auction is not finalized before the agreed time:
        require(block.timestamp < endAt, "Auction ended");
        // the bid has to be higher than the latest bid:
        require(msg.value < msg.sender.balance, "The bid has to be higher than the highest bid to be accepted");

        //new balance of the bidder:
        bids[msg.sender] += msg.value;
        // set the new highest bid and bidder:
        if(bids[msg.sender] > highestBid) {
            highestBid = msg.value;
            highestBidder = msg.sender;
        }
        // emitting Bid event:
        emit Bid(highestBidder, highestBid);
    }

    function withdraw() external payable {
        require(msg.sender != highestBidder, "highest bidder cannot withdraw");
        // get the balance of the bidder within the contract
        uint balanceBidder = bids[msg.sender];
        // set the balance to 0 before withrawal:
        bids[msg.sender] = 0;
        //withdraw from the contracts:
        payable(msg.sender).transfer(balanceBidder);
        // (bool sent, bytes memory data) = payable(msg.sender).call(value: balanceBidder).("");
        // require(sent, "Could not withdraw");
        // emitting Withdraw event:
        emit Withdraw(msg.sender, balanceBidder);

    }

    //eending the auction:
    function end() external inProgress onlySeller {
        // //make sure the auction is in progress already:
        // require(started || !ended, "Auction has to be  in progress!");
        // make sure the auction is not finalized before the agreed time:
        require(block.timestamp >= endAt, "Auction is still running");
        
        //check if there was any bids   
        if (highestBidder != address(0)){
            // if yes, transfer nft: to the highest bidder
            token.transferFrom(address(this), highestBidder, tokenId);
            // token.transfer(highestBidder, tokenId);

            //and the highest bid to the seller:
            payable(seller).transfer(highestBid);
            // (bool sent, bytes memory data) = payable(seller).call(value: highestBid).("");
            // require(sent, "Could not pay seller");
        } else{
            //transfer back to seller
            token.transferFrom(address(this), payable(seller),  tokenId);
            // token.transfer(seller, tokenId);
        }
        //  ending the auction:
        ended= true;
        started = false;
        //emitting the event:
        emit End(highestBidder, highestBid);
    }
}

contract AuctionDeployer {
     // Create an `address public` variable called `kasei_token_address`.
    address public NFTRegistery_address;
    // Create an `address public` variable called `kasei_crowdsale_address`.
    address public auction_address;

    // Add the constructor.
    constructor() {
        // Create a new instance of the Artregistry contract.
        NFTRegistery token = new NFTRegistery();
        // Assign the token contract’s address to the `kasei_token_address` variable.
        NFTRegistery_address = address(token);

        // Create a new instance of the `KaseiCoinCrowdsale` contract
        Auction nft_auction = new Auction();
            
        // Aassign the `KaseiCoinCrowdsale` contract’s address to the `kasei_crowdsale_address` variable.
        auction_address = address(nft_auction);

        // Set the `Auction` contract as a minter
        // token.addMinter(auction_address);
        
        // Have the `AuctionDeployer` renounce its minter role.
        // token.renounceMinter();
    }
}
