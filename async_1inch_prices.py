#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 14:22:42 2020

@author: dreadkermit
"""
from web3 import Web3
import requests
from concurrent.futures import ProcessPoolExecutor as PoolExecutor
from concurrent.futures import ThreadPoolExecutor
import sys
import pickle
import time
import asyncio
import nest_asyncio

print('web3 test:')
web3 = Web3(Web3.HTTPProvider('PUT YOUR HTTP PROVIDER HERE'))

print(web3.eth.blockNumber)

eth_add = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

inch = Web3('https://api.1inch.exchange/v3.0/')

exchanges = requests.get('https://api.1inch.exchange/v3.0/1/exchanges').json()
tokens = requests.get('https://api.1inch.exchange/v3.0/1/tokens').json()['tokens']

print("Comparing all Pairs: ")

def getPath(tok1, tok2, excludeExch=None, maxSlip=2, amount=1000000000000000000):
    params={'fromTokenAddress':tok1, 'toTokenAddress':tok2,'amount':amount}  
    path = None
    y=0
    while path is None and y<100:
        try:
            path=requests.get('https://api.1inch.exchange/v3.0/1/quote', params=params)
        except:
            y+=1
    
    if y==100:
        return{'message':'Error'}
    else:
        return path.json()
    
address='put eth address here'

def swapQuote(tok1, tok2, protocols, maxSlip=2, amount=1000000000000000000, fee=0.5, address=address, dis='true'):
    params={'fromTokenAddress':tok1, 'toTokenAddress':tok2,'amount':amount, 'protocols':protocols}
            
    
    txn = None
    y=0
    while txn is None and y<100:
        try:
            txn=requests.get('https://api.1inch.exchange/v3.0/1/quote', params=params)
        except:
            y+=1
    if y==100:
        return{'message':'Error'}
    else:
        return txn.json()
    
one_eth=1000000000000000000

def probe_token(tok1, tok2):
    arb = None
    if tok1 != tok2:
        sys.stdout.write('\r'+ str(tok1)+' '+ str(tok2))
        sys.stdout.flush()
        
        amount=one_eth
        if tok1 != eth_add and tok2 != eth_add:
            toeth = swapQuote(eth_add, tok1)
            amount = int(toeth['toTokenAmount'])
            ethgas1=float(toeth['estimatedGas'])

        ideal = getPath(tok1, tok2)
        id_exch=None
        other_exch = ''
        if 'message' not in ideal:
            try:
                for ex in ideal['protocols'][0]:
                    if ex[0]['part']!=100:
                        other_exch+=ex[0]['name']+','
                    else:
                        id_exch+=ex[0]['name']+','
            except:
                pass
                
        if id_exch is not None:
            forward = swapQuote(tok1, tok2, protocols=other_exch, amount = amount)
            
            if 'message' in forward and forward['message']=='Error':
                pass
            else:
                gas1=forward['estimatedGas']
                first_trx = int(forward['toTokenAmount'])
                back = swapQuote(tok2, tok1,protocols = id_exch, amount=first_trx )
                if 'message' in back and back['message']=='Error':
                    pass
                else:
                    old_trx = float(back['toTokenAmount'])
                    gas2=back['estimatedGas']
                    
                if tok1 != eth_add and tok2 != eth_add:
                    back2eth = swapQuote(tok1, eth_add)
                    final = float(back2eth['toTokenAmount'])
                    ethgas2 = float(back2eth['estimatedGas'])
                else:
                    final = old_trx
                    ethgas1 = 0
                    ethgas2 = 0
                    
                    if ((final-float(gas1)-float(gas2)-ethgas1 - ethgas2)/one_eth)-1 > 0.05:
                        print('\n'+'Arbitrage Found!')
                        arb = {'first_token': tok1, 'second_token': tok2, 
                                           'profit': ((old_trx-float(gas1)-float(gas2))/one_eth)-1}
                        print(arb)
    if arb is not None:
        return arb
    else:
        return {'first_token': tok1, 'second_token': tok2, 
                                           'profit': -1}
                    
    
async def asynch_search():
    arbitrages=[]
    names=[i for i in tokens]


    arbitrages=[]
    majors=['ETH','USDT','DAI','USDC', 'BAL', 'COMP', 'UNI', 'LEND']

    
    #wETH Address:
    tok1='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    coros = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        tasks = [coros.run_in_executor(executor, probe_token, *(tok1, tok2)) for tok2 in names]
        
        for response in await asyncio.gather(*tasks):
            arbitrages.append(response)
            
    return arbitrages

def main():
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(asynch_search())
    arbitrages = loop.run_until_complete(future)
    with open('arbitrages.pkl', 'wb') as file:
        pickle.dump(arbitrages, file)
        
main()