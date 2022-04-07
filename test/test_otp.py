import os
import sys
from pathlib import Path
from subprocess import Popen, PIPE

sys.path.append(str(Path(__file__).resolve().parents[1]))

import otp  # noqa: E402

SOURCE_FILE = "source_test"
SOURCE_FILE_CONTENT = b"Hello World!"
KEY_FILE1 = "key_test1"
KEY_FILE1_CONTENT = b"3ncrYpT"
KEY_FILE2 = "key_test2"
KEY_FILE2_CONTENT = b"""
\xa3\x92\xc1\xaf\xb3\xf8\xfb\xe3\xcd\xe6\xa3\x82\x01\n\x02\x82\x01\x01
\x00\xe4\x91\xa9\t\x1f\x91\xdb\x1e\xeb\x05\xed\x84\xeb\xa2\xec\x8b\x19
\x89\xde\xf9\xf5\x07\xab\x02\xe8\x18\xf8"""


def populate_file(value, filename):
    with open(filename, 'wb') as f:
        f.write(value)


def remove_file(filename):
    os.remove(filename)


def test_validate_file_ok():

    populate_file(b'', SOURCE_FILE)

    file_path = otp.validate_file(SOURCE_FILE)
    file_name = file_path.split('/')[-1]

    remove_file(SOURCE_FILE)

    assert SOURCE_FILE == file_name


def test_validate_file_fail():

    file_path = otp.validate_file("fail")
    expected_result = ""

    assert file_path == expected_result


def test_file_to_bytes_ok():

    populate_file(SOURCE_FILE_CONTENT, SOURCE_FILE)

    file_bytes = otp.file_to_bytes(SOURCE_FILE)

    remove_file(SOURCE_FILE)

    assert SOURCE_FILE_CONTENT[0] == file_bytes[0]


def test_file_to_bytes_fail():

    file_bytes = otp.file_to_bytes("fail")
    expected_result = ""

    assert file_bytes == expected_result


def test_validate_length_ok():

    result = otp.validate_length(SOURCE_FILE_CONTENT, KEY_FILE2_CONTENT, 0)
    expected_result = True

    assert result == expected_result


def test_validate_length_fail():

    result1 = otp.validate_length(b'', KEY_FILE1_CONTENT, 0)
    result2 = otp.validate_length(SOURCE_FILE_CONTENT, b'', 0)
    result3 = otp.validate_length(SOURCE_FILE_CONTENT, KEY_FILE1_CONTENT, 0)
    result4 = otp.validate_length(SOURCE_FILE_CONTENT, KEY_FILE1_CONTENT, 999)
    expected_result = False

    assert result1 == expected_result
    assert result2 == expected_result
    assert result3 == expected_result
    assert result4 == expected_result


def test_encrypt_ok():

    encrypted = otp.encrypt(SOURCE_FILE_CONTENT, KEY_FILE2_CONTENT, 4)
    decrypted = otp.encrypt(encrypted, KEY_FILE2_CONTENT, 4)

    assert SOURCE_FILE_CONTENT == decrypted


def test_encrypt_fail():

    encrypted = otp.encrypt(1, KEY_FILE1_CONTENT, 4)
    expected_result = None

    assert encrypted == expected_result


def test_save_output_ok():

    result = otp.save_output(KEY_FILE2_CONTENT, SOURCE_FILE)

    remove_file(SOURCE_FILE)
    expected_result = True

    assert result == expected_result


def test_save_output_fail():

    result = otp.save_output(1, SOURCE_FILE)

    remove_file(SOURCE_FILE)
    expected_result = False

    assert result == expected_result


def test_exit_code_ok():
    """ Sucessfully Encrypt file"""

    populate_file(SOURCE_FILE_CONTENT, SOURCE_FILE)
    populate_file(KEY_FILE2_CONTENT, KEY_FILE2)
    outfile = 'out'

    command = ['python3', 'otp.py', '-s', SOURCE_FILE, '-k', KEY_FILE2, '-o', outfile, '-x', '4']
    child = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = child.communicate()

    rc = child.returncode

    remove_file(SOURCE_FILE)
    remove_file(KEY_FILE2)
    remove_file(outfile)
    expected_result = 0

    assert rc == expected_result


def test_exit_code_fail1():
    """ Fail because key file is smaller"""

    populate_file(SOURCE_FILE_CONTENT, SOURCE_FILE)
    populate_file(KEY_FILE1_CONTENT, KEY_FILE1)

    command = ['python3', 'otp.py', '-s', SOURCE_FILE, '-k', KEY_FILE1, '-o', 'never_created', '-x', '0']
    child = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = child.communicate()

    rc = child.returncode

    remove_file(SOURCE_FILE)
    remove_file(KEY_FILE1)
    expected_result = 1

    assert rc == expected_result


def test_exit_code_fail2():
    """ Fail because key file is ok but offset is larger"""

    populate_file(SOURCE_FILE_CONTENT, SOURCE_FILE)
    populate_file(KEY_FILE2_CONTENT, KEY_FILE2)

    command = ['python3', 'otp.py', '-s', SOURCE_FILE, '-k', KEY_FILE2, '-o', 'never_created', '-x', '444']
    child = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = child.communicate()

    rc = child.returncode

    remove_file(SOURCE_FILE)
    remove_file(KEY_FILE2)
    expected_result = 1

    assert rc == expected_result


def test_parse_args():

    result = otp.parse_args(['-s', 's', '-k', 'k', '-o', 'o', '-x', '0'])

    assert result.source == 's'
    assert result.key == 'k'
    assert result.output == 'o'
    assert result.offset == 0


def test_main_ok():

    populate_file(SOURCE_FILE_CONTENT, SOURCE_FILE)
    populate_file(KEY_FILE2_CONTENT, KEY_FILE2)
    encrypted = 'enc'
    decrypted = 'dec'
    result = ''

    otp.main(['-s', SOURCE_FILE, '-k', KEY_FILE2, '-o', encrypted, '-x', '0'])
    otp.main(['-s', encrypted, '-k', KEY_FILE2, '-o', decrypted, '-x', '0'])

    with open(decrypted, 'rb') as f:
        result = f.read()

    remove_file(SOURCE_FILE)
    remove_file(KEY_FILE2)
    remove_file(encrypted)
    remove_file(decrypted)

    assert result == SOURCE_FILE_CONTENT


def test_main_fail1():
    """ Fail because key file is smaller"""

    populate_file(SOURCE_FILE_CONTENT, SOURCE_FILE)
    populate_file(KEY_FILE1_CONTENT, KEY_FILE1)
    encrypted = 'enc'

    try:
        otp.main(['-s', SOURCE_FILE, '-k', KEY_FILE1, '-o', encrypted, '-x', '0'])
        result = 'ok'
    except SystemExit:
        result = 'fail'

    remove_file(SOURCE_FILE)
    remove_file(KEY_FILE1)
    expected_result = 'fail'

    assert result == expected_result


def test_main_fail2(monkeypatch):
    """ Fail because encrypt not working"""

    def bad_encrypt(s, k, o):
        return None

    monkeypatch.setattr(otp, 'encrypt', bad_encrypt)

    populate_file(SOURCE_FILE_CONTENT, SOURCE_FILE)
    populate_file(KEY_FILE2_CONTENT, KEY_FILE2)
    encrypted = 'enc'

    try:
        otp.main(['-s', SOURCE_FILE, '-k', KEY_FILE2, '-o', encrypted, '-x', '0'])
        result = 'ok'
    except SystemExit:
        result = 'fail'

    remove_file(SOURCE_FILE)
    remove_file(KEY_FILE2)
    expected_result = 'fail'

    assert result == expected_result


def test_main_fail3(monkeypatch):
    """ Fail because outfile content is no valid"""

    def bad_encrypt(s, k, o):
        return True

    monkeypatch.setattr(otp, 'encrypt', bad_encrypt)

    populate_file(SOURCE_FILE_CONTENT, SOURCE_FILE)
    populate_file(KEY_FILE2_CONTENT, KEY_FILE2)
    encrypted = 'enc'

    try:
        otp.main(['-s', SOURCE_FILE, '-k', KEY_FILE2, '-o', encrypted, '-x', '0'])
        result = 'ok'
    except SystemExit:
        result = 'fail'

    remove_file(SOURCE_FILE)
    remove_file(KEY_FILE2)
    remove_file(encrypted)
    expected_result = 'fail'

    assert result == expected_result
