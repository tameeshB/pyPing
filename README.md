# pyPingCLI
## End-to-End AES256 Encrypted direct local and global terminal messaging

## Installation
```pip install pypingcli```
## Usage
```pyping start```
## Peer-To-Peer Architecture 
[Sockets sub-module : pyPing/pypingcli/sockets ](https://github.com/tameeshB/pyPing/tree/master/pypingcli/sockets)
- Either of the peers(_A_) starts accepting connection requests.
- The other peer(_B_) requests to connect.
- _A_ accepts request and initiates key handshake.

## Key Handshake
[CryptoManager sub-module : pyPing/pypingcli/cryptoManager ](https://github.com/tameeshB/pyPing/tree/master/pypingcli/cryptoManager)
- Server peer sends a ```/asymkey?:``` after accepting connection to request for the asymetric key.
- _B_ responds ```/asymkey:<pubKey>``` with a generated RSA Public Key.
- _A_ generates 256-bit AES Key, encrypts it with RSA Public Key obtained from remote and sends the ciphertext key ```/encsymmkey:<symKeyCipher>``` back to the remote.
- _B_ obtains the symmetric 256-bit AES key by deciphering the key.
- All messages sent are now encrypted with the shared symmetric key.

## "Military Grade" Encryption as referred to in fiction
[Advanced Encryption Standard - Wikipedia](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard#Security)
>The National Security Agency (NSA) reviewed all the AES finalists, including Rijndael, and stated that all of them were secure enough for U.S. Government non-classified data. In June 2003, the U.S. Government announced that AES could be used to protect classified information:
>>The design and strength of all key lengths of the AES algorithm (i.e., 128, 192 and 256) are sufficient to protect classified information up to the SECRET level. TOP SECRET information will require use of either the 192 or 256 key lengths.

