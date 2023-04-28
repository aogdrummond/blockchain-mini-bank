import json
from hashlib import sha256
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class Encryption:

    def create_keys_pair(self):
        """
        """
        def clean_key(key_string):
            return key_string.replace("'","")
        
        private_key = rsa.generate_private_key(public_exponent=65537,
                                               key_size=2048)

        encrypted_pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())

        pem_public_key = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo)
        public_key = clean_key(str(pem_public_key))
        private_key = clean_key(str(encrypted_pem_private_key))
        
        return public_key, private_key
    
    def encrypt_transaction(self,data,previous_hash,keys):
        
        message = json.dumps(data)
        signature = sha256(keys["private"].encode()+message.encode()).hexdigest()
        payload = {"message":message,"signature":signature,"public_key":keys["public"]}
        new_proof = 1
        block = {"message":payload,
                 "timestamp":str(datetime.now()),
                 "previous_hash":previous_hash,
                 "proof" : new_proof}
        
        hash_value = sha256(json.dumps(block).encode()).hexdigest()
        
        print("Mining a solution for your message.")
        while not ("01" in hash_value):
            print(f"Testing proof {new_proof}")
            new_proof += 1
            block["proof"] = self.digest_proof(block,new_proof)
            hash_value = sha256(json.dumps(block).encode()).hexdigest()
        print("Solution found.")
        return hash_value 

    def digest_proof(self,block,new_proof):

        return int(str(new_proof**2 - block["proof"]**2))
