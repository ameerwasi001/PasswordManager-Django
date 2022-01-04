# Password Manager Django
This is not meant for production since production-grade password managers often use a combination of both a master password and a private key stored on the user's device but this one only has the master password as its main secret. This uses powerful RSA and AES-128 bit encryption using the master password which is only ever known by the user. This README will be a short document on the Password manager's design rather than a manual on how to use it, since that is, in my totally unbiased opinion quite self-explanatory.

# Local encryption
The passwords one has stored on their vault follow a simple encryption scheme, all it does is encrypt your password with a randomly generated 128-bit key and then encrypt that key with a key derived from your master password using the PBKDF2/HMAC algorithm. Whenever one needs to decrypt this, they would simply decrypt the key and then decrypt the password using that.

# Password Sharing
Every time a user signs up, their public and private key are generated. While the public key is stored as it is, the private key is encrypted by the master password of the user before being stored. When one sends their password to someone else, the system simply uses their public key to encrypt the AES key of the password in question and sends all of that over. When this password is being viewed for the first time, the AES key is decrypted and then re-encrypted by the receiver's password. Which allows them to view this password whenever they please.
