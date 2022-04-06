import argparse
import sys
from os import path

def validate_file(filename):
	""" Validate if file exits, then return the abs path"""

	abs_path = ""

	try:
		if path.exists(filename):
			abs_path = path.abspath(filename)
		else:
			raise Exception("File <{}> does not exist".format(filename))
	
	except Exception as e:
		print("[-] Error on validate_file:", e)

	finally:
		return abs_path

def file_to_bytes(filename):
	""" Convert file to bytes"""

	result = ""

	try:
		with open(filename,"rb") as f:
			result = f.read()
	except Exception as e:
		print("[-] Error on file_to_bytes:", e)

	finally:
		return result

def validate_length(source, key, offset):
	""" Check if file length is okay"""

	try:
		source_len = len(source)
		key_len = len(key)

		print('[*] Source length:', source_len)
		print('[*] Key length:', key_len)
		print('[*] Offset:', offset)
		
		if source_len < 1:
			raise Exception("Invalid Source file length")

		if key_len < 1:
			raise Exception("Invalid Key file length")

		if key_len < (source_len + offset):
			raise Exception("Source file is larger than keyfile + offset")

	except Exception as e:
		print("[-] Error on validate_length:", e)
		sys.exit(-1)

def encrypt(source, key, offset):
	""" XOR each correspond byte starting on offset"""
	
	result =[]

	try:
		key = key[offset:-1]

		for b1, b2 in zip(source, key):
			result.append (b1^b2)

		return bytes(result)
	
	except Exception as e:
		print("[-] Error on encrypt", e)
		sys.exit(-1)

def save_output(result, filename):
	""" Save the encrypted result to the output file"""
	
	try:
		with open(filename, "wb") as f:
			f.write(result)

	except Exception as e:
		print("[-] Error on save_output", e)
		sys.exit(-1)
	

def main():
	
	# Initialize parser
	parser = argparse.ArgumentParser(description="Encrypt Files with OTP-Encryption")
	
	# Get cli Arguments
	parser.add_argument("-s",type=str, metavar='<sourcefile>', dest='source',
						help="Source file to be encrypted/decrypted", required=True)

	parser.add_argument("-o", type=str, metavar='<outputfile>', dest='output', 
						help="Output file with the results", required=True)

	parser.add_argument("-k", type=str, metavar='<keyfile>', dest='key',
						help="KeyFile or Pad with the encryption key", required=True)

	parser.add_argument("-x", type=int, metavar='<offset>', default=0, dest='offset',
						help="(Optional) Start the encryption with x bytes offset. Default is 0", required=False)
	
	args = parser.parse_args()
	
	# Validate source and key files
	print('[+] Validating Files')
	source = validate_file(args.source) 
	key = validate_file(args.key)

	# Asign output & offset
	output = args.output
	offset = args.offset

	# Convert to Bytes source and key files
	print('[+] Files to Bytes')
	source_bytes = file_to_bytes(source)
	key_bytes = file_to_bytes(key)

	# Validate length
	print('[+] Source file:', source)
	print('[+] key or Pad file:', key)
	print('[+] Validate Length')
	validate_length(source_bytes, key_bytes, offset)

	# Encrypt
	print('[+] Start Encryption/Decryption')

	result = encrypt(source_bytes, key_bytes, offset)

	# Save to output
	print('[+] Save result on', output)
	save_output(result, output)

	print('[+] Encryption/Decryption done')

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)