from web3 import Web3
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()


class BlockchainService:
    def __init__(self):
        self.rpc_url = os.getenv('POLYGON_RPC_URL', 'https://rpc-mumbai.maticvigil.com')
        self.contract_address = os.getenv('CONTRACT_ADDRESS', '')
        self.private_key = os.getenv('PRIVATE_KEY', '')
        
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        self.contract_abi = [
            {
                "inputs": [
                    {"internalType": "string", "name": "_commodity", "type": "string"},
                    {"internalType": "uint256", "name": "_quantity", "type": "uint256"},
                    {"internalType": "uint256", "name": "_pricePerUnit", "type": "uint256"},
                    {"internalType": "uint256", "name": "_deliveryDate", "type": "uint256"}
                ],
                "name": "createContract",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "_contractId", "type": "uint256"}],
                "name": "signAsBuyer",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "_contractId", "type": "uint256"}],
                "name": "getContract",
                "outputs": [
                    {
                        "components": [
                            {"internalType": "uint256", "name": "id", "type": "uint256"},
                            {"internalType": "address", "name": "farmer", "type": "address"},
                            {"internalType": "address", "name": "buyer", "type": "address"},
                            {"internalType": "string", "name": "commodity", "type": "string"},
                            {"internalType": "uint256", "name": "quantity", "type": "uint256"},
                            {"internalType": "uint256", "name": "pricePerUnit", "type": "uint256"},
                            {"internalType": "uint256", "name": "deliveryDate", "type": "uint256"},
                            {"internalType": "bool", "name": "farmerSigned", "type": "bool"},
                            {"internalType": "bool", "name": "buyerSigned", "type": "bool"},
                            {"internalType": "bool", "name": "settled", "type": "bool"},
                            {"internalType": "uint256", "name": "createdAt", "type": "uint256"}
                        ],
                        "internalType": "struct ForwardContract.Contract",
                        "name": "",
                        "type": "tuple"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getTotalContracts",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "address", "name": "_farmer", "type": "address"}],
                "name": "getFarmerContracts",
                "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "uint256", "name": "contractId", "type": "uint256"},
                    {"indexed": True, "internalType": "address", "name": "farmer", "type": "address"},
                    {"indexed": False, "internalType": "string", "name": "commodity", "type": "string"},
                    {"indexed": False, "internalType": "uint256", "name": "quantity", "type": "uint256"},
                    {"indexed": False, "internalType": "uint256", "name": "pricePerUnit", "type": "uint256"},
                    {"indexed": False, "internalType": "uint256", "name": "deliveryDate", "type": "uint256"}
                ],
                "name": "ContractCreated",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "uint256", "name": "contractId", "type": "uint256"},
                    {"indexed": True, "internalType": "address", "name": "signer", "type": "address"},
                    {"indexed": False, "internalType": "string", "name": "signerType", "type": "string"}
                ],
                "name": "ContractSigned",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "uint256", "name": "contractId", "type": "uint256"},
                    {"indexed": True, "internalType": "address", "name": "farmer", "type": "address"},
                    {"indexed": True, "internalType": "address", "name": "buyer", "type": "address"},
                    {"indexed": False, "internalType": "uint256", "name": "totalValue", "type": "uint256"}
                ],
                "name": "ContractSettled",
                "type": "event"
            }
        ]
        
        if self.contract_address and self.w3.is_address(self.contract_address):
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=self.contract_abi
            )
        else:
            self.contract = None
    
    def is_configured(self):
        """Check if blockchain service is properly configured"""
        return (
            self.contract_address and 
            self.private_key and 
            self.contract is not None and
            self.w3.is_connected()
        )
    
    def create_contract(self, commodity, quantity, price_per_unit, delivery_date_timestamp, farmer_address):
        """
        Create a forward contract on blockchain
        
        Args:
            commodity: Name of commodity (e.g., "Soybean")
            quantity: Quantity in quintals
            price_per_unit: Price per quintal (in smallest currency unit)
            delivery_date_timestamp: Unix timestamp of delivery date
            farmer_address: Ethereum address of the farmer
        
        Returns:
            Transaction hash and contract ID
        """
        if not self.is_configured():
            raise Exception("Blockchain service not configured. Please set CONTRACT_ADDRESS and PRIVATE_KEY in .env")
        
        try:
            account = self.w3.eth.account.from_key(self.private_key)
            
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.createContract(
                commodity,
                quantity,
                price_per_unit,
                delivery_date_timestamp
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            logs = self.contract.events.ContractCreated().process_receipt(receipt)
            contract_id = logs[0]['args']['contractId'] if logs else None
            
            return {
                'success': True,
                'transaction_hash': tx_hash.hex(),
                'contract_id': contract_id,
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed']
            }
            
        except Exception as e:
            raise Exception(f"Error creating contract: {str(e)}")
    
    def sign_contract(self, contract_id, buyer_address):
        """
        Buyer signs a contract
        
        Args:
            contract_id: ID of the contract to sign
            buyer_address: Ethereum address of the buyer
        
        Returns:
            Transaction hash
        """
        if not self.is_configured():
            raise Exception("Blockchain service not configured")
        
        try:
            account = self.w3.eth.account.from_key(self.private_key)
            
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.signAsBuyer(
                contract_id
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': tx_hash.hex(),
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed']
            }
            
        except Exception as e:
            raise Exception(f"Error signing contract: {str(e)}")
    
    def get_contract_details(self, contract_id):
        """
        Get details of a contract
        
        Args:
            contract_id: ID of the contract
        
        Returns:
            Contract details dictionary
        """
        if not self.is_configured():
            raise Exception("Blockchain service not configured")
        
        try:
            contract_data = self.contract.functions.getContract(contract_id).call()
            
            return {
                'contract_id': contract_data[0],
                'farmer_address': contract_data[1],
                'buyer_address': contract_data[2],
                'commodity': contract_data[3],
                'quantity': contract_data[4],
                'price_per_unit': contract_data[5],
                'delivery_date': datetime.fromtimestamp(contract_data[6]).strftime('%Y-%m-%d'),
                'delivery_date_timestamp': contract_data[6],
                'farmer_signed': contract_data[7],
                'buyer_signed': contract_data[8],
                'settled': contract_data[9],
                'created_at': datetime.fromtimestamp(contract_data[10]).strftime('%Y-%m-%d %H:%M:%S'),
                'total_value': contract_data[4] * contract_data[5],
                'status': self._get_contract_status(contract_data[7], contract_data[8], contract_data[9])
            }
            
        except Exception as e:
            raise Exception(f"Error fetching contract details: {str(e)}")
    
    def _get_contract_status(self, farmer_signed, buyer_signed, settled):
        """Determine contract status"""
        if settled:
            return "SETTLED"
        elif farmer_signed and buyer_signed:
            return "SIGNED_BY_BOTH"
        elif farmer_signed:
            return "WAITING_FOR_BUYER"
        else:
            return "PENDING"
    
    def get_total_contracts(self):
        """Get total number of contracts on blockchain"""
        if not self.is_configured():
            return 0
        
        try:
            return self.contract.functions.getTotalContracts().call()
        except:
            return 0
