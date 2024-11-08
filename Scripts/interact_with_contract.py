import os
import json
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware

# Load environment variables from .env file
load_dotenv()

# Connect to the Ethereum network (Rinkeby or Ropsten)
infura_url = os.getenv('INFURA_URL')
w3 = Web3(Web3.HTTPProvider(infura_url))

# Ensure we are connected
if not w3.isConnected():
    print("Failed to connect to the Ethereum network.")
    exit()

# Inject the Geth PoA middleware if using Rinkeby or Ropsten
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# Set up your account and private key
private_key = os.getenv('PRIVATE_KEY')
account = w3.eth.account.privateKeyToAccount(private_key)
address = account.address

# Read the compiled contract's ABI and bytecode
with open('contracts/BillOfRights.json') as f:
    compiled_contract = json.load(f)
    abi = compiled_contract['abi']
    bytecode = compiled_contract['bytecode']

# Set up the contract
BillOfRights = w3.eth.contract(abi=abi, bytecode=bytecode)

# Build the transaction
transaction = BillOfRights.constructor().buildTransaction({
    'from': address,
    'gas': 5000000,
    'gasPrice': w3.toWei('20', 'gwei'),
    'nonce': w3.eth.getTransactionCount(address),
})

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined
txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

print(f'Contract deployed at address: {txn_receipt.contractAddress}')