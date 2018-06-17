from flask import Flask
from flask import request
import json  
from blockchain import Blockchain
import random
import filemanager as fm

bc=Blockchain()
trusted_servers = []
server_config='{"trusted":true,"host_name":"127.0.0.1:5003"}'
config=json.loads(server_config)

app=Flask(__name__)

class ServerInfo:
	
	def __init__(self,id,ip,port):
		self.id=id
		self.ip=ip
		self.port=port
		
		

#payload is a python dict
def send_post(url,payload):
	return requests.post(url, json=payload)


def read_trusted_servers():

    servers_filename = 'trusted_servers.txt'

    with open(servers_filename, 'r') as fp:

        for line in fp.readlines():
            server_id = int(line.split()[0])
            server_ip = line.split()[1]
            port  = int(line.split()[2])
            trusted_servers.append(ServerInfo(server_id, server_ip, port))


@app.before_first_request
def setup():
	
	read_trusted_servers()
	print(trusted_servers)
	
	trusted_peers_list=[]
	
	if not config["trusted"]:
		print("Obtaining peer lists")
		for server in trusted_servers:
			trusted_url="http://"+server.ip+":"+server.port
			register_url=trusted_url+"/register"
			list_url=trusted_url+"/peerlist"
			
			#Register you hostname
			send_post(register_url,{"host":config["host_name"]})
			
			#Get all hosts from trusted server
			peer_list=requests.get(list_url)
			for p in peer_list:
				trusted_peers_list.append(p)
				
	#now have master list from trusted peers, tries to discover more from non trusted
	fetch_all_peers(trusted_peers_list)
			
	return ""
	
def get_peer_list(host):
	url=host+"/peerlist"
	peer_str=request.get(url).content

def fetch_all_peers(peer_list):
	return ""

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
	
@app.route('/peerlist',methods=["GET"])
def get_peers():
	return json.dumps(peer_urls)
	
@app.route('/register',methods=["POST"])
def start():
	if request.method=="POST":
		
		
	
'''	
@app.route('/create',methods=["GET","POST"])
def create():
	key = RSA.generate(2048)
	print(key)
	return ""
		
		
#
key = RSA.generate(2048)
print(key)
'''

#app.run()