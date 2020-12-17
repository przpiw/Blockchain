from ecoin import *
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

"""
 Simple API that demonstrate basic functionality of the blockchain
"""
# Flask Web App to interact with created blockchain
app = Flask(__name__)

# Creating an address for the node on port 5000
node_address = str(uuid4()).replace('-','')


# Blockchain instance
blockchain = Blockchain()

# Route decorator to tell Flask what URL should trigger function

# GET This will mine a next block and add it to the blockchain
@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver = 'You', amount = 1)
    new_block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'You have mined a block!',
                'index':new_block['index'],
                'timestamp':new_block['timestamp'],
                'proof':new_block['proof'],
                'previous_hash':new_block['previous_hash'],
                'transactions': new_block['transactions']}
    return jsonify(response),200
    
# GET the full blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# GET check if blockchain is valid'
@app.route('/is_valid',methods=['GET'])
def is_valid_chain():
    is_blockchain_valid = blockchain.is_chain_vaild(blockchain.chain)
    response = {'is_valid':is_blockchain_valid}
    return jsonify(response),200
    
# POST Add a new transaction
@app.route('/add_transaction',methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender','receiver','amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing',400
    index = blockchain.add_transaction(json['sender'], json[
        'receiver'], json['amount'])
    response = {'message':f'This transaction will be added to Block {index}'}
    return jsonify(response),201
    
# Decentrilizing Blockchain

# Connect new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The ecoin blockchain now contains the following nodes:',
                'total_nodes':list(blockchain.nodes)}
    return jsonify(response),201

# GET Replace the chain by the longest chain if needed
@app.route('/replace_chain',methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Replaced chain with the longest one',
                    'new_chain':blockchain.chain}
    else:
        response: {'message': 'The chain is the largest one',
                   'current chain':blockchain.chain}
    return jsonify(response),200

# Running the app
app.run(host='0.0.0.0',port=5003)
