# great thanks to Jerico Alcaras and Ciaran Moyne  with python sytanx help  ( my first python program)


import json
from pprint import pprint
from hashlib import sha256
import secretsharing as sss
import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import json


def load_inferno():                             # loads a .json to a python dict 
    with open('inferno.json') as f:
        temp = json.load(f)
   
    return temp

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def decrypt(enc, password):
  #  private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(password.zfill(32).decode('hex'), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

def pxor(pwd,share):
    '''
      XOR a hashed password into a Shamir-share

      1st few chars of share are index, then "-" then hexdigits
      we'll return the same index, then "-" then xor(hexdigits,sha256(pwd))
      we truncate the sha256(pwd) to if the hexdigits are shorter
      we left pad the sha256(pwd) with zeros if the hexdigits are longer
      we left pad the output with zeros to the full length we xor'd
    '''
    words=share.split("-")
    hexshare=words[1]
    slen=len(hexshare)
    hashpwd=sha256(pwd).hexdigest()
    hlen=len(hashpwd)
    outlen=0
    if slen<hlen:
        outlen=slen
        hashpwd=hashpwd[0:outlen]
    elif slen>hlen:
        outlen=slen
        hashpwd=hashpwd.zfill(outlen)
    else:
        outlen=hlen
    xorvalue=int(hexshare, 16) ^ int(hashpwd, 16) # convert to integers and xor 
    paddedresult='{:x}'.format(xorvalue)          # convert back to hex
    paddedresult=paddedresult.zfill(outlen)       # pad left
    result=words[0]+"-"+paddedresult              # put index back
    return result



inferno_Dict = load_inferno()
hashes = inferno_Dict['hashes']
shares = inferno_Dict['shares']
pot = open('john.pot','r')
#import pdb; pdb.set_trace()
lines = pot.read().split('\n')
xored = []      # list of plaintext xor share
secrets = []

for i, hash in enumerate(hashes):
    for line in lines:
     if hash in line:
         pwd = line.split(':')[1]
         xoring = pxor(pwd,shares[i])
         xored.append(str(xoring))
pprint(xored)





secret1=sss.SecretSharer.recover_secret(xored)
print(secret1)
xored.pop()
secret2=sss.SecretSharer.recover_secret(xored)
print(secret2)

if (secret1 == secret2):
    print("level complete")
    ciphertext = inferno_Dict['ciphertext']
    nextCiphertext = decrypt(ciphertext, secret2)     #pass it ciphertext / secret once passed k
    outputFile = open('nextLevel.json','a')
    outputFile.write(nextCiphertext)

    
    
    
    

    




















