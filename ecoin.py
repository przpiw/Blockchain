# Blockchain
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import sys
"""
Simple representation of the blockchain
"""
class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = [] # List that will contains transactions
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes= set()
        
        
# Creates a block and appends created block to the blockchain
    def create_block(self, proof, previous_hash):
        # Create next block
        block = {'index': len(self.chain) + 1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = [] # Clear list of the transactions
        self.chain.append(block) # Add block to the chain
        return block
    
# Gets last previous block from the chain    
    def get_previous_block(self):
        return self.chain[-1]
    
# Computes hash that satisfy requirement of blockchain
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
# Hashes given block
    def hash(self, block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
# Checks validity of the blockchain
    def is_chain_valid(self,chain):
        previous_block= chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof'];
            proof = block['proof'];
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
# Add transaction
    def add_transaction(self,sender,receiver,amount):
        self.transactions.append({'sender':sender,
                                  'receiver':receiver,
                                  'amount':amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
# Add node to blockchain
    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
            
# Concensus implementation
    # Replace chain of all nodes that are shorter than node with longest chain
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['lenght']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    
    

