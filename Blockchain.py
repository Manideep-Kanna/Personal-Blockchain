#Creating a Blockchain
from time import time
import hashlib
import json 
#from flask import flask,jsonify

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
       The Block which is created :return: The Blocks

        '''

        block={
            'index':len(self.chain)+1,
            'transactions':self.pending_transactions,
            'time':time(),
            'proof':proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions=[]
        self.chain.append(block)
        return block
    @property
    def last_block(self):
        return self.chain[-1]

    def new_transcation(self,sender,reciever,amount):
        transaction={
            'sender':sender,
            'reciever':reciever,
            'amount':amount
        }
        self.pending_transactions.append(transaction)

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


blockchain=Blockchain()
t1=blockchain.new_transcation(sender="Manideep",reciever="Ravi",amount="10 BTC")
t2=blockchain.new_transcation("Manideep","Srinu","20 BTC")
t3=blockchain.new_transcation("Manideep","Kanna","50 BTC")

blockchain.new_block(1234)

t4=blockchain.new_transcation("Kanna","Sujatha","100 BTC")
t5=blockchain.new_transcation("Kanna","Surya","200 BTC")

blockchain.new_block(5678)

print(blockchain.chain)


