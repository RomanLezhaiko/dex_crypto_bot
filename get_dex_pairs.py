import os
import time
import json

from dotenv import load_dotenv
from web3 import Web3
import requests

from db import Session
from models import Pair


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
factory_abi = response.text
json_object = json.loads(factory_abi)
factory_abi = str(json_object['result'])
factory_contract = web3.eth.contract(factory_address, abi=factory_abi)
print('Ok, contract created')

for i in range(100):
    pair_address = factory_contract.functions.allPairs(i).call()
    url = f'https://api.bscscan.com/api?module=contract&action=getabi&address={pair_address}&apikey={api_key_bsc_scan}'
    response = requests.get(url)
    pair_abi = response.text
    json_object = json.loads(pair_abi)
    pair_abi = str(json_object['result'])
    pair_contract = web3.eth.contract(pair_address, abi=pair_abi)
    token_0_address = pair_contract.functions.token0().call()
    token_1_address = pair_contract.functions.token1().call()
    tokens_list = [token_0_address, token_1_address]
    time.sleep(1)

    token_name_list = []
    for token in tokens_list:
        url = f'https://api.bscscan.com/api?module=contract&action=getabi&address={pair_address}&apikey={api_key_bsc_scan}'
        response = requests.get(url)
        token_abi = response.text
        json_object = json.loads(token_abi)
        token_abi = str(json_object['result'])
        token_contract = web3.eth.contract(token, abi=token_abi)
        token_name = token_contract.functions.name().call()
        token_name_list.append(token_name)
        time.sleep(1)
    
    print(' / '.join(token_name_list))
    with Session() as session:
        pair = Pair(token_name_1=token_name_list[0], token_name_2=token_name_list[1])
        session.add(pair)
        session.commit()
                
