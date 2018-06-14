import hashlib


class File:

	def __init__(self,file_name,author,hash):
		self.file_name=file_name
		self.author=author
		self.hash=hash	

def open_file(file_name):
	file = open(file_name,"rb")
	byte_data = file.read()
	file.close()
	return byte_data
	
#Should work regardless of file format
def get_file_hash(file_name):
	file_data=open_file(file_name)
	sha = hashlib.sha256()
	sha.update(file_data)
	return sha.hexdigest()
	