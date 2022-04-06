import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import otp

SOURCE_FILE = "source_test"
SOURCE_FILE_CONTENT = "Hello World!"
KEY_FILE1 = "key_test1"
KEY_FILE1_CONTENT = "3ncrYpT/D3Cryp/1s/FUn!*|*"
KEY_FILE2 = "key_test2"
KEY_FILE2_CONTENT = b"\xa3\x92\xc1\xaf\xb3\xf8\xfb\xe3\xcd\xe6\xa3\x82\x01\n\x02\x82\x01\x01\x00\xe4\x91\xa9\t\x1f\x91\xdb\x1e\xeb\x05\xed\x84\xeb\xa2\xec\x8b\x19\x89\xde\xf9\xf5\x07\xab\x02\xe8\x18\xf8"

def populate_file(value, filename):
	with open(filename, 'wb') as f:
		f.write(value)

def remove_file(filename):
	os.remove(filename)

def test_validate_file_ok():

	populate_file(b'',SOURCE_FILE)

	file_path = otp.validate_file(SOURCE_FILE)
	file_name = file_path.split('/')[-1]
	
	remove_file(SOURCE_FILE)
	
	assert SOURCE_FILE == file_name

def test_validate_file_fail():

	file_path = otp.validate_file("fail")
	
	assert file_path == ""