from flask import Flask
from flask import request
import json  
from blockchain import Blockchain
import random
#from Crypto.Cipher import RSA

bc=Blockchain()
peer_urls=[]

app=Flask(__name__)

@app.route('/add',methods=["POST"])
def add():
	if request.method=="POST":
		data=request.get_json()
		
		v=valid_data(data)
		
		if v=="":		
			bc.add_block(data["file_name"],data["file_hash"])
			bc.print_blockchain()
			return "Added data"
		else:
			return v,500
		
	return ""
	
def valid_data(data):
	if "file_name" not in data:
		return "Missing key: file_name"
	if "file_hash" not in data:
		return "Missing key: file_hash"
		
	return ""	

@app.route('/blocks',methods=["GET"])
def get_blocks():
	return bc.get_blockchain_JSON()
	
def get_peer_chains(peer_urls):
	peer_chains=[]
	for url in peer_urls:
		peer_bc=requests.get(url+"/blocks").content
		peer_chain_json=json.loads(peer_bc)
		peer_chains.append(peer_chain_json)
		
	return peer_chains
	
def consensus():
	peer_chains=get_peer_chains(peer_urls)
	longest_chain=bc.get_blockchain_JSON()
	for c in peer_chains:
		if len(longest_chain)<len(c):
			longest_chain=c
	bc.load_blockchain_JSON(longest_chain)
	
	
'''	
@app.route('/create',methods=["GET","POST"])
def create():
	key = RSA.generate(2048)
	print(key)
	return ""
		
		
#app.run()
key = RSA.generate(2048)
print(key)
'''