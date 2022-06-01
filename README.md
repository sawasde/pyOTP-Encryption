# OTP-Encryption

[![Na|solid](https://img.shields.io/badge/license-GPL-brightgreen)](https://github.com/alturiano/OTP-Encryption/blob/main/LICENSE) [![Na|solid](https://img.shields.io/badge/python-3.8-brightgreen)](https://github.com/alturiano/OTP-Encryption/blob/master/LICENSE) ![example workflow](https://github.com/r00ne/pyOTP-Encryption/actions/workflows/python-app.yml/badge.svg)



This is an encryption/decryption **poc** written in python based on one-time pad **(OTP) encryption**. The program essentially XOR's two files (source file & key file) together to create an encrypted file (output file). The key file must be at least as long as the source file. If you want to use an offset then the key file must be at least as long as **sourcefile + offset**.

**One-time pad encryption is theoretically [unbreakable](https://en.wikipedia.org/wiki/One-time_pad) when used correctly.**

# Usage

### Python 3
    python otp.py -s <sourcefile> -k <keyfile> -o <outputfile> -x <offset (default 0)>

        -s <sourcefile>  Source file to be encrypted/decrypted
        -o <outputfile>  Output file with the results
        -k <keyfile>     KeyFile or Pad with the encryption key
        -x <offset>      (Optional) Start the encryption with x bytes offset. Default is 0
    
### Docker
----
Build the container in root of the repository:

    docker build -t pyotp-encryption .

Run the containter in the root of the repository. The files you want to encrypt/decrypt should be on the root of the repository as well:

##### Linux/MacOS/Powershell

    docker run -v ${PWD}:/home pyotp-encryption -s <sourcefile> -k <keyfile> -o <outputfile> -x <offset (default 0)>
    
##### Windows

    docker run -v %cd%:/home pyotp-encryption -s <sourcefile> -k <keyfile> -o <outputfile> -x <offset (default 0)>

### Modes
----
##### Encryption Mode
`<sourcefile>` is the file you want to encrypt, `<outputfile>` is the file that would eventually be encrypted, `<keyfile>` or pad file is the encryption key, `<offset (default 0)>` to start the encryption with x bytes offset from the first byte on the keyfile.

##### Decryption Mode
`<sourcefile>` is the encrypted file you want to decrypt, `<outputfile>` is the file that would be eventually decrypted to plain text, `<keyfile>` or pad file is the key that was used to encrypt the original file, `<offset (default 0)>` the offset used to encrypt the original file

# Other Versions

There is a C version version [here](https://github.com/alturiano/OTP-Encryption).
