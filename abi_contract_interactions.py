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
web3 = Web3(Web3.HTTPProvider('YOUR HTTP PROVIDER HERE'))

print(str(web3.eth.blockNumber))

api_key = 'YOUR ETHERSCAN API KEY HERE'

factory = web3.eth.contract(address='0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f', 
        abi=requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address=0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
                     params={'apikey':api_key}).json()['result'])

num_tokens = factory.functions.allPairsLength().call()

uni_tokens = []

for i in range(num_tokens+1):
    add = None
    while add is None:
        try:
            add = factory.functions.allPairs(i).call()
        except:
            pass
    
    sys.stdout.write('\r'+add+'                                    ')
    sys.stdout.flush()
    
    uni_tokens.append(add)



def getABI(adr):
    r = requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address='+adr,
                     params={'apikey':api_key}).json()['result']
    
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
    
    if t =='0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
        symbol='ETH'
    else:  
        symbol='Error'
    token0 = 'Error'
    token1 = 'Error'
        
    if 'Contract source code not verified' in abi:
        for a in generic_abis:
            try:
                token0 = web3.eth.contract(address=addy, abi=a).functions.token0().call()
                token1 = web3.eth.contract(address=addy, abi=a).functions.token1().call()
                # symbol = web3.eth.contract(address=addy, abi=a).functions.symbol().call()

            except:
                pass
    else:
        try:
            token0 = web3.eth.contract(address=addy, abi=abi).functions.token0().call()
            token1 = web3.eth.contract(address=addy, abi=abi).functions.token1().call()
            # symbol = web3.eth.contract(address=addy, abi=a).functions.symbol().call()

        except:
            for a in generic_abis:
                try:
                    # symbol = web3.eth.contract(address=addy, abi=a).functions.symbol().call()
                    token0 = web3.eth.contract(address=addy, abi=a).functions.token0().call()
                    token1 = web3.eth.contract(address=addy, abi=a).functions.token1().call()
                except:
                    pass
    
    if not isinstance(token0,str):
        token0=token0.decode('utf-8').rstrip('\x00')
        token1=token1.decode('utf-8').rstrip('\x00')
        
    symbol0 = requests.get('https://api.etherscan.io/api?module=account&action=tokentx&contractaddress='+token0,
             params={'apikey':api_key}).json()['result'][0]['tokenSymbol']
    symbol1 = requests.get('https://api.etherscan.io/api?module=account&action=tokentx&contractaddress='+token1,
             params={'apikey':api_key}).json()['result'][0]['tokenSymbol']
    
    LIST.append([symbol0+'/'+symbol1, addy, abi])
    sys.stdout.write('\r'+symbol0+'/'+symbol1+', '+str(uni_tokens.index(t))+'                                    ')
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
        
        
    with open('contracts_dict.pickle', 'wb') as handle:
        pickle.dump(contracts, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    print('Successfully saved contracts dictionary')
        
    return contracts

contract_dict = genContractDict(new_list)

print('Done')



       
        
        
    
