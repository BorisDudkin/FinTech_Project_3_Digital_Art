// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

// store URI of meta data file in blockchain storage itself
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

// create contract for registering NFTs and minting tokens during registration using ERC721 URIStorage
contract NFT_reg is ERC721URIStorage, ReentrancyGuard{
    //
    uint public tokenSupply;
    constructor() ERC721("BN Art Token", "BNAT") {}

    // create required input structure for NFT Name, artwork and minimum auction price. 
    struct NFT_struct {
        string name;
        string artist;
        uint256 auctionMinimum;

    }
    // map NFT structure to NFTMetaData
    mapping(uint256 => NFT_struct) public NFTMetaData;

    // create register NFT function including minting and token supply count
    function registerNFT(
        address owner,
        string memory name,
        string memory artist,
        uint256 initialAuctionMinimum,
        uint256 _tokenId,
        string calldata _uri
    ) external returns (uint256) {
        tokenSupply ++;
        
        require(initialAuctionMinimum >0,"price must be greater than zero");
        
        _mint(owner,_tokenId);
        _setTokenURI(_tokenId, _uri);

        NFTMetaData[_tokenId] = NFT_struct(name, artist, initialAuctionMinimum);

        return(_tokenId);
    }
}

