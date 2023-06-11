      
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import os
import json
from web3 import Web3, HTTPProvider
import ipfshttpclient as  ips
import os
from django.core.files.storage import FileSystemStorage
import pickle
deployed_contract = '0xD35b45888cd906c66E39984DD2438477E95F7e8c'
def getpoduct_function(lefn):
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #ecommerce contract code
    deployed_contract_address = deployed_contract #hash address to access student contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
   
    details = contract.functions.getProduct().call()  
    print(details)

    objects = []
    rows = details.split("\n")
    x = len(rows)-1
    if lefn != 0:
        if x >lefn:
            x =lefn

        
  
        
    for i in range(x):
        arr = rows[i].split("#")
        # print("my=== "+str(arr[0])+" "+arr[1]+" "+arr[2]+" ")
        if arr[0] == 'addproduct':
               
            obj = {
                    "supplier": arr[1],
                    "productname": arr[2],
                    "prize": arr[3],
                    "qty": arr[4],
                    "desc":arr[5],
                    "img":"http://127.0.0.1:8000/media/shop/images/7v3hvjcixb14y1zhw9pd.jpg"
                } 
            # print(arr,obj)

            objects.append(obj)
    print(objects)
    return objects

details = ""

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #ecommerce contract code
    deployed_contract_address = deployed_contract #hash address to access student contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getUser().call()
    if contract_type == 'addproduct':
        details = contract.functions.getProduct().call()
    if contract_type == 'bookorder':
        details = contract.functions.getOrder().call()    
    print(details)   

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #ecommerce contract file
    deployed_contract_address = deployed_contract #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.addUser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'addproduct':
        details+=currentData
        msg = contract.functions.addProduct(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'bookorder':
        details+=currentData
        msg = contract.functions.bookOrder(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)