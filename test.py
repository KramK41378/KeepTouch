from hashlib import sha512

print(sha512('1234'.encode('utf-8'), usedforsecurity=True).hexdigest())