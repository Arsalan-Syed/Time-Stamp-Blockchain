import datetime
import hashlib
import random

class Block:
	
	#Compute the hash of this block
	def hash_block(self):
		sha = hashlib.sha256()
		s=str(self.data)+str(self.previous_hash)
		sha.update(s.encode())
		return sha.hexdigest()
	
	#Initialize the class
	def __init__(self, index, timestamp, data, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash
		self.hash = self.hash_block()
		
	def get_block_JSON(self):
		s='{\n'+'"Index": "'+str(self.index)+'",\n'+'"Timestamp":"'+str(self.timestamp)+'",\n'+'"Data":'+str(self.data)+',\n'+'"Previous hash":"'+str(self.previous_hash)+'",\n'+'"Current hash":"'+str(self.hash)+'"\n}\n'
		return s
		
	def print_block(self):
		print(self.get_block_JSON())
		

class Blockchain:

	#TODO have a stricter condition
	def check_valid_hash(self,data,previous_hash):
		sha = hashlib.sha256()
		s=str(data)+str(previous_hash)
		sha.update(s.encode())
		return sha.hexdigest()[0]=='0'

	#Returns first block in chain
	def create_genesis_block(self):
		data='{"file_name":"Genesis","file_hash":0,"proof":"0"}'
		return Block(0,datetime.datetime.now(),data,'0')
		
	#Returns next block in chain
	def create_data_block(self,data):
		index=self.prev_block.index+1
		timestamp=datetime.datetime.now()
		previous_hash=self.prev_block.hash
		
		if self.check_valid_hash(data,previous_hash):
			print(data+"\n")
			return Block(index,timestamp,data,previous_hash)
		else:
			return None
		
	def dataToJSON(self,data_list):
		s='{'
		for d in data_list:
			key='"'+d[0]+'"'
			value='"'+d[1]+'"'
			s=s+key+':'+value+',\n'
		s=s[:-2]+'}'
		return s
		
	def update_prev_block(self,next_block):
		self.prev_block=next_block
		
	def add_block(self,file_name,file_hash):
		
		next_block=None
		
		#Mine's the next block
		while next_block is None:
			proof=str(random.randint(0,1000))
			data_list=[('file_name',file_name),('file_hash',file_hash),('proof',proof)]
			next_block=self.create_data_block(self.dataToJSON(data_list))
						
		if(next_block is None):
			print('Invalid block hash')
		else:
			self.chain.append(next_block)
			self.update_prev_block(next_block)
		
	#Returns list of all blocks with given filename
	#TODO
	def search_block_by_file_name(self,file_name):
		return []

	#Return block with given file hash
	#TODO
	def search_block_by_file_hash(self,file_hash):
		return ''
		
	def get_blockchain_JSON(self):
		s='{\n"blocks":[\n'
		for b in self.chain:
			s=s+b.get_block_JSON()+',\n'
		s=s[:-2]+'\n]\n}'
		return s
	
	#TODO init using JSON encoded string
	def load_blockchain_JSON(json_data):
	
		
	def print_blockchain(self):
		print(self.get_blockchain_JSON())
		
	def __init__(self):
		self.chain=[self.create_genesis_block()]
		self.prev_block=self.chain[0]		
		
def main():	
	blockchain = Blockchain()	

	for i in range(3):
		blockchain.add_block('test.jpg','012345','0')

		
	for b in blockchain.chain:
		b.print_block();

#main()