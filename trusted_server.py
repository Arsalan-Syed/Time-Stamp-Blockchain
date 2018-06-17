from flask import Flask
from flask import request
import json  
from blockchain import Blockchain
import random

bc=Blockchain()
peer_urls=set([])

app=Flask(__name__)


@app.before_first_request
def setup():
	

@app.route('/peerlist',methods=["GET"])
def get_peers():
	return json.dumps(peer_urls)
	


	
	
app.run()