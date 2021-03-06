#Creating a Blockchain
from datetime import datetime
import hashlib
import json 
from flask import Flask,jsonify

# Part 1 Building a Blockchain

class Blockchain:
    
    #when the blockchain created these entities should be present
    
    def __init__(self):
        
        #Blockchain consists of an chain of blocks 
        
        self.chain=[]

        #Pending Transactions
        self.pending_transactions=[]
        
        '''
        It also consists of the genesis block whose prev hash is 0 
        to create an new block we need proof and the prev hash as hash is 
        generated using the SHA which only gives us encoded string
        '''
        
        self.new_block(previous_hash="This is The Genesis Block",
                       proof=100)
    def new_block(self,proof,previous_hash=None):

        '''

       Correct value of the Nounce :param proof:
       Previous hash of the Block in the chain :param previous_hash:
       The Block which is created :return: The Block

        '''

        block={
            'index':len(self.chain)+1,
            # 'transactions':self.pending_transactions,
            'time':str(datetime.now()),
            'proof':proof,
            'previous_hash': previous_hash ,
        }
        # self.pending_transactions=[]
        self.chain.append(block)
        return block

    def last_block(self):
        return self.chain[-1]

    # def new_transcation(self,sender,reciever,amount):
    #     transaction={
    #         'sender':sender,
    #         'reciever':reciever,
    #         'amount':amount
    #     }
    #     self.pending_transactions.append(transaction)

#The following functions returns the proof which is generated by an miner

    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            '''
            simple mathematical operation is calculated here x^2-y^2 the reason we took - is because 
            it is not symmentric means => a-b != b-a change the result into string and then encode it 
            into unicode format so that it can be a valid input for sha256 inorder to get the string 
            in hexadecimal format we use hexdigest.
            '''
            hash_generated=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()

            #Simple way of checking weather the hash is valid or not

            if hash_generated[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof

    def hash(self,block):

        #Dumps the string into an json Object

        block_json=json.dumps(block,sort_keys=True)

        #Encodes the json into byte format which can be accepted by hash functions

        block_encoded_json=block_json.encode()

        #Generates the Hash Object

        raw_hash=hashlib.sha256(block_encoded_json)

        # Changes the Hash Object into the hexadecimal Hash

        hex_hash=raw_hash.hexdigest()

        return hex_hash

    def is_valid_chain(self):
        previous_block=self.chain[0]
        block_index=1
        while block_index<len(self.chain):
            block=self.chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            proof=block['proof']
            previous_proof=previous_block['proof']
            hash_generated = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_generated[:4] !='0000':
                return False
        return True


blockchain=Blockchain()

app=Flask(__name__)

@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response)


@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.last_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    block=blockchain.new_block(proof,previous_hash)
    response={
        'message':'Congratulations you have mined your block',
        'index':block['index'],
        # 'transactions':block['transactions'],
        'time':str(block['time']),
        'proof':block['proof'],
        'previous_hash':block['previous_hash']
    }
    return jsonify(response)

@app.route('/is_valid',methods=['GET'])
def is_valid():
    flag=blockchain.is_valid_chain()
    if flag:
        return jsonify({"message":"The Following chain is valid"})
    else:
        jsonify({"message":"The Following chain is not valid"})


app.run(debug=True)



