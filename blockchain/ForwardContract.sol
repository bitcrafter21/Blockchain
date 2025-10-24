// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ForwardContract
 * @dev Blockchain-based forward contract for oilseed hedging
 * @notice This contract allows farmers and buyers to create and settle forward contracts
 */
contract ForwardContract {
    
    struct Contract {
        uint256 id;
        address farmer;
        address buyer;
        string commodity;
        uint256 quantity;
        uint256 pricePerUnit;
        uint256 deliveryDate;
        bool farmerSigned;
        bool buyerSigned;
        bool settled;
        uint256 createdAt;
    }
    
    uint256 public contractCounter;
    mapping(uint256 => Contract) public contracts;
    
    event ContractCreated(
        uint256 indexed contractId,
        address indexed farmer,
        string commodity,
        uint256 quantity,
        uint256 pricePerUnit,
        uint256 deliveryDate
    );
    
    event ContractSigned(
        uint256 indexed contractId,
        address indexed signer,
        string signerType
    );
    
    event ContractSettled(
        uint256 indexed contractId,
        address indexed farmer,
        address indexed buyer,
        uint256 totalValue
    );
    
    modifier onlyFarmer(uint256 _contractId) {
        require(
            contracts[_contractId].farmer == msg.sender,
            "Only farmer can perform this action"
        );
        _;
    }
    
    modifier onlyBuyer(uint256 _contractId) {
        require(
            contracts[_contractId].buyer == msg.sender,
            "Only buyer can perform this action"
        );
        _;
    }
    
    modifier contractExists(uint256 _contractId) {
        require(
            _contractId > 0 && _contractId <= contractCounter,
            "Contract does not exist"
        );
        _;
    }
    
    /**
     * @dev Create a new forward contract
     * @param _commodity Name of the commodity (e.g., "Soybean")
     * @param _quantity Quantity in quintals
     * @param _pricePerUnit Price per quintal in smallest currency unit
     * @param _deliveryDate Unix timestamp of delivery date
     * @return contractId The ID of the newly created contract
     */
    function createContract(
        string memory _commodity,
        uint256 _quantity,
        uint256 _pricePerUnit,
        uint256 _deliveryDate
    ) external returns (uint256) {
        require(_quantity > 0, "Quantity must be greater than 0");
        require(_pricePerUnit > 0, "Price must be greater than 0");
        require(_deliveryDate > block.timestamp, "Delivery date must be in the future");
        
        contractCounter++;
        
        contracts[contractCounter] = Contract({
            id: contractCounter,
            farmer: msg.sender,
            buyer: address(0),
            commodity: _commodity,
            quantity: _quantity,
            pricePerUnit: _pricePerUnit,
            deliveryDate: _deliveryDate,
            farmerSigned: true,
            buyerSigned: false,
            settled: false,
            createdAt: block.timestamp
        });
        
        emit ContractCreated(
            contractCounter,
            msg.sender,
            _commodity,
            _quantity,
            _pricePerUnit,
            _deliveryDate
        );
        
        emit ContractSigned(contractCounter, msg.sender, "FARMER");
        
        return contractCounter;
    }
    
    /**
     * @dev Buyer accepts and signs the contract
     * @param _contractId ID of the contract to sign
     */
    function signAsBuyer(uint256 _contractId) external contractExists(_contractId) {
        Contract storage c = contracts[_contractId];
        
        require(c.buyer == address(0), "Contract already has a buyer");
        require(c.farmer != msg.sender, "Farmer cannot be the buyer");
        require(!c.settled, "Contract already settled");
        
        c.buyer = msg.sender;
        c.buyerSigned = true;
        
        emit ContractSigned(_contractId, msg.sender, "BUYER");
        
        if (c.farmerSigned && c.buyerSigned) {
            _settleContract(_contractId);
        }
    }
    
    /**
     * @dev Internal function to settle the contract
     * @param _contractId ID of the contract to settle
     */
    function _settleContract(uint256 _contractId) private {
        Contract storage c = contracts[_contractId];
        
        require(c.farmerSigned && c.buyerSigned, "Both parties must sign");
        require(!c.settled, "Contract already settled");
        
        c.settled = true;
        
        uint256 totalValue = c.quantity * c.pricePerUnit;
        
        emit ContractSettled(_contractId, c.farmer, c.buyer, totalValue);
    }
    
    /**
     * @dev Get contract details
     * @param _contractId ID of the contract
     * @return Contract struct containing all contract details
     */
    function getContract(uint256 _contractId) 
        external 
        view 
        contractExists(_contractId) 
        returns (Contract memory) 
    {
        return contracts[_contractId];
    }
    
    /**
     * @dev Get all contracts created by a farmer
     * @param _farmer Address of the farmer
     * @return contractIds Array of contract IDs
     */
    function getFarmerContracts(address _farmer) external view returns (uint256[] memory) {
        uint256[] memory tempIds = new uint256[](contractCounter);
        uint256 count = 0;
        
        for (uint256 i = 1; i <= contractCounter; i++) {
            if (contracts[i].farmer == _farmer) {
                tempIds[count] = i;
                count++;
            }
        }
        
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = tempIds[i];
        }
        
        return result;
    }
    
    /**
     * @dev Get all contracts signed by a buyer
     * @param _buyer Address of the buyer
     * @return contractIds Array of contract IDs
     */
    function getBuyerContracts(address _buyer) external view returns (uint256[] memory) {
        uint256[] memory tempIds = new uint256[](contractCounter);
        uint256 count = 0;
        
        for (uint256 i = 1; i <= contractCounter; i++) {
            if (contracts[i].buyer == _buyer) {
                tempIds[count] = i;
                count++;
            }
        }
        
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = tempIds[i];
        }
        
        return result;
    }
    
    /**
     * @dev Get total number of contracts
     * @return Total contract count
     */
    function getTotalContracts() external view returns (uint256) {
        return contractCounter;
    }
}
