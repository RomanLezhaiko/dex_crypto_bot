import os
import time
import json

from dotenv import load_dotenv
from web3 import Web3
import requests

from db import Session
from models import Pair, Token


load_dotenv()

debug = os.getenv('DEBUG')
node_rpc = os.getenv('NODERPC')
factory_address = os.getenv('FACTORY_ADDRESS')
api_key_bsc_scan = os.getenv('API_KEY_BSC_SCAN')

web3 = Web3(Web3.HTTPProvider(node_rpc))
print(f"Is connected: {web3.is_connected()}")

url = f'https://api.bscscan.com/api?module=contract&action=getabi&address={factory_address}&apikey={api_key_bsc_scan}'
response = requests.get(url)
factory_abi = response.text
json_object = json.loads(factory_abi)
factory_abi = str(json_object['result'])
factory_contract = web3.eth.contract(factory_address, abi=factory_abi)

session = Session()
obj = session.query(Pair).order_by(Pair.id.desc()).first()
session.close()
number = ''
try:
    number = obj.pair_number + 1
    print(obj.pair_number)
except AttributeError:
    number = 0


for i in range(number, 100):
    pair_address = factory_contract.functions.allPairs(i).call()
    url = f'https://api.bscscan.com/api?module=contract&action=getabi&address={pair_address}&apikey={api_key_bsc_scan}'
    response = requests.get(url)
    pair_abi = response.text
    json_object = json.loads(pair_abi)
    pair_abi = str(json_object['result'])
    try:
        pair_contract = web3.eth.contract(pair_address, abi=pair_abi)
    except:
        continue
    token_0_address = pair_contract.functions.token0().call()
    token_1_address = pair_contract.functions.token1().call()
    tokens_list = [token_0_address, token_1_address]
    
    session = Session()
    pair = Pair(pair_address=pair_address, pair_abi=pair_abi, pair_number=i)
    session.add(pair)
    print(pair.id)
    time.sleep(1)

    token_name_list = []
    flag_all_clear = True
    
    for j in range(len(tokens_list)):
        url = f'https://api.bscscan.com/api?module=contract&action=getabi&address={tokens_list[j]}&apikey={api_key_bsc_scan}'
        response = requests.get(url)
        token_abi = response.text
        try:
            json_object = json.loads(token_abi)
            token_abi = str(json_object['result'])
            token_contract = web3.eth.contract(tokens_list[j], abi=token_abi)
            token_name = token_contract.functions.name().call()
        except Exception:
            print(tokens_list[j])
            session.rollback()
            break

        token_name_list.append(token_name)
        token = Token(token_name=token_name, token_address=tokens_list[j], token_position=j+1, pair_id=pair.id)
        session.add(token)
        time.sleep(1)

    if flag_all_clear:
        session.commit()
    
    session.close()
                
