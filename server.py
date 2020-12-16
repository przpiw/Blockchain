from blockchain import *
from flask import Flask, jsonify
"""
 Simple API that demonstrate basic functionality of the blockchain
"""
# Flask Web App to interact with created blockchain
app = Flask(__name__)

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
    new_block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'You have mined a block!',
                'index':new_block['index'],
                'timestamp':new_block['timestamp'],
                'proof':new_block['proof'],
                'previous_hash':new_block['previous_hash']}
    return jsonify(response),200
    
# GET the full blockchain
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'lenght': len(blockchain.chain)}
    return jsonify(response),200

# GET check if blockchain is valid'
@app.route('/is_valid',methods=['GET'])
def is_valid_chain():
    is_blockchain_valid = blockchain.is_chain_vaild(blockchain.chain)
    response = {'is_valid':is_blockchain_valid}
    return jsonify(response),200
    

# Running the app
app.run(host='0.0.0.0',port=5000)
