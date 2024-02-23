from web3 import Web3, HTTPProvider
import json

def connect_with_blockchain(acc):
    try:
        # Stage 1: Connecting with RPC server
        rpcServer = "http://127.0.0.1:8045"
        web3 = Web3(HTTPProvider(rpcServer))
        print('Connected with Blockchain')

        # Stage 2: Set default account
        if acc == '0':
            web3.eth.defaultAccount = web3.eth.accounts[0]
        else:
            web3.eth.defaultAccount = acc

        # Stage 3: Load contract ABI and address
        artifacts_path = '../build/contracts/fakeProdDetector.json'
        with open(artifacts_path) as f:
            contract_json = json.load(f)
            contract_abi = contract_json['abi']
            contract_address = contract_json['networks']['5777']['address']

        # Stage 4: Initialize contract instance
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        return contract, web3
    except Exception as e:
        print('Error connecting with blockchain:', e)

try:
    contract, web3 = connect_with_blockchain('0x8391BE76f2181188FeDA980B4b08925b3e19f0f1')

    tx_hash = contract.functions.uploadProduct("123", "abhi", "100").transact()
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print("Uploaded product. Transaction receipt:", receipt)

    tx_hash1 = contract.functions.reportFakeProduct("123").transact()
    receipt1 = web3.eth.waitForTransactionReceipt(tx_hash1)
    print("Reported fake product. Transaction receipt:", receipt1)

    tx_hash3 = contract.functions.isFakeProduct("132").call()  # Using call to get return value
    print("Is product fake?", tx_hash3)

except Exception as e:
    print("Error:", e)
