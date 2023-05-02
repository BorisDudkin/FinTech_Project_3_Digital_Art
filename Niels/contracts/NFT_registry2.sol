pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract NFTRegistry is ERC721Full {
    constructor() public ERC721Full("BN Art Token", "BNAT") {}

    struct NFT {
        string name;
        string artist;
        string tokenURI;
        //uint256 appraisalValue; // we could make this initial value or minimum required auction value
    }

    mapping(uint256 => NFT) public NFTCollection;

    //event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    function registerNFT(
        address owner,
        string memory name,
        string memory artist,
        //uint256 initialAppraisalValue,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        NFTCollection[tokenId] = NFT(name, artist, tokenURI);

        return tokenId;
    }

}
