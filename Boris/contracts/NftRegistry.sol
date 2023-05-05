// SPDX-License-Identifier: MIT
pragma solidity ^0.8.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";


// create contract for registering NFTs and minting tokens during registration using ERC721 URIStorage
contract NFTRegistery is ERC721, ERC721URIStorage{
    
    //Calling Counters contract function for _tokenIdCounter
    using Counters for Counters.Counter;
    Counters.Counter public _tokenIdCounter;
    address contractAddress;

    constructor() ERC721("BN Art Token", "BNAT") {}

    // create required input structure for NFT Name, artwork and minimum auction price. 
    struct Artwork {
        string name;
        string artist;
        uint256 appraisalValue;

    }
    // map NFT structure to NFTMetaData
    mapping(uint256 => Artwork) public artCollection;

    // can be removed no need for appraisal. 
    event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    // create register NFT function including minting and token supply count
    function registerArtwork(
        address owner,
        string memory name,
        string memory artist,
        uint256 initialAppraisalValue,
        //uint256 tokenId,
        string memory uri
    ) public returns (uint256) {
        uint256 tokenId = _tokenIdCounter.current();

        // Increment token IDs
        _tokenIdCounter.increment();

        // Mint NFT
        _safeMint(owner, tokenId);

        // Set token URI
        _setTokenURI(tokenId, uri);

        // Add tokenID to AuctionCollection
        artCollection[tokenId] = Artwork(name, artist, initialAppraisalValue);

        // Return registered NFT tokenId
        return tokenId;

    }

    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

        
        
    // below can be removed, no need for new appraisal
    function newAppraisal(
        uint256 tokenId,
        uint256 newAppraisalValue,
        string memory reportURI
    ) external returns (uint256) {
        artCollection[tokenId].appraisalValue = newAppraisalValue;

        emit Appraisal(tokenId, newAppraisalValue, reportURI);

        return artCollection[tokenId].appraisalValue;
    }


}

