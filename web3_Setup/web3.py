from web3 import Web3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to the Ethereum network (Infura or local node)
infura_url = os.getenv('INFURA_URL')
w3 = Web3(Web3.HTTPProvider(infura_url))

# Check the connection
if not w3.isConnected():
    print("Failed to connect to Ethereum network")
else:
    print("Connected to Ethereum network")

# Return the Web3 instance
def get_web3_instance():
    return w3
