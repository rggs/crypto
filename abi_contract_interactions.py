#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 19:42:25 2020

@author: dreadkermit
"""

from web3 import Web3
import requests
import numpy as np
import time
import sys
import pickle
import json

print('web3 test:')
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f5f96a3d1bc34551afddb89fdc77bbbe'))

print(str(web3.eth.blockNumber))

api_key = '7N9YT4A7X2MPWHXFSHR32XMUSIENRANXKJ'

factory = web3.eth.contract(address='0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95', 
        abi=requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address=0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95',
                     params={'apikey':api_key}).json()['result'])

num_tokens = factory.functions.tokenCount().call()

uni_tokens = []

for i in range(num_tokens+1):
    add = None
    while add is None:
        try:
            add = factory.functions.getTokenWithId(i).call()
        except:
            pass
    
    sys.stdout.write('\r'+add+'                                    ')
    sys.stdout.flush()
    
    uni_tokens.append(add)



def getABI(adr):
    r = requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address='+adr,
                     params={'apikey':'api_key'}).json()['result']
    
    return r


LIST=[]
for t in uni_tokens:
    addy = t
    types=['bytes32', 'string', 'bytes8']
    
    abi = getABI(t)
    
    generic_abis = [json.loads(
        '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"'+str(b)
        +'"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501
            for b in types]
    
    if t =='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
        symbol='WETH'
    else:  
        symbol='Error'
    
    # EIP20_ABI = json.loads(
    #     '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"'+str(types[0])
    #     +'"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501
    
    if 'Contract source code not verified' in abi:
        for a in generic_abis:
            try:
                symbol = web3.eth.contract(address=addy, abi=a).functions.symbol().call()
            except:
                pass
    else:
        try:
            symbol = web3.eth.contract(address=addy, abi=abi).functions.symbol().call()
        except:
            for a in generic_abis:
                try:
                    symbol = web3.eth.contract(address=addy, abi=a).functions.symbol().call()
                except:
                    pass
    
    if not isinstance(symbol,str):
        symbol=symbol.decode('utf-8').rstrip('\x00')
    
    LIST.append([symbol, addy, abi])
    sys.stdout.write('\r'+symbol+', '+str(uni_tokens.index(t))+'                                    ')
    sys.stdout.flush()
    
    time.sleep(0.21) #DODGE THE ETHERSCAN API LIMIT
    
    
    
LIST = np.array(LIST, dtype='str')
np.savetxt('LIST.csv', LIST, delimiter=',', fmt='%s')

mask = np.ones(len(LIST), dtype = bool)
for token in LIST:
    locs = np.where(LIST[:,0] == token[0])
    if len(locs[0]) > 1:
        mask[locs[0][1:]] = False
        
new_list = LIST[mask]
np.savetxt('Refined_Token_List.csv', new_list, delimiter='/t', fmt='%s')


def genContractDict(abi_list):
    contracts = {}
    print('Creating contracts dictionary')
    for t in abi_list:
        sys.stdout.write('\r'+'Getting contract for: '+t[0]+'                                    ')
        sys.stdout.flush()
        
        #checksum_adr = Web3.toChecksumAddress(cont[1])
        
        exch_add = factory.functions.getExchange(t[1]).call()
        
        contracts[t[0]]={'token':t[0], 'exch_add':exch_add}
        
        # if t[0] != 'ETH':
        #     abi = getABI(exch_add)
        #     contract = web3.eth.contract(address=exch_add, abi=abi)
        #     contracts[t[0]]={'token':t[0], 'contract':contract}
        # else:
        #     contracts[t[0]]={'token':t[0], 'contract':t[2]}
            
        #time.sleep(0.21)
        
    with open('contracts_dict.pickle', 'wb') as handle:
        pickle.dump(contracts, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    print('Successfully saved contracts dictionary')
        
    return contracts

contract_dict = genContractDict(new_list)

print('Done')


        
        
    
