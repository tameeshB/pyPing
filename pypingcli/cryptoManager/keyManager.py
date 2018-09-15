from Crypto import Random
from Crypto.PublicKey import RSA
from pypingcli.cryptoManager.aes import AESCipher
import base64
import json
import globals
import os
import pickle

class KeyManager(AESCipher):
    def __init__(self):
        self.pubKey = None
        self.__privKey = None
        self.__symmKey = None
        self.RSAInstance = None
        # self.bs = 32
        # self.AESInstance = None # Inherited
    def generateSymmKey(self):
        self.__symmKey = self.gen_password(32)
        self.setKeyHash(self.__symmKey)
    
    def generateAsymKeys(self):
        rng = Random.new().read
        self.RSAInstance = RSA.generate(2048, rng)
        self.pubKey = self.RSAInstance.exportKey('OpenSSH')
        return self.pubKey
    
    def keyStatus(self):
        if self.RSAInstance == None:
            return 0 # No keys initialised
        elif self.__symmKey == None:
            return 1 # Public key present but symmKey not present
        else:
            return 2 # All keys in place

    def getEncSymmKey(self, remotePubKey):
        self.generateSymmKey()
        return self.encryptKey(remotePubKey)

    def encryptKey(self, remotePubKey):
        remoteRSA = RSA.importKey(remotePubKey)
        return pickle.dumps(
                remoteRSA.encrypt(self.__symmKey,10)
            ).encode('base64', 'strict')

    def decryptKey(self, symmKeyCipherText):
        self.__symmKey = self.RSAInstance.decrypt(
                pickle.loads(
                    symmKeyCipherText.decode('base64', 'strict')
                    )
            )
        self.setKeyHash(self.__symmKey)
        if len(self.__symmKey) == 32:
            return True
        else:
            return False

    def gen_password(self, length=8, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"):
        random_bytes = os.urandom(length)
        len_charset = len(charset)
        indices = [int(len_charset * (ord(byte) / 256.0)) for byte in random_bytes]
        return "".join([charset[index] for index in indices])