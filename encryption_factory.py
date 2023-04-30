import json
from hashlib import sha256
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
        
        timestamp = data["date"]
        message = json.dumps(data)
        signature = sha256(keys["private"].encode()+message.encode()).hexdigest()
        payload = {"transaction":message,"signature":signature,"public_key":keys["public"]}
        new_proof = 1
        block = self.assemble_block(payload,timestamp,previous_hash,new_proof)      
        hash_value = sha256(json.dumps(block).encode()).hexdigest()
        
        print("Mining a solution for your message.")
        while not ("012" in hash_value or
                   "123" in hash_value or
                   "abc" in hash_value or
                   "xyz" in hash_value or
                   "987" in hash_value or
                   "456" in hash_value): #Encapsular isso aqui
            print(f"Testing proof {new_proof}")
            new_proof += 1
            block["proof"] = str(self.digest_proof(block,new_proof))
            hash_value = sha256(json.dumps(block).encode()).hexdigest()
            if new_proof == 30:
                raise MemoryError
            
        print("Solution found.")
        
        return hash_value, block["proof"]
    
    def assemble_block(self,payload,timestamp,previous_hash,proof):

        block = {"message":payload,
                "timestamp":timestamp,
                "previous_hash":previous_hash,
                "proof" : str(proof)}
        
        return block

    def digest_proof(self,block,new_proof):

        return int(str(new_proof*2 - int(block["proof"])*2))
    
    def recreate_chain_hashes(self,data,keys):
        blockchain_hashes = []
        for idx, transaction in enumerate(data):
            if idx == 0:
                previous_hash = "0"
            else:
                previous_hash = data[idx-1][-2]
            timestamp = transaction[3].strftime("%Y-%m-%d %H:%M:%S")
            payload = {"value":transaction[2],"date":timestamp,"id":transaction[1]}
            proof = transaction[-1]
            message = json.dumps(payload)
            signature = sha256(keys["private"].encode()+message.encode()).hexdigest()
            payload = {"transaction":message,"signature":signature,"public_key":keys["public"]}
            block = self.assemble_block(payload,timestamp,previous_hash,proof)      
            hash = sha256(json.dumps(block).encode()).hexdigest()
            blockchain_hashes.append(hash)
        
        return blockchain_hashes
