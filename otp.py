import argparse
import sys
from os import path

def validate_file(filename):

	abs_path = ''

	try:
		abs_path = path.abspath(filename)
		if path.exists(filename):
			return abs_path
		else:
			raise Exception('File <{}> does not exist'.format(filename))
	
	except Exception as e:
		print(e)



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

	# Save output
	output = args.output

	# Convert to Bytes source and key files


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)