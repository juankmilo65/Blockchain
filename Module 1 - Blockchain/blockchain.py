#Create a Blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

#Step 1 Blockchain setup 
class Blockchain:
    def __init__(self):
        self.Chain=[]
        self.create_block(proof=1, previous_hash='0')
    
    def create_block(self, proof, previous_hash):
        block = {'index':len(self.Chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash': previous_hash}
        
        self.Chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.Chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof= False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] == '0000':
                check_proof =True
            else: 
                new_proof +=1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #Check if chan in valid.
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index =1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
           
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index +=1
        return True
    
# Step 2 Blockchain mine

app = Flask(__name__)
blockchain = Blockchain()

# New block mine
@app.route('/mine_block', methods=['Get'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message':'Felicidades, haz minado un bloque!',
                'index': block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']}
    return jsonify(response), 200

"Obteniendo caneda completa"
@app.route('/get_chain', methods=['Get'])
def get_chain():
    response = {'chain':blockchain.Chain,
                'length':len(blockchain.Chain)}
    return jsonify(response), 200

#
@app.route('/is_valid', methods=['Get'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.Chain)
    if is_valid:
        response = {'message':'Todobien, El blockchain es valido'}
    else:
        response = {'message':'houston, tenemos un problema, el blockchain no es valido'}
    return jsonify(response), 200


#ejecutando el app
app.run(host='0.0.0.0', port='5000')

                
        
    
            