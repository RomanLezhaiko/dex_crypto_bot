import os

from dotenv import load_dotenv
from web3 import Web3
import requests


load_dotenv()

debug = os.getenv('DEBUG')
node_rpc = os.getenv('NODERPC')
factory_address = os.getenv('FACTORY_ADDRESS')
api_key_bsc_scan = os.getenv('API_KEY_BSC_SCAN')

print(debug, node_rpc, sep='\n')

web3 = Web3(Web3.HTTPProvider(node_rpc))
print(f"Is connected: {web3.is_connected()}")

url = f'https://api.bscscan.com/api?module=contract&action=getabi&address={factory_address}&apikey={api_key_bsc_scan}'
response = requests.get(url)
ABI = response.text
print(ABI)
print(type(ABI))