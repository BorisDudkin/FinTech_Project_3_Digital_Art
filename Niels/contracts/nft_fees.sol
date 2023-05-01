// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

// Import IERC721
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
// Import ReentrancyGuard
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

// define nftfees contract 
contract nftfees is ReentrancyGuard {
    // set Variables for nftfees contract

    // set the account that receives fees
    address payable public immutable feeAccount; 
    // set fees for platform
    uint public immutable feeAmount; 
    // count how many items were listed in total
    uint public itemCount; 

    // use constructor to collect fees from the artist
    constructor(uint _feeAmount) {
        feeAccount = payable(msg.sender);
        feeAmount = _feeAmount;
    }

}